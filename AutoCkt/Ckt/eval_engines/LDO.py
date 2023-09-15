""" 
# LDO

This LDO is based on the schematic of Fig2.10 in Keertana's article.
Here is url for the article: 
https://www2.eecs.berkeley.edu/Pubs/TechRpts/2022/EECS-2022-27.pdf

"""

import sys
import os
from pathlib import Path
from copy import deepcopy
import hdl21 as h
import hdl21.sim as hs
import vlsirtools.spice as vsp
from hdl21.external_module import SpiceType
from hdl21.prefix import µ, NANO
import numpy

CURRENT_PATH = Path(os.path.dirname(os.path.abspath(__file__)))
SPICE_MODEL_45NM_BULK_PATH = CURRENT_PATH / "45nm_bulk.txt"

""" 
Create a small "PDK" consisting of an externally-defined Nmos and Pmos transistor. 
Real versions will have some more parameters; these just have multiplier "m". 
"""


@h.paramclass
class MosParams:
    m = h.Param(dtype=int, desc="Transistor Multiplier")


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
class LDO_Params:
    """Parameter class"""

    w1 = h.Param(dtype=int, desc="Width of m1", default=10)
    w2 = h.Param(dtype=int, desc="Width of m2", default=10)
    w3 = h.Param(dtype=int, desc="Width of m3", default=10)
    w4 = h.Param(dtype=int, desc="Width of m4", default=10)
    w5 = h.Param(dtype=int, desc="Width of m5", default=10)
    w6 = h.Param(dtype=int, desc="Width of m6", default=10)
    w7r = h.Param(dtype=int, desc="Width of m7r", default=10)
    w8 = h.Param(dtype=int, desc="Width of m8", default=10)
    wc = h.Param(dtype=int, desc="Width of mc", default=10)
    w10 = h.Param(dtype=int, desc="Width of m10", default=10)
    wpass = h.Param(dtype=int, desc="Width of mpass", default=10)
    VDD = h.Param(dtype=h.Scalar, desc="VDD voltage", default=1.2)
    Cc = h.Param(dtype=h.Scalar, desc="Cc capacitance", default=1e-11)
    Cf1 = h.Param(dtype=h.Scalar, desc="Cf1 capacitance", default=1e-11)
    Cf2 = h.Param(dtype=h.Scalar, desc="Cf2 capacitance", default=1e-11)
    Rrf1 = h.Param(dtype=h.Scalar, desc="Rrf1 resistance", default=1e6)
    Rrf2 = h.Param(dtype=h.Scalar, desc="Rrf2 reeistance", default=4e6)
    ibias = h.Param(dtype=h.Scalar, desc="ibias current", default=3e-5)


@h.generator
def LDO_1(p: LDO_Params) -> h.Module:
    """# LDO"""

    @h.module
    class LDO:
        # IO Interface
        VDD, VSS = 2 * h.Input()
        ibias = h.Input()
        vref = h.Input()

        vout = h.Output()

        # Internal Signals
        v1, v2, v3, v4, v5, v6, vfb = h.Signals(7)

        # EA
        m1 = nmos(m=p.w1)(d=v1, g=vfb, s=v3, b=v3)  # vfb
        m2 = nmos(m=p.w2)(d=v2, g=vref, s=v3, b=v3)  # vref
        m3 = pmos(m=p.w3)(d=v1, g=v1, s=VDD, b=VDD)  # Current Mirror
        m4 = pmos(m=p.w4)(d=v2, g=v1, s=VDD, b=VDD)  # Current Mirror
        mc = nmos(m=p.wc)(d=v1, g=vref, s=v4, b=v4)
        m8 = nmos(m=p.w8)(d=v2, g=vref, s=v5, b=v5)

        #
        mpass = pmos(m=p.wpass)(d=vout, g=v2, s=VDD, b=VDD)

        # Current Biasing
        m5 = nmos(m=p.w5)(d=v3, g=v6, s=VSS, b=VSS)  # Bias Current
        m6 = nmos(m=p.w6)(d=v6, g=v6, s=VSS, b=VSS)  # Current Source Bias
        m7r = nmos(m=p.w7r)(d=v4, g=v6, s=VSS, b=VSS)
        m10 = nmos(m=p.w10)(d=v5, g=v6, s=VSS, b=VSS)

        # Compensation Network
        Cc = h.Cap(c=p.Cc)(p=v5, n=vout)  # Miller Capacitance

        # Feedback
        Cf1 = h.Cap(c=p.Cf1)(p=vout, n=vfb)
        Cf2 = h.Cap(c=p.Cf2)(p=vfb, n=VSS)
        Rf1 = h.Res(r=p.Rrf1)(p=vout, n=vfb)
        Rf2 = h.Res(r=p.Rrf2)(p=vfb, n=VSS)

    return LDO


@h.module
class CapCell:
    """# Compensation Capacitor Cell"""

    p, n, VDD, VSS = 4 * h.Port()
    # FIXME: internal content! Using tech-specific `ExternalModule`s


@h.module
class ResCell:
    """# Compensation Resistor Cell"""

    p, n, sub = 3 * h.Port()
    # FIXME: internal content! Using tech-specific `ExternalModule`s


@h.module
class Compensation:
    """# Single Ended RC Compensation Network"""

    a, b, VDD, VSS = 4 * h.Port()
    r = ResCell(p=a, sub=VDD)
    c = CapCell(p=r.n, n=b, VDD=VDD, VSS=VSS)


def LDO_Sim(params: LDO_Params) -> h.sim.Sim:
    """# Op Amp Simulation Input"""

    @hs.sim
    class MosDcopSim:
        """# Mos Dc Operating Point Simulation Input"""

        @h.module
        class Tb:
            """# Basic Mos Testbench"""

            VSS = h.Port()  # The testbench interface: sole port VSS
            vdc = h.Vdc(dc=params.VDD)(n=VSS)  # A DC voltage source
            dcin = h.Diff()
            sig_out = h.Signal()
            i_bias = h.Signal()
            sig_ac = h.Vdc(dc=1.8, ac=0.3)(n=vdc.p)
            Isource = h.Isrc(dc=params.ibias)(p=vdc.p, n=i_bias)
            dangling = h.Signal()

            inst = LDO_1(params)(
                VDD=sig_ac.p, VSS=VSS, ibias=i_bias, vref=dangling, vout=sig_out
            )

        # Simulation Stimulus
        op = hs.Op()
        ac = hs.Ac(sweep=hs.LogSweep(1e1, 1e10, 10))
        mod = hs.Include(SPICE_MODEL_45NM_BULK_PATH)

    return MosDcopSim


def main():
    # h.netlist(OpAmp(), sys.stdout)

    opts = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE,
        fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
        rundir="./scratch",  # Set the working directory for the simulation. Uses a temporary directory by default.
    )
    if not vsp.ngspice.available():
        print("ngspice is not available. Skipping simulation.")
        return

    # Run the simulation!
    params = LDO_Params()
    results = LDO_Sim(params).run(opts)

    print(
        "Gain:            "
        + str(find_dc_gain(2 * results["ac"].data["v(xtop.sig_out)"]))
    )
    print(
        "UGBW:            "
        + str(find_ugbw(results["ac"].freq, 2 * results["ac"].data["v(xtop.sig_out)"]))
    )
    print(
        "Phase margin:    "
        + str(find_phm(results["ac"].freq, 2 * results["ac"].data["v(xtop.sig_out)"]))
    )
    print("Ivdd:            " + str(find_I_vdd(results["ac"].data["i(v.xtop.vvdc)"])))


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


if __name__ == "__main__":
    main()
