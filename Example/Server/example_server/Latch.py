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


""" 
Create a small "PDK" consisting of an externally-defined Nmos and Pmos transistor. 
Real versions will have some more parameters; these just have multiplier "m". 
"""


@h.paramclass
class MosParams:
    m = h.Param(dtype=int, desc="Transistor Multiplier")

@h.paramclass
class PdkMosParams:
    w = h.Param(dtype=h.Scalar, desc="Width in resolution units", default=0.5 * µ)
    l = h.Param(dtype=h.Scalar, desc="Length in resolution units", default=90 * NANO)
    nf = h.Param(dtype=h.Scalar, desc="Number of parallel fingers", default=1)
    m = h.Param(dtype=h.Scalar, desc="Transistor Multiplier", default=1)


nmos = h.ExternalModule(
    name="nmos",
    desc="Nmos Transistor (Multiplier Param Only!)",
    port_list=deepcopy(h.Mos.port_list),
    paramtype=PdkMosParams,
    spicetype=SpiceType.MOS,
)
pmos = h.ExternalModule(
    name="pmos",
    desc="Pmos Transistor (Multiplier Param Only!)",
    port_list=deepcopy(h.Mos.port_list),
    paramtype=PdkMosParams,
    spicetype=SpiceType.MOS,
)

@h.paramclass
class LatchParams:
    """Parameter class"""
    w1 = h.Param(dtype=int, desc="Width of NMOS M1", default=10)
    w2 = h.Param(dtype=int, desc="Width of PMOS M2", default=20)
    w3 = h.Param(dtype=int, desc="Width of NMOS M3", default=10)
    w4 = h.Param(dtype=int, desc="Width of PMOS M4", default=20)
    VDD = h.Param(dtype=h.Scalar, desc="VDD voltage", default=1.2)


@h.generator
def Latch(p: LatchParams) -> h.Module:
    """# Latch """

    @h.module
    class SimpleLatch:
        # IO Interface
        VDD, VSS = 2 * h.Input()
        Q0 = h.Input()
        
        inp = h.Diff(desc="Differential Input", port=True, role=h.Diff.Roles.SINK)
        Q = h.Output()

        # Input Inverter
        M1 = nmos(m=p.w1)(d=Q0, g=Q, s=VSS, b=VSS) # NMOS of input Inv
        M2 = pmos(m=p.w2)(d=Q0, g=Q, s=VDD, b=VDD) # PMOS of input Inv

        # Output Inverter
        M3 = nmos(m=p.w3)(d=Q, g=Q0, s=VSS, b=VSS) # NMOS of output Inv
        M4 = pmos(m=p.w4)(d=Q, g=Q0, s=VDD, b=VDD) # PMOS of output Inv

    return SimpleLatch


@hs.sim

# FIXME: Need to get 
# (i) settling time;
# (ii) power consumption

class MosDcopSim:
    """# Mos Dc Operating Point Simulation Input"""
    # def __init__(params):
        

    @h.module
    class Tb:
        """# Basic Mos Testbench"""

        VSS = h.Port()  # The testbench interface: sole port VSS
        vdc = h.Vdc(dc=1.2)(n=VSS)  # A DC voltage source
        dcin = h.Diff()
        sig_out = h.Signal()
        i_bias = h.Signal()
        sig_p = h.Vdc(dc=0.6, ac=0.5)(p=dcin.p,n=VSS)
        sig_n = h.Vdc(dc=0.6, ac=-0.5)(p=dcin.n,n=VSS)
        Isource = h.Isrc(dc = 3e-5)(p = vdc.p, n = i_bias)
        
        inst=Latch()(VDD=vdc.p, VSS=VSS, ibias=i_bias, inp=dcin, out=sig_out)

    # Simulation Stimulus
    op = hs.Op()
    ac = hs.Ac(sweep=hs.LogSweep(1e1, 1e10, 10))
    mod = hs.Include("../45nm_bulk.txt")



def main():
    # h.netlist(OpAmp(), sys.stdout)

    opts = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE,
        fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
        rundir="./scratch",  # Set the working directory for the simulation. Uses a temporary directory by default.
    )
    if not vsp.ngspice.available():
        print("ngspice is not available. Skipping simulation.")
        return

    # Run the simulation!
    results = MosDcopSim.run(opts)

    print("Gain:            "+str(find_dc_gain(2*results["ac"].data["v(xtop.sig_out)"])))
    print("UGBW:            "+str(find_ugbw(results["ac"].freq,2*results["ac"].data["v(xtop.sig_out)"])))
    print("Phase margin:    "+str(find_phm(results["ac"].freq,2*results["ac"].data["v(xtop.sig_out)"])))
    print("Ivdd:            "+str(find_I_vdd(results["ac"].data["i(v.xtop.vvdc)"])))


    

def find_I_vdd(vout:numpy.array) -> float:
    return numpy.abs(vout)[0]

def find_dc_gain(vout:numpy.array) -> float:
    return numpy.abs(vout)[0]

def find_ugbw(freq:numpy.array, vout:numpy.array) -> float:
    gain = numpy.abs(vout)
    ugbw_index, valid = _get_best_crossing(gain, val=1)
    if valid:
        return freq[ugbw_index]
    else:
        return freq[0]

def find_phm(freq:numpy.array, vout:numpy.array) -> float:
    gain = numpy.abs(vout)
    phase = numpy.angle(vout, deg=False)
    phase = numpy.unwrap(phase)  # unwrap the discontinuity
    phase = numpy.rad2deg(phase)  # convert to degrees

    ugbw_index, valid = _get_best_crossing(gain, val=1)
    if valid:
        if phase[ugbw_index] > 0:
            return -180 + phase[ugbw_index]
        else:
            return 180 + phase[ugbw_index]
    else:
        return -180

def _get_best_crossing(yvec:numpy.array, val:float) -> tuple[int, bool]:
    zero_crossings = numpy.where(numpy.diff(numpy.sign(yvec-val)))[0]
    if len(zero_crossings)==0:
        return 0, False
    if abs((yvec-val)[zero_crossings[0]]) < abs((yvec-val)[zero_crossings[0]+1]):
        return zero_crossings[0], True
    else:
        return (zero_crossings[0]+1), True


if __name__ == "__main__":
    main()
