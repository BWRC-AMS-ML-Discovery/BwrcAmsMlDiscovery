""" 
# Two Stage Op Amp
"""

import hdl21 as h
from autockt_shared import OpAmpInput, OpAmpOutput, auto_ckt_sim_hdl21

from .tb import simulate
from .params import TbParams
from .pdk import nmos, pmos
from .typing import as_hdl21_paramclass, Hdl21Paramclass


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
def OpAmp(p: Hdl21Paramclass(OpAmpInput)) -> h.Module:
    """# Two stage OpAmp"""

    @h.module
    class DiffOta:
        cl = h.prefix.Prefixed(number=1e-11)

        # IO Interface
        VDD, VSS = 2 * h.Input()
        ibias = h.Input()

        inp = h.Diff(desc="Differential Input", port=True, role=h.Diff.Roles.SINK)
        out = h.Output()

        # Internal Signals
        net3, net4, net5 = h.Signals(3)

        # Input Stage
        mp1 = pmos(m=p.mp1)(
            d=net4, g=net4, s=VDD, b=VDD
        )  # Current mirror within the input stage
        mp2 = pmos(m=p.mp1)(
            d=net5, g=net4, s=VDD, b=VDD
        )  # Current mirror within the input stage
        mn1 = nmos(m=p.mn1)(d=net4, g=inp.n, s=net3, b=net3)  # Input MOS pair
        mn2 = nmos(m=p.mn1)(d=net5, g=inp.p, s=net3, b=net3)  # Input MOS pair
        mn3 = nmos(m=p.mn3)(d=net3, g=ibias, s=VSS, b=VSS)  # Mirrored current source

        # Output Stage
        mp3 = pmos(m=p.mp3)(d=out, g=net5, s=VDD, b=VDD)  # Output inverter
        mn5 = nmos(m=p.mn5)(d=out, g=ibias, s=VSS, b=VSS)  # Output inverter
        CL = h.Cap(c=cl)(p=out, n=VSS)  # Load capacitance

        # Biasing
        mn4 = nmos(m=p.mn4)(
            d=ibias, g=ibias, s=VSS, b=VSS
        )  # Current mirror co-operating with mn3

        # Compensation Network
        Cc = h.Cap(c=p.cc)(p=net5, n=out)  # Miller Capacitance

    return DiffOta


def opamp_inner(inp: OpAmpInput) -> OpAmpOutput:
    """# Two-Stage OpAmp RPC Implementation"""

    # Convert our input into `OpAmpParams`
    params = as_hdl21_paramclass(inp)

    VDD = h.prefix.Prefixed(number=1.2)
    ibias = h.prefix.Prefixed(number=3e-5)

    # Create a testbench, simulate it, and return the metrics!
    opamp = OpAmp(params)
    tbparams = TbParams(dut=opamp, VDD=params.VDD, ibias=params.ibias)
    return simulate(tbparams)
