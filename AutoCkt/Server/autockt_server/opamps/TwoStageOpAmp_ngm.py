""" 
# Negative-Gm Load OpAmp
"""

import hdl21 as h
import vlsirtools.spice as vsp

from autockt_shared import TwoStageOpAmpNgmInput, OpAmpOutput

from ..pdk import nmos, pmos


@h.paramclass
class ngmOpAmpParams:
    """Parameter class"""

    wtail1 = h.Param(dtype=int, desc="Width of PMOS Mtial1", default=10)
    wtail2 = h.Param(dtype=int, desc="Width of PMOS Mtial2", default=10)
    wcm = h.Param(dtype=int, desc="width of PMOS Mcm", default=10)
    win = h.Param(dtype=int, desc="width od PMOS Min", default=10)
    wref = h.Param(dtype=int, desc="Width of PMOS Mref", default=10)
    wd1 = h.Param(dtype=int, desc="Width of NMOS Md1", default=10)
    wd = h.Param(dtype=int, desc="Width of NMOS Md", default=10)
    wn_gm = h.Param(dtype=int, desc="Width of NMOS Mn_gm", default=10)
    wtail = h.Param(dtype=int, desc="Width of PMOS Mtial", default=10)
    wtailr = h.Param(dtype=int, desc="Width of PMOS Mtailr", default=10)
    VDD = h.Param(dtype=h.Scalar, desc="VDD voltage", default=1.2)
    Cc = h.Param(dtype=h.Scalar, desc="Cc capacitance", default=1e-14)
    Rf = h.Param(dtype=h.Scalar, desc="Rf resistor", default=100)
    Vcm = h.Param(dtype=h.Scalar, desc="Vcm input voltage", default=0.6)
    Vref = h.Param(dtype=h.Scalar, desc="Vref input voltage", default=0.8)
    ibias = h.Param(dtype=h.Scalar, desc="ibias current", default=2e-6)


@h.generator
def ngmOpAmp(p: ngmOpAmpParams) -> h.Module:
    """# Two stage OpAmp"""

    @h.module
    class DiffOta:
        # IO Interface
        VDD, VSS = 2 * h.Input()
        ibias = h.Input()

        inp = h.Diff(desc="Differential Input", port=True, role=h.Diff.Roles.SINK)
        cm = h.Input()
        ref = h.Input()
        v5 = h.Output()
        v6 = h.Output()

        # Internal Signals
        v1, v2, v3, v4, v7, v8, v9 = h.Signals(7)

        # Input & Output Stage
        Mcm_1 = pmos(m=p.wcm)(d=v3, g=cm, s=VDD, b=VDD)
        Mcm_2 = pmos(m=p.wcm)(d=v9, g=cm, s=VDD, b=VDD)
        Md1_1 = nmos(m=p.wd1)(d=v3, g=v5, s=VSS, b=VSS)
        Md1_2 = nmos(m=p.wd1)(d=v9, g=v6, s=VSS, b=VSS)

        Min_1 = pmos(m=p.win)(d=v7, g=inp.p, s=v5, b=v5)
        Min_2 = pmos(m=p.win)(d=v7, g=inp.n, s=v6, b=v6)
        Md_1 = nmos(m=p.wd1)(d=v5, g=v5, s=VSS, b=VSS)
        Md_2 = nmos(m=p.wd1)(d=v6, g=v6, s=VSS, b=VSS)
        Mn_gm_1 = nmos(m=p.wn_gm)(d=v5, g=v6, s=VSS, b=VSS)
        Mn_gm_2 = nmos(m=p.wn_gm)(d=v6, g=v5, s=VSS, b=VSS)

        # Biasing
        Mref = pmos(m=p.wref)(d=v1, g=ref, s=v2, b=v2)
        Mtailr = pmos(m=p.wtailr)(d=v2, g=v1, s=VDD, b=VDD)
        Mtail = pmos(m=p.wtail)(d=v7, g=v1, s=VDD, b=VDD)
        Mtail1 = pmos(m=p.wtail1)(d=v3, g=v1, s=VDD, b=VDD)
        Mtail2 = pmos(m=p.wtail2)(d=v9, g=v1, s=VDD, b=VDD)

        # Compensation Network
        Cc_1 = h.Cap(c=p.Cc)(p=v4, n=v5)  # Miller Capacitance
        Cc_2 = h.Cap(c=p.Cc)(p=v8, n=v6)
        Rf_1 = h.Res(r=p.Rf)(p=v3, n=v4)
        Rf_2 = h.Res(r=p.Rf)(p=v9, n=v8)

    return DiffOta


def two_stage_op_amp_ngm_sim(inp: TwoStageOpAmpNgmInput) -> OpAmpOutput:
    """
    TwoStageOpAmpNgm Simulation
    """
    opts = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE,
        fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
        rundir="./scratch",  # Set the working directory for the simulation. Uses a temporary directory by default.
    )
    if not vsp.ngspice.available():
        print("ngspice is not available. Skipping simulation.")
        return

    # Run the simulation!
    params = ngmOpAmpParams(
        wtail1=inp.wtail1,
        wtail2=inp.wtail2,
        wcm=inp.wcm,
        win=inp.win,
        wref=inp.wref,
        wd1=inp.wd1,
        wd=inp.wd,
        wn_gm=inp.wn_gm,
        wtail=inp.wtail,
        wtailr=inp.wtailr,
        VDD=inp.VDD,
        Cc=inp.Cc,
        Rf=inp.Rf,
        Vcm=inp.Vcm,
        Vref=inp.Vref,
        ibias=inp.ibias,
    )
    sim_input = ngmOpAmpSim(params)

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

    # And return them as an `OpAmpOutput`
    return OpAmpOutput(
        ugbw=ugbw,
        gain=gain,
        phm=phm,
        ibias=ibias,
    )
