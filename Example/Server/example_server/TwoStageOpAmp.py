""" 
# Two Stage Op Amp
"""

from copy import deepcopy
from dataclasses import asdict

import numpy

import hdl21 as h
import hdl21.sim as hs
import vlsirtools.spice as vsp
from hdl21.external_module import SpiceType
from hdl21.prefix import µ, NANO

from example_shared import auto_ckt_sim, AutoCktInput, AutoCktOutput


@auto_ckt_sim.impl
def auto_ckt_sim(inp: AutoCktInput) -> AutoCktOutput:
    """
    AutoCkt Simulation
    """
    if not vsp.ngspice.available():
        raise RuntimeError

    # Convert our input into `OpAmpParams`
    params = OpAmpParams(**asdict(inp))

    # Create a set of simulation input for it
    sim_input = OpAmpSim(params)

    # Simulation options
    opts = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE,
        fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
        rundir="./scratch",  # Set the working directory for the simulation. Uses a temporary directory by default.
    )

    # Run the simulation!
    results = sim_input.run(opts)

    # Extract our metrics from those results
    ac_result = results["ac"]
    sig_out = ac_result.data["v(xtop.sig_out)"]
    gain = find_dc_gain(2 * sig_out)
    ugbw = find_ugbw(ac_result.freq, 2 * sig_out)
    phm = find_phm(ac_result.freq, 2 * sig_out)
    idd = ac_result.data["i(v.xtop.vvdc)"]
    ibias = find_I_vdd(idd)

    # And return them as an `AutoCktOutput`
    return AutoCktOutput(
        ugbw=ugbw,
        gain=gain,
        phm=phm,
        ibias=ibias,
    )


""" 
Create a small "PDK" consisting of an externally-defined Nmos and Pmos transistor. 
Real versions will have some more parameters; these just have multiplier "m". 
"""


@h.paramclass
class PdkMosParams:
    w = h.Param(dtype=h.Scalar, desc="Width in resolution units", default=0.5 * µ)
    l = h.Param(dtype=h.Scalar, desc="Length in resolution units", default=90 * NANO)
    nf = h.Param(dtype=h.Scalar, desc="Number of parallel fingers", default=1)
    m = h.Param(dtype=h.Scalar, desc="Transistor Multiplier", default=1)


nmos = h.ExternalModule(
    name="nmos",
    desc="Nmos Transistor (Multiplier Param Only!)",
    port_list=deepcopy(h.Mos.port_list),
    paramtype=PdkMosParams,
    spicetype=SpiceType.MOS,
)
pmos = h.ExternalModule(
    name="pmos",
    desc="Pmos Transistor (Multiplier Param Only!)",
    port_list=deepcopy(h.Mos.port_list),
    paramtype=PdkMosParams,
    spicetype=SpiceType.MOS,
)


@h.paramclass
class OpAmpParams:
    """Parameter class"""

    wp1 = h.Param(dtype=int, desc="Width of PMOS mp1", default=10)
    wp2 = h.Param(dtype=int, desc="Width of PMOS mp2", default=10)
    wp3 = h.Param(dtype=int, desc="Width of PMOS mp3", default=4)
    wn1 = h.Param(dtype=int, desc="Width of NMOS mn1", default=38)
    wn2 = h.Param(dtype=int, desc="Width of NMOS mn2", default=38)
    wn3 = h.Param(dtype=int, desc="Width of NMOS mn3", default=9)
    wn4 = h.Param(dtype=int, desc="Width of NMOS mn4", default=20)
    wn5 = h.Param(dtype=int, desc="Width of NMOS mn5", default=60)
    VDD = h.Param(dtype=h.Scalar, desc="VDD voltage", default=1.2)
    CL = h.Param(dtype=h.Scalar, desc="CL capacitance", default=1e-11)
    Cc = h.Param(dtype=h.Scalar, desc="Cc capacitance", default=3e-12)
    ibias = h.Param(dtype=h.Scalar, desc="ibias current", default=3e-5)


