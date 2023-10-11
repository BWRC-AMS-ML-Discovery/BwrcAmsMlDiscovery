""" 
# Two Stage Op Amp
"""

import hdl21 as h
from autockt_shared import OpAmpInput, OpAmpOutput, auto_ckt_sim_hdl21

from .tb import simulate
from .params import TbParams
from .pdk import nmos, pmos


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
    class DiffOta:
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

    return DiffOta


def opamp_inner(inp: OpAmpInput) -> OpAmpOutput:
    """# Two-Stage OpAmp RPC Implementation"""

    # Convert our input into `OpAmpParams`
    # FIXME: @king-han gonna clean all this conversion stuff up
    params = OpAmpParams(
        wp1=inp.mp1,
        wn1=inp.mn1,
        wp3=inp.mp3,
        wn3=inp.mn3,
        wn4=inp.mn4,
        wn5=inp.mn5,
        Cc=inp.cc,
        # FIXME Extra, don't need?
        wp2=inp.mp1,
        wn2=inp.mn1,
    )

    # Create a testbench, simulate it, and return the metrics!
    opamp = OpAmp(params)
    tbparams = TbParams(dut=opamp, VDD=params.VDD, ibias=params.ibias)
    return simulate(tbparams)
