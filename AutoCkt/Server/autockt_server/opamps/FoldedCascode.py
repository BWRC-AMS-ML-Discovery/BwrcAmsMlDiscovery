""" 
# Folded Cascode OpAmp
"""

import hdl21 as h
import vlsirtools.spice as vsp

from autockt_shared import FoldedCascodeInput, OpAmpOutput

# Local Imports
from ..pdk import nmos, pmos


@h.paramclass
class FoldedCascodeParams:
    """Parameter class"""

    w1_2 = h.Param(dtype=int, desc="Width of M1/2", default=10)
    w5_6 = h.Param(dtype=int, desc="Width of M5/6", default=10)
    w7_8 = h.Param(dtype=int, desc="Width of M7/8", default=10)
    w9_10 = h.Param(dtype=int, desc="width of M9/10", default=10)
    w11_12 = h.Param(dtype=int, desc="Width of M11/12", default=10)
    w13_14 = h.Param(dtype=int, desc="Width of M13/14", default=10)
    w15_16 = h.Param(dtype=int, desc="Width of M15/16", default=10)
    w17 = h.Param(dtype=int, desc="Width of M17", default=10)
    w18 = h.Param(dtype=int, desc="width of M18", default=10)

    cl = h.Param(dtype=h.Scalar, desc="cl capacitance", default=1e-14)
    cc = h.Param(dtype=h.Scalar, desc="cc capacitance", default=1e-14)
    rc = h.Param(dtype=h.Scalar, desc="rc resistor", default=100)
    VDD = h.Param(dtype=h.Scalar, desc="VDD voltage", default=1.2)

    wb0 = h.Param(dtype=int, desc="Width of MB0 ", default=10)
    wb1 = h.Param(dtype=int, desc="Width of MB1 ", default=10)
    wb2 = h.Param(dtype=int, desc="Width of MB2 ", default=10)
    wb3 = h.Param(dtype=int, desc="Width of MB3 ", default=10)
    wb4 = h.Param(dtype=int, desc="Width of MB4 ", default=10)
    wb5 = h.Param(dtype=int, desc="Width of MB5 ", default=10)
    wb6 = h.Param(dtype=int, desc="Width of MB6 ", default=10)
    wb7 = h.Param(dtype=int, desc="Width of MB7 ", default=10)
    wb8 = h.Param(dtype=int, desc="Width of MB8 ", default=10)
    wb9 = h.Param(dtype=int, desc="Width of MB9 ", default=10)
    wb10 = h.Param(dtype=int, desc="Width of MB10", default=10)
    wb11 = h.Param(dtype=int, desc="Width of MB11", default=10)
    wb12 = h.Param(dtype=int, desc="Width of MB12", default=10)
    wb13 = h.Param(dtype=int, desc="Width of MB13", default=10)
    wb14 = h.Param(dtype=int, desc="Width of MB14", default=10)
    wb15 = h.Param(dtype=int, desc="Width of MB15", default=10)
    wb16 = h.Param(dtype=int, desc="Width of MB16", default=10)
    wb17 = h.Param(dtype=int, desc="Width of MB17", default=10)
    wb18 = h.Param(dtype=int, desc="Width of MB18", default=10)
    wb19 = h.Param(dtype=int, desc="Width of MB19", default=10)

    ibias = h.Param(dtype=h.Scalar, desc="ibias current", default=30e-6)
    Vcm = h.Param(dtype=h.Scalar, desc="Vcm", default=1)


