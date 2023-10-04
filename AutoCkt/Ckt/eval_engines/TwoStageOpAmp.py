""" 
# Two Stage Op Amp
"""

import hdl21 as h
from autockt_shared import OpAmpInput, OpAmpOutput, auto_ckt_sim_hdl21

from .tb import simulate
from .params import TbParams
from .pdk import nmos, pmos


@h.generator
def OpAmp(p: hdl21_paramclass[OpAmpInput]) -> h.Module:
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
    # FIXME the names of the params are not the same, need to change above
    params = as_hdl21_paramclass(inp)

    # Create a testbench, simulate it, and return the metrics!
    opamp = OpAmp(params)
    tbparams = TbParams(dut=opamp, VDD=params.VDD, ibias=params.ibias)
    return simulate(tbparams)


@auto_ckt_sim_hdl21.impl
def auto_ckt_sim_hdl21(inp: OpAmpInput) -> OpAmpOutput:
    """# Our RPC Handler"""
    return opamp_inner(inp)
