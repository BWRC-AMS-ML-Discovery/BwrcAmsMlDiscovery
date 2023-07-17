""" 
# Fully Differential OTA Example 

Highlights the capacity to use `Diff` signals and `Pair`s of instances 
for differential circuits. 

In this file, we use the schematic of Fig3.5 in Keertana's article

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
    w15_16 = h.Param(dtype = int, desc = "Width of M15/16", default = 10)
    w5_6 = h.Param(dtype = int, desc = "Width of M5/6", default = 10)
    w2_8 = h.Param(dtype = int, desc = "width of M2/8", default = 10)
    w9_10 = h.Param(dtype = int, desc = "width of M9/10", default = 10)
    w11_12 = h.Param(dtype = int, desc = "Width of M11/12", default = 10)
    w13_14 = h.Param(dtype = int, desc = "Width of M13/14", default = 10)
    w17 = h.Param(dtype = int, desc = "Width of M17", default = 10)
    w1_2 = h.Param(dtype = int, desc = "Width of M1/2", default = 10)
    w7_8 = h.Param(dtype = int, desc = "Width of M7/8", default = 10)
    w18 = h.Param(dtype = int, desc = "width of M18", default = 10)
    VDD = h.Param(dtype=h.Scalar, desc="VDD voltage", default=1.2)
    cl = h.Param(dtype=h.Scalar, desc="cl capacitance", default=1e-14)
    cc = h.Param(dtype=h.Scalar, desc="cc capacitance", default=1e-14)
    rc = h.Param(dtype=h.Scalar, desc="rc resistor", default=100)

@h.generator
def OpAmp(p: OpAmpParams) -> h.Module:
    """# Two stage OpAmp """

    @h.module
    class FoldedCascode:
        # IO Interface
        VDD, VSS = 2 * h.Input()
        ibias = h.Input()
        
        inp = h.Diff(desc="Differential Input", port=True, role=h.Diff.Roles.SINK)
        
        ref = h.Input()
        v9 = h.Output()
        v10 = h.Output()
        v_nmbias = h.Input()
        v_nbbias = h.Input()
        v_bbias = h.Input()
        v_cm = h.Input()
        v_cs = h.Input()

        # Internal Signals
        v1, v2, v3, v4, v5, v6, v7, v8, v11, v12= h.Signals(10)

        # Input Stage
        M1 = nmos(m = p.w1_2)(d = v11, g = inp.p, s = v1, b = v1)
        M2 = nmos(m = p.w1_2)(d = v12, g = inp.n, s = v1, b = v1)
        M17 = nmos(m = p.w17)(d = v1, g = v_nmbias, s = v2, b = v2)
        M18 = nmos(m = p.w18)(d = v2, g = v_nbbias, s = VSS, b = VSS)

        M5 = pmos(m = p.w5_6)(d = v11, g = v_bbias, s = VDD, b = VDD)
        M6 = pmos(m = p.w5_6)(d = v12, g = v_bbias, s = VDD, b = VDD)

        M7 = pmos(m = p.w7_8)(d = v5, g = v_cm, s = v11, b = v11)
        M8 = pmos(m = p.w7_8)(d = v6, g = v_cm, s = v12, b = v12)
        M9 = nmos(m = p.w9_10)(d = v5, g = v_nmbias, s = v3, b = v3)
        M10 = nmos(m = p.w9_10)(d = v6, g = v_nmbias, s = v4, b = v4)
        M11 = nmos(m = p.w11_12)(d = v3, g = v_nbbias, s = VSS, b = VSS)
        M12 = nmos(m = p.w11_12)(d = v4, g = v_nbbias, s = VSS, b = VSS)

        # Output Stage
        M13 = pmos(m = p.w13_14)(d = v9, g = v_cs, s = VDD, b = VDD)
        M14 = pmos(m = p.w13_14)(d = v10, g = v_cs, s = VDD, b = VDD)
        M15 = nmos(m = p.w15_16)(d = v9, g = v5, s = VSS, b = VSS)
        M16 = nmos(m = p.w15_16)(d = v10, g = v6, s = VSS, b = VSS)
        

        # Compensation Network
        Cc_1 = h.Cap(c = p.cc)(p = v9, n = v7) # Miller Capacitance
        Cc_2 = h.Cap(c = p.cc)(p = v10, n = v8)
        Rc_1 = h.Res(r = p.rc)(p = v7, n = v5)
        Rc_2 = h.Res(r = p.rc)(p = v8, n = v6)

    return FoldedCascode


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

# FIXME: no sim yet

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
