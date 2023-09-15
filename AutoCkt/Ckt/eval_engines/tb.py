""" 
# Testbench & Test Utilities
"""

import numpy

import hdl21 as h
import hdl21.sim as hs
import vlsirtools.spice as vsp

from autockt_shared import OpAmpOutput

from .params import TbParams
from .pdk import SPICE_MODEL_45NM_BULK_PATH


def OpAmpSim(params: TbParams) -> h.sim.Sim:
    """# Op Amp Simulation Input"""

    @hs.sim
    class OpAmpSim:
        """# OpAmp Simulation Input"""

        @h.module
        class Tb:
            """# Op-Amp Testbench"""

            VSS = h.Port()  # The testbench interface: sole port VSS

            vdc = h.Vdc(dc=params.VDD)(n=VSS)  # A DC voltage source
            dcin = h.Diff()
            sig_out = h.Signal()
            i_bias = h.Signal()
            sig_p = h.Vdc(dc=params.VDD / 2, ac=0.5)(p=dcin.p, n=VSS)
            sig_n = h.Vdc(dc=params.VDD / 2, ac=-0.5)(p=dcin.n, n=VSS)
            Isource = h.Isrc(dc=params.ibias)(p=vdc.p, n=i_bias)

            # The Op-Amp DUT
            inst = params.dut(VDD=vdc.p, VSS=VSS, ibias=i_bias, inp=dcin, out=sig_out)

        # Simulation Stimulus
        op = hs.Op()
        ac = hs.Ac(sweep=hs.LogSweep(1e1, 1e10, 10))

        # Model Includes
        mod = hs.Include(SPICE_MODEL_45NM_BULK_PATH)

    # Add any extra simulator control elements
    ctrls = params.ctrls or []
    for ctrl in ctrls:
        OpAmpSim.add(ctrl)

    return OpAmpSim


def simulate(params: TbParams) -> OpAmpOutput:
    """# FIXME DOCSTRING PLZ"""

    # Get our simulation input
    sim_input = OpAmpSim(params=params)

    opts = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE,
        fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
        rundir="./scratch",  # Set the working directory for the simulation. Uses a temporary directory by default.
    )

    # Run the simulation
    results = sim_input.run(opts)

    # And extract our metrics/ outputs from the results
    return extract_outputs(results)


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


def extract_outputs(results: h.sim.SimResult) -> OpAmpOutput:
    """# Extract our metrics from `results`"""

    ac_result = results["ac"]
    sig_out = ac_result.data["xtop.sig_out"]
    gain = find_dc_gain(2 * sig_out)
    ugbw = find_ugbw(ac_result.freq, 2 * sig_out)
    phm = find_phm(ac_result.freq, 2 * sig_out)
    idd = ac_result.data["xtop.vdc:p"]
    ibias = find_I_vdd(idd)

    # And return them as an `OpAmpOutput`
    return OpAmpOutput(
        ugbw=ugbw,
        gain=gain,
        phm=phm,
        ibias=ibias,
    )
