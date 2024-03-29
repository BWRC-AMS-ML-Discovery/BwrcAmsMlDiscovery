""" 
# Two Stage Op Amp
"""

import hdl21 as h
from autockt_shared import OpAmpInput, OpAmpOutput, auto_ckt_sim_hdl21

from ..typing import as_hdl21_paramclass, Hdl21Paramclass
from ..pdk import nmos, pmos
from .params import TbParams
from .tb import simulate, OpAmpTb

Params = Hdl21Paramclass(OpAmpInput)


@h.generator
def TwoStageOpAmp(p: Params) -> h.Module:
    """# Two Stage OpAmp"""

    cl = h.prefix.Prefixed(number=1e-11)

    @h.module
    class TwoStageOpAmp:

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

    return TwoStageOpAmp


def opamp_inner(inp: OpAmpInput) -> OpAmpOutput:
    """# Two-Stage OpAmp RPC Implementation"""

    # Convert `inp` into the generator's parameters
    params = as_hdl21_paramclass(inp)

    VDD = h.prefix.Prefixed(number=1.2)
    ibias = h.prefix.Prefixed(number=3e-5)

    # Create a testbench, simulate it, and return the metrics!
    opamp = TwoStageOpAmp(params)
    tbparams = TbParams(
        dut=opamp,
        VDD=VDD,
        ibias=ibias,
    )
    tbmodule = OpAmpTb(tbparams)
    return simulate(tbmodule)
