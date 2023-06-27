""" 
# Simple Two-Stage LDO Example 

Highlights the capacity to use `Diff` signals and `Pair`s of instances 
for differential circuits. 

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
class OpAmpParams:
    """Parameter class"""
    w1a = h.Param(dtype=int, desc="Width of NMOS M1a", default=10)
    w1b = h.Param(dtype=int, desc="Width of NMOS M1b", default=10)
    w2a = h.Param(dtype=int, desc="Width of PMOS M2a", default=4)
    w2b = h.Param(dtype=int, desc="Width of PMOS M2b", default=38)
    w3 = h.Param(dtype=int, desc="Width of PMOS M3", default=38)
    w4a = h.Param(dtype=int, desc="Width of NMOS M4a", default=9)
    w4b = h.Param(dtype=int, desc="Width of NMOS M4b", default=20)
    VDD = h.Param(dtype=h.Scalar, desc="VDD voltage", default=1.2)
    CL = h.Param(dtype=h.Scalar, desc="CL capacitance", default=1e-11)
    Cc = h.Param(dtype=h.Scalar, desc="Cc capacitance", default=3e-12)
    Iref = h.Param(dtype=h.Scalar, desc="ibias current", default=3e-5)


@h.generator
def LDO(p: OpAmpParams) -> h.Module:
    """# Two stage LDO """

    @h.module
    class LDOModule:
        # IO Interface
        VDD, VSS = 2 * h.Input()
        Iref = h.Input()
        Vref = h.Input()
        Vreg = h.Output()
        IL = h.Output() # the current of load circuit, FIXME(maybe)

        # Internal Signals
        V1, V2, V3, V5, V6 = h.Signals(5)

        # Error Amp & Current Mirror
        M1a = nmos(m=p.w1a)(d=V1, g=V3, s=V5, b=V5) # Feedback MOS
        M1b = nmos(m=p.w1b)(d=V2, g=Vref, s=V5, b=V5) # Vref MOS
        M2a = pmos(m=p.w2a)(d=V1, g=V1, s=VDD, b=VDD) 
        M2b = pmos(m=p.w2b)(d=V2, g=V1, s=VDD, b=VDD) 
        M4a = nmos(m=p.w4a)(d=V6, g=V6, S=VSS, b=VSS) # current mirror source
        M4b = nmos(m=p.w4b)(d=V5, g=V6, s=VSS, b=VSS) # curreent mirror

        # Output Stage
        mp3 = pmos(m=p.w3)(d=Vreg, g=V2, s=VDD, b=VDD) # output PMOS

        CL = h.Cap(c=p.CL)(p = Vreg, n = VSS) # Load capacitance

        # Compensation Network
        Cc = h.Cap(c = p.Cc)(p = V2, n = Vreg) # Miller Capacitance

        # Feedback Resistors
        R1 = h.Res(r = p.R1)(p = Vreg, n = V3)
        R2 = h.Res(r = p.R2)(p = V3, n = VSS)

    return LDOModule


@h.module
class CapCell:
    """# Compensation Capacitor Cell"""

    p, n, VDD, VSS = 4 * h.Port()
    # FIXME: internal content! Using tech-specific `ExternalModule`s


@h.module
class ResCell:
    """# Compensation Resistor Cell"""

    p, n, sub = 3 * h.Port()
    # FIXME: internal content! Using tech-specific `ExternalModule`s


@h.module
class Compensation:
    """# Single Ended RC Compensation Network"""

    a, b, VDD, VSS = 4 * h.Port()
    r = ResCell(p=a, sub=VDD)
    c = CapCell(p=r.n, n=b, VDD=VDD, VSS=VSS)


@hs.sim
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
        
        inst=OpAmp()(VDD=vdc.p, VSS=VSS, ibias=i_bias, inp=dcin, out=sig_out)

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

    """     # Get the transistor drain current
    # print(results)
    print(results["op"])
    print(results["ac"].data["v(xtop.sig_out)"])
    print(results["ac"].data["i(v.xtop.vvdc)"])
    # # print(results["ac"].data["v(xtop.dcin_p)"])
    # # print(results["ac"].data["v(xtop.dcin_n)"])
    print(type(results))
    print(type(results["ac"]))
    print(type(results["ac"].data["v(xtop.sig_out)"]))
    print(results["ac"].data.keys())
    print(type(results["ac"].data)) """

    print("Gain:            "+str(find_dc_gain(2*results["ac"].data["v(xtop.sig_out)"])))
    print("UGBW:            "+str(find_ugbw(results["ac"].freq,2*results["ac"].data["v(xtop.sig_out)"])))
    print("Phase margin:    "+str(find_phm(results["ac"].freq,2*results["ac"].data["v(xtop.sig_out)"])))
    print("Ivdd:            "+str(find_I_vdd(results["ac"].data["i(v.xtop.vvdc)"])))


    # result_list=list(results["ac"].data["v(xtop.sig_out)"])
    # result_list_i=list(results["ac"].data["i(v.xtop.vvdc)"])
    # import math, cmath
    # # from tabulate import tabulate
    # for i in range(len(result_list)):
    #     freq = 10 * math.pow(10,i/10)
    #     gain = result_list[i]
    #     abs_gain = abs(result_list[i])*2
    #     gain_phase = math.degrees(cmath.phase(gain))
    #     power_con = abs(result_list_i[i])
    #     print (format(freq,".7E")+"   "+format(gain,".7E")+"   "+format(abs_gain,".7E")+"   "+str(gain_phase)+"   "+format(power_con,".7E"))
    
    # for i in range(len(result_list)-1):
    #     if (abs(result_list[i])*2>1) & (abs(result_list[i+1])*2<1):
    #         if abs(abs(result_list[i])*2-1) > abs(abs(result_list[i+1])*2-1):
    #             ugbw = 10 * math.pow(10,(i+1)/10)
    #             phase_margin = math.degrees(cmath.phase(result_list[i+1]))
    #         else:
    #             ugbw = 10 * math.pow(10,i/10)
    #             phase_margin = math.degrees(cmath.phase(result_list[i]))

    # # print(result_list)
    # # print(len(result_list))
    # # print(list(results["ac"].data["v(xtop.sig_out)"]))
    # # print(len(results["ac"].data["v(xtop.sig_out)"]))
    # print("Gain: "+format(abs(result_list[0])*2,".7e"))
    # print("UGBW: "+format(ugbw,".7e"))
    # print("Phase Margin: "+str(180+phase_margin))
    # print("Ivdd: "+format(abs(result_list_i[0]),".7e"))

"""     import numpy
    numpy.set_printoptions(precision=7, suppress=False)
    print(numpy.abs(results["ac"].data["v(xtop.sig_out)"]))
    numpy.set_printoptions(precision=7, suppress=True)
    print(numpy.angle(results["ac"].data["v(xtop.sig_out)"], deg=True))
    print((results["ac"].freq))
 """

    

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
