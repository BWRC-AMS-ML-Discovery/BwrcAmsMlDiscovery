""" 
# Two Stage Op Amp
"""

import hdl21 as h
from hdl21.prefix import FEMTO
from autockt_shared import OpAmpInput, OpAmpOutput

from ..typing import as_hdl21_paramclass, Hdl21Paramclass
from ..pdk import nmos, pmos
from .params import TbParams
from .tb import simulate, OpAmpTb

Params = Hdl21Paramclass(OpAmpInput)


@h.generator
def TwoStageOpAmp(p: Params) -> h.Module:
    """# Two Stage OpAmp"""

    # FIXME: move to testbench(?)
    cl = h.prefix.Prefixed(number=1e-11)

    # Multiplier functions of the parametric devices
    nbias = lambda x: nmos(m=p.nbias * x)
    ninp = lambda x: nmos(m=p.ninp * x)
    pmoses = lambda x: pmos(m=p.pmoses * x)

    @h.module
    class TwoStageOpAmp:
        # IO Interface
        VDD, VSS = 2 * h.Input()
        ibias = h.Input()
        inp = h.Diff(desc="Differential Input", port=True, role=h.Diff.Roles.SINK)
        out = h.Output()

        # Implementation
        out1 = h.Diff()

        # Input Bias
        miin = nbias(x=1)(d=ibias, g=ibias, s=VSS, b=VSS)
        mbias_inp = nbias(x=2 * p.alpha)(g=ibias, s=VSS, b=VSS)

        # Input Pair
        minp = h.Pair(ninp(x=p.alpha))(d=out1, g=inp, s=mbias_inp.d, b=VSS)

        # Input Stage Load
        # mpld = h.Pair(pmoses(x=p.alpha))(d=out1, g=outn, s=VDD, b=VDD)
        mpld = h.Pair(pmoses(x=p.alpha))(d=out1, g=out1.n, s=VDD, b=VDD)

        # FIXME: hacking out the output stage for the time being

        # Output Stage
        mp3 = pmoses(x=p.beta)(d=out, g=out1.p, s=VDD, b=VDD)
        mn5 = nbias(x=p.beta)(d=out, g=ibias, s=VSS, b=VSS)

        # Load capacitance... FIXME what do we do with ya
        CL = h.Cap(c=cl)(p=out, n=VSS)

        # Miller Compensation Cap
        cc = h.Cap(c=p.cc * FEMTO)(p=out, n=out1.p)

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