@h.generator
def OpAmp(p: OpAmpParams) -> h.Module:
    """# Two stage OpAmp"""

    @h.module
    class OpAmp:
        # IO Interface
        VDD, VSS = 2 * h.Input()
        ibias = h.Input()

        inp = h.Diff(desc="Differential Input", port=True, role=h.Diff.Roles.SINK)
        out = h.Output()

        # Internal Signals
        net3, net4, net5 = h.Signals(3)

        # Input Stage
        mp1 = pmos(m=p.wp1)(
            d=net4, g=net4, s=VDD, b=VDD
        )  # Current mirror within the input stage
        mp2 = pmos(m=p.wp2)(
            d=net5, g=net4, s=VDD, b=VDD
        )  # Current mirror within the input stage
        mn1 = nmos(m=p.wn1)(d=net4, g=inp.n, s=net3, b=net3)  # Input MOS pair
        mn2 = nmos(m=p.wn2)(d=net5, g=inp.p, s=net3, b=net3)  # Input MOS pair
        mn3 = nmos(m=p.wn3)(d=net3, g=ibias, s=VSS, b=VSS)  # Mirrored current source

        # Output Stage
        mp3 = pmos(m=p.wp3)(d=out, g=net5, s=VDD, b=VDD)  # Output inverter
        mn5 = nmos(m=p.wn5)(d=out, g=ibias, s=VSS, b=VSS)  # Output inverter
        CL = h.Cap(c=p.CL)(p=out, n=VSS)  # Load capacitance

        # Biasing
        mn4 = nmos(m=p.wn4)(
            d=ibias, g=ibias, s=VSS, b=VSS
        )  # Current mirror co-operating with mn3

        # Compensation Network
        Cc = h.Cap(c=p.Cc)(p=net5, n=out)  # Miller Capacitance

    return OpAmp


def OpAmpSim(params: OpAmpParams) -> h.sim.Sim:
    """# Op Amp Simulation Input"""

    @hs.sim
    class OpAmpSim:
        @h.module
        class Tb:
            """# Testbench"""

            VSS = h.Port()  # The testbench interface: sole port VSS
            vdc = h.Vdc(dc=1.2)(n=VSS)  # A DC voltage source
            dcin = h.Diff()
            sig_out = h.Signal()
            i_bias = h.Signal()
            sig_p = h.Vdc(dc=0.6, ac=0.5)(p=dcin.p, n=VSS)
            sig_n = h.Vdc(dc=0.6, ac=-0.5)(p=dcin.n, n=VSS)
            Isource = h.Isrc(dc=3e-5)(p=vdc.p, n=i_bias)

            inst = OpAmp(params)(
                VDD=vdc.p, VSS=VSS, ibias=i_bias, inp=dcin, out=sig_out
            )

        # Simulation Stimulus
        op = hs.Op()
        ac = hs.Ac(sweep=hs.LogSweep(1e1, 1e10, 10))
        mod = hs.Include("../45nm_bulk.txt")

    return OpAmpSim


def find_I_vdd(vout: numpy.array) -> float:
    return numpy.abs(vout)[0]


def find_dc_gain(vout: numpy.array) -> float:
    return numpy.abs(vout)[0]


def find_ugbw(freq: numpy.array, vout: numpy.array) -> float:
    gain = numpy.abs(vout)
    ugbw_index, valid = _get_best_crossing(gain, val=1)
    if valid:
        return freq[ugbw_index]
    else:
        return freq[0]


def find_phm(freq: numpy.array, vout: numpy.array) -> float:
    gain = numpy.abs(vout)
    phase = numpy.angle(vout, deg=False)
    phase = numpy.unwrap(phase)  # unwrap the discontinuity
    phase = numpy.rad2deg(phase)  # convert to degrees

    ugbw_index, valid = _get_best_crossing(gain, val=1)
    if valid:
        if phase[ugbw_index] > 0:
            return -180 + phase[ugbw_index]
        else:
            return 180 + phase[ugbw_index]
    else:
        return -180


def _get_best_crossing(yvec: numpy.array, val: float) -> tuple[int, bool]:
    zero_crossings = numpy.where(numpy.diff(numpy.sign(yvec - val)))[0]
    if len(zero_crossings) == 0:
        return 0, False
    if abs((yvec - val)[zero_crossings[0]]) < abs((yvec - val)[zero_crossings[0] + 1]):
        return zero_crossings[0], True
    else:
        return (zero_crossings[0] + 1), True
