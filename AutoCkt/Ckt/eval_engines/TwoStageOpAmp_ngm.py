""" 
# FIXME: WRITE AN ACTUAL DOC COMMENT

# Two Stage Op Amp with negative gm

"""


import hdl21 as h
from autockt_shared import TwoStageOpAmpNgmInput, OpAmpOutput, auto_ckt_sim_hdl21

from .tb import simulate
from .params import TbParams
from .pdk import nmos, pmos

# from .pdk import SPICE_MODEL_45NM_BULK_PATH, nmos, pmos


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
        # cm = h.Input()
        # ref = h.Input()
        # v5 = h.Output()
        # v6 = h.Output()
        cm = h.Signal()
        ref = h.Signal()
        cm_vsource = h.Vdc(dc=p.Vcm)(p=cm, n=VSS)
        ref_vsource = h.Vdc(dc=p.Vref)(p=ref, n=VSS)
        out = h.Output()
        v6 = h.Signal()

        # Internal Signals
        v1, v2, v3, v4, v7, v8, v9 = h.Signals(7)

        # Input & Output Stage
        Mcm_1 = pmos(m=p.wcm)(d=v3, g=cm, s=VDD, b=VDD)
        Mcm_2 = pmos(m=p.wcm)(d=v9, g=cm, s=VDD, b=VDD)
        Md1_1 = nmos(m=p.wd1)(d=v3, g=out, s=VSS, b=VSS)
        Md1_2 = nmos(m=p.wd1)(d=v9, g=v6, s=VSS, b=VSS)

        Min_1 = pmos(m=p.win)(d=v7, g=inp.p, s=out, b=out)
        Min_2 = pmos(m=p.win)(d=v7, g=inp.n, s=v6, b=v6)
        Md_1 = nmos(m=p.wd1)(d=out, g=out, s=VSS, b=VSS)
        Md_2 = nmos(m=p.wd1)(d=v6, g=v6, s=VSS, b=VSS)
        Mn_gm_1 = nmos(m=p.wn_gm)(d=out, g=v6, s=VSS, b=VSS)
        Mn_gm_2 = nmos(m=p.wn_gm)(d=v6, g=out, s=VSS, b=VSS)

        # Biasing
        Mref = pmos(m=p.wref)(d=v1, g=ref, s=v2, b=v2)
        Mtailr = pmos(m=p.wtailr)(d=v2, g=v1, s=VDD, b=VDD)
        Mtail = pmos(m=p.wtail)(d=v7, g=v1, s=VDD, b=VDD)
        Mtail1 = pmos(m=p.wtail1)(d=v3, g=v1, s=VDD, b=VDD)
        Mtail2 = pmos(m=p.wtail2)(d=v9, g=v1, s=VDD, b=VDD)

        # Compensation Network
        Cc_1 = h.Cap(c=p.Cc)(p=v4, n=out)  # Miller Capacitance
        Cc_2 = h.Cap(c=p.Cc)(p=v8, n=v6)
        Rf_1 = h.Res(r=p.Rf)(p=v3, n=v4)
        Rf_2 = h.Res(r=p.Rf)(p=v9, n=v8)

    return DiffOta


def ngm_opamp_inner(inp: TwoStageOpAmpNgmInput) -> OpAmpOutput:
    """# Two-Stage OpAmp RPC Implementation"""

    # Convert our input into `OpAmpParams`
    # FIXME: @king-han gonna clean all this conversion stuff up
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

    # Create a testbench, simulate it, and return the metrics!
    opamp = ngmOpAmp(params)
    tbparams = TbParams(dut=opamp, VDD=params.VDD, ibias=params.ibias)
    return simulate(tbparams)


# @auto_ckt_sim_hdl21.impl
# def auto_ckt_sim_hdl21(inp: TwoStageOpAmpNgmInput) -> OpAmpOutput:
#     """# Our RPC Handler"""
#     return opamp_inner(inp)