@h.generator
def FoldedCascodeGen(p: FoldedCascodeParams) -> h.Module:
    """# Two stage OpAmp"""

    @h.module
    class FoldedCascode:
        # IO Interface
        VDD, VSS = 2 * h.Input()
        ibias = h.Input()

        inp = h.Diff(desc="Differential Input", port=True, role=h.Diff.Roles.SINK)

        # ref = h.Input()
        v9 = h.Output()
        v10 = h.Output()
        # v_nmbias = h.Input()
        # v_nbbias = h.Input()
        # v_bbias = h.Input()
        v_cm = h.Input()
        # v_cs = h.Input()
        v_cs = h.Signal()

        v_nmbias, v_nbbias, v_bbias, v_pcas = h.Signals(4)

        # Internal Signals
        v1, v2, v3, v4, v5, v6, v7, v8, v11, v12 = h.Signals(10)

        # Input Stage
        M1 = nmos(m=p.w1_2)(d=v11, g=inp.p, s=v1, b=v1)
        M2 = nmos(m=p.w1_2)(d=v12, g=inp.n, s=v1, b=v1)
        M17 = nmos(m=p.w17)(d=v1, g=v_nmbias, s=v2, b=v2)
        M18 = nmos(m=p.w18)(d=v2, g=v_nbbias, s=VSS, b=VSS)

        M5 = pmos(m=p.w5_6)(d=v11, g=v_bbias, s=VDD, b=VDD)
        M6 = pmos(m=p.w5_6)(d=v12, g=v_bbias, s=VDD, b=VDD)

        M7 = pmos(m=p.w7_8)(d=v5, g=v_cm, s=v11, b=v11)
        M8 = pmos(m=p.w7_8)(d=v6, g=v_cm, s=v12, b=v12)
        M9 = nmos(m=p.w9_10)(d=v5, g=v_nmbias, s=v3, b=v3)
        M10 = nmos(m=p.w9_10)(d=v6, g=v_nmbias, s=v4, b=v4)
        M11 = nmos(m=p.w11_12)(d=v3, g=v_nbbias, s=VSS, b=VSS)
        M12 = nmos(m=p.w11_12)(d=v4, g=v_nbbias, s=VSS, b=VSS)

        # Output Stage
        M13 = pmos(m=p.w13_14)(d=v9, g=v_cs, s=VDD, b=VDD)
        M14 = pmos(m=p.w13_14)(d=v10, g=v_cs, s=VDD, b=VDD)
        M15 = nmos(m=p.w15_16)(d=v9, g=v5, s=VSS, b=VSS)
        M16 = nmos(m=p.w15_16)(d=v10, g=v6, s=VSS, b=VSS)

        # Compensation Network
        Cc_1 = h.Cap(c=p.cc)(p=v9, n=v7)  # Miller Capacitance
        Cc_2 = h.Cap(c=p.cc)(p=v10, n=v8)
        Rc_1 = h.Res(r=p.rc)(p=v7, n=v5)
        Rc_2 = h.Res(r=p.rc)(p=v8, n=v6)

        # Bias generator
        vbias2 = h.Signal()
        b1, b2, b3, b4, b5, b6, b7, b8, b9 = h.Signals(9)

        MB0 = nmos(m=p.wb0)(d=ibias, g=ibias, s=vbias2, b=vbias2)
        MB1 = nmos(m=p.wb1)(d=v_pcas, g=ibias, s=b1, b=b1)
        MB2 = nmos(m=p.wb2)(d=vbias2, g=vbias2, s=VSS, b=VSS)
        MB3 = nmos(m=p.wb3)(d=b1, g=vbias2, s=VSS, b=VSS)

        MB4 = pmos(m=p.wb4)(d=v_bbias, g=v_bbias, s=VDD, b=VDD)
        MB5 = pmos(m=p.wb5)(d=v_pcas, g=v_pcas, s=v_bbias, b=v_bbias)
        MB6 = pmos(m=p.wb6)(d=b2, g=v_bbias, s=VDD, b=VDD)
        MB7 = pmos(m=p.wb7)(d=b3, g=v_pcas, s=b2, b=b2)

        MB8 = nmos(m=p.wb8)(d=b3, g=v_nmbias, s=b4, b=b4)
        MB9 = nmos(m=p.wb9)(d=b4, g=v_nmbias, s=b5, b=b5)
        MB10 = nmos(m=p.wb10)(d=b5, g=v_nmbias, s=b6, b=b6)
        MB11 = nmos(m=p.wb11)(d=b6, g=v_nmbias, s=VSS, b=VSS)

        MB12 = pmos(m=p.wb12)(d=b7, g=v_bbias, s=VDD, b=VDD)
        MB13 = pmos(m=p.wb13)(d=v_nbbias, g=v_pcas, s=b7, b=b7)
        MB14 = nmos(m=p.wb14)(
            d=v_nbbias, g=v_nmbias, s=b8, b=b8
        )  # TODO: check where the gate should connect to
        MB15 = nmos(m=p.wb15)(d=b8, g=v_nbbias, s=VSS, b=VSS)

        MB16 = pmos(m=p.wb16)(d=v_cs, g=v_cs, s=VDD, b=VDD)
        MB14 = nmos(m=p.wb14)(d=v_cs, g=vbias2, s=b9, b=b9)
        MB15 = nmos(m=p.wb15)(d=b9, g=vbias2, s=VSS, b=VSS)

    return FoldedCascode


def folded_cascode_sim(inp: FoldedCascodeInput) -> OpAmpOutput:
    """
    FoldedCascode Simulation
    """
    opts = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE,
        fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
        rundir="./scratch",  # Set the working directory for the simulation. Uses a temporary directory by default.
    )
    if not vsp.ngspice.available():
        print("ngspice is not available. Skipping simulation.")
        return

    params = FoldedCascodeParams(
        w1_2=inp.w1_2,
        w5_6=inp.w5_6,
        w7_8=inp.w7_8,
        w9_10=inp.w9_10,
        w11_12=inp.w11_12,
        w13_14=inp.w13_14,
        w15_16=inp.w15_16,
        w17=inp.w17,
        w18=inp.w18,
        # VDD=inp.VDD,
        cl=inp.cl,
        cc=inp.cc,
        rc=inp.rc,
        wb0=inp.wb0,
        wb1=inp.wb1,
        wb2=inp.wb2,
        wb3=inp.wb3,
        wb4=inp.wb4,
        wb5=inp.wb5,
        wb6=inp.wb6,
        wb7=inp.wb7,
        wb8=inp.wb8,
        wb9=inp.wb9,
        wb10=inp.wb10,
        wb11=inp.wb11,
        wb12=inp.wb12,
        wb13=inp.wb13,
        wb14=inp.wb14,
        wb15=inp.wb15,
        wb16=inp.wb16,
        wb17=inp.wb17,
        wb18=inp.wb18,
        wb19=inp.wb19,
        ibias=inp.ibias,
        Vcm=inp.Vcm,
    )

    # Run the simulation!
    results = FoldedCascodeSim(params).run(opts)

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
