"""
# Latch Example

"""

import sys
from copy import deepcopy
import hdl21 as h
import hdl21.sim as hs
import vlsirtools.spice as vsp
from hdl21.external_module import SpiceType
from hdl21.prefix import µ, NANO
import numpy
import Latch


@h.paramclass
class FFParams:
    """Parameter class"""
    L1 = Latch.LatchParams()
    L2 = Latch.LatchParams()

    # L1 = h.Param(dtype=Latch.LatchParams(), desc="params of Latch1")
    # L2 = h.Param(dtype=Latch.LatchParams(), desc="params of Latch2")


@h.generator
def FFgen(p: FFParams) -> h.Module:
    """# FF """

    @h.module
    class FF:
        # IO Interface
        VDD, VSS = 2 * h.Input()
        CLK, CKB = 2 * h.Input()
        D = h.Input()
        Q = h.Output()

        intermediate_signal = h.Signal()

        # Sampling latch
        Sampling_latch = Latch.LatchGen(p.L1)(VDD=VDD, VSS=VSS, CLK=CKB, CKB=CLK, D=D, Q=intermediate_signal)

        # Holding latch
        Holding_latch  = Latch.LatchGen(p.L2)(VDD=VDD, VSS=VSS, CLK=CLK, CKB=CKB, D=intermediate_signal, Q=Q)


    return FF

@hs.sim

# FIXME: Need to get
# (i) settling time;
# (ii) power consumption


# class MosDcopSim:
#     """# Mos Dc Operating Point Simulation Input"""
#     # def __init__(params):


#     @h.module
#     class Tb:
#         """# Basic Mos Testbench"""

#         VSS = h.Port()  # The testbench interface: sole port VSS
#         vdc = h.Vdc(dc=1.2)(n=VSS)  # A DC voltage source
#         dcin = h.Diff()
#         sig_out = h.Signal()
#         i_bias = h.Signal()
#         sig_p = h.Vdc(dc=0.6, ac=0.5)(p=dcin.p,n=VSS)
#         sig_n = h.Vdc(dc=0.6, ac=-0.5)(p=dcin.n,n=VSS)
#         Isource = h.Isrc(dc = 3e-5)(p = vdc.p, n = i_bias)

#         inst=Latch()(VDD=vdc.p, VSS=VSS, ibias=i_bias, inp=dcin, out=sig_out)

#     # Simulation Stimulus
#     op = hs.Op()
#     ac = hs.Ac(sweep=hs.LogSweep(1e1, 1e10, 10))
#     mod = hs.Include("../45nm_bulk.txt")



def main():
    h.netlist(FFGen(), sys.stdout)
    # h.netlist(LatchGen(LatchParams()), sys.stdout)


if __name__ == "__main__":
    main()
