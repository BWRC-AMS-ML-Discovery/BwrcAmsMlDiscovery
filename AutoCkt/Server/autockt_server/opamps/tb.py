""" 
# Testbench & Test Utilities
"""

from typing import Optional
import numpy

import hdl21 as h
import hdl21.sim as hs
import vlsirtools.spice as vsp

from autockt_shared import OpAmpOutput

from .params import TbParams
from ..pdk import SPICE_MODEL_45NM_BULK_PATH


@h.generator
def OpAmpTb(params: TbParams) -> h.Module:
    """# Generic Op-Amp Testbench"""

    vicm = params.vicm or params.VDD / 2

    @h.module
    class OpAmpTb:
        VSS = h.Port()  # The testbench interface: sole port VSS

        # Drive VDD
        VDD, sig_out, ibias = 3 * h.Signal()
        vdc = h.Vdc(dc=params.VDD)(p=VDD, n=VSS)
        inp = h.Diff()
        sig_p = h.Vdc(dc=vicm, ac=+0.5)(p=inp.p, n=VSS)
        sig_n = h.Vdc(dc=vicm, ac=-0.5)(p=inp.n, n=VSS)
        Isource = h.Isrc(dc=params.ibias)(p=VSS, n=ibias)

        # The Op-Amp DUT
        inst = params.dut(VDD=VDD, VSS=VSS, ibias=ibias, inp=inp, out=sig_out)

    return OpAmpTb


def OpAmpSim(tbmodule: h.Instantiable) -> h.sim.Sim:
    """# Op Amp Simulation Input"""

    @hs.sim
    class OpAmpSim:
        """# OpAmp Simulation Input"""

        # The testbench
        tb = tbmodule

        # Simulation Stimulus
        op = hs.Op()
        ac = hs.Ac(sweep=hs.LogSweep(start=1, stop=1e10, npts=10))

        # Model Includes
        mod = hs.Include(SPICE_MODEL_45NM_BULK_PATH)

    return OpAmpSim


def simulate(tbmodule: h.Instantiable) -> OpAmpOutput:
    """# Simulate an op-amp testbench, parse and return its metrics."""

    # Apply `params` to generate the test

    # Get our simulation input
    sim_input = OpAmpSim(tbmodule)

    if not vsp.ngspice.available():
        raise RuntimeError(f"No ngspice available")

    opts = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE,
        fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
        rundir="./scratch",  # Set the working directory for the simulation. Uses a temporary directory by default.
    )

    # Run the simulation
    results = sim_input.run(opts)

    # And extract our metrics/ outputs from the results
    return extract_outputs(results)


def find_dc_gain(vout: numpy.array) -> float:
    return numpy.abs(vout)[0]


def find_ugbw(freq: numpy.array, vout: numpy.array) -> float:
    gain = numpy.abs(vout)
    ugbw_index = _get_best_crossing(gain, val=1)
    if ugbw_index is None:
        return freq[0]  # None found; return the minimum frequency
    return freq[ugbw_index]


def find_phm(freq: numpy.array, vout: numpy.array) -> float:
    gain = numpy.abs(vout)
    phase = numpy.angle(vout, deg=False)
    phase = numpy.unwrap(phase)  # unwrap the discontinuity
    phase = numpy.rad2deg(phase)  # convert to degrees

    ugbw_index = _get_best_crossing(gain, val=1)
    if ugbw_index is None:
        return -180

    if phase[ugbw_index] > 0:
        return phase[ugbw_index] - 180
    return phase[ugbw_index] + 180


def _get_best_crossing(yvec: numpy.array, val: float) -> Optional[int]:
    """
    Get the index of the "best" crossing of `yvec` across `val`.
    Returns None if no sufficiently good crossing (no crossing at all?) is found.
    FIXME @HarryYanH: what do you mean "best"?
    the value which is closest to our threshold
    """

    zero_crossings = numpy.where(numpy.diff(numpy.sign(yvec - val)))[0]
    if len(zero_crossings) == 0:
        return None

    # FIXME @HarryYanH: what is this comparison here?
    if abs((yvec - val)[zero_crossings[0]]) < abs((yvec - val)[zero_crossings[0] + 1]):
        return zero_crossings[0]
    return zero_crossings[0] + 1


def extract_outputs(results: h.sim.SimResult) -> OpAmpOutput:
    """# Extract our metrics from `results`"""

    ac_result = results["ac"]
    sig_out = ac_result.data["v(xtop.sig_out)"]

    # FIXME: @HarryYanH: why are these all multiplied by 2?
    # Because the amplitude of our AC signal is 0.5, *2 here means /0.5
    gain = find_dc_gain(2 * sig_out)
    ugbw = find_ugbw(ac_result.freq, 2 * sig_out)
    phm = find_phm(ac_result.freq, 2 * sig_out)

    # Get the supply current from the DC operating point results
    op_result = results["op"]
    idd = numpy.abs(op_result.data["i(v.xtop.vvdc)"])

    # And return them as an `OpAmpOutput`
    return OpAmpOutput(
        ugbw=ugbw,
        gain=gain,
        phm=phm,
        ibias=idd,
    )
