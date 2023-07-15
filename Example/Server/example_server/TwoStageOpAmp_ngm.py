""" 
# Fully Differential OTA Example 

Highlights the capacity to use `Diff` signals and `Pair`s of instances 
for differential circuits. 

In this file, we use the schematic of Fig2.18 in Keertana's article

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
    wtail1 = h.Param(dtype = int, desc = "Width of PMOS Mtial1", default = 10)
    wtail2 = h.Param(dtype = int, desc = "Width of PMOS Mtial2", default = 10)
    wcm = h.Param(dtype = int, desc = "width of PMOS Mcm", default = 10)
    win = h.Param(dtype = int, desc = "width od PMOS Min", default = 10)
    wref = h.Param(dtype = int, desc = "Width of PMOS Mref", default = 10)
    wd1 = h.Param(dtype = int, desc = "Width of NMOS Md1", default = 10)
    wd = h.Param(dtype = int, desc = "Width of NMOS Md", default = 10)
    wn_gm = h.Param(dtype = int, desc = "Width of NMOS Mn_gm", default = 10)
    wtail = h.Param(dtype = int, desc = "Width of PMOS Mtial", default = 10)
    wtailr = h.Param(dtype=int, desc="Width of PMOS Mtailr", default=10)
    VDD = h.Param(dtype=h.Scalar, desc="VDD voltage", default=1.2)
    Cc = h.Param(dtype=h.Scalar, desc="Cc capacitance", default=1e-14)
    Rf = h.Param(dtype=h.Scalar, desc="Rf resistor", default=100)

@h.generator
def OpAmp(p: OpAmpParams) -> h.Module:
    """# Two stage OpAmp """

    @h.module
    class DiffOta:
        # IO Interface
        VDD, VSS = 2 * h.Input()
        ibias = h.Input()
        
        inp = h.Diff(desc="Differential Input", port=True, role=h.Diff.Roles.SINK)
        cm = h.Input()
        ref = h.Input()
        v5 = h.Output()
        v6 = h.Output()

        # Internal Signals
        v1, v2, v3, v4, v7, v8, v9 = h.Signals(7)

        # Input & Output Stage
        Mcm_1 = pmos(m = p.wcm)(d = v3, g = cm, s = VDD, b = VDD)
        Mcm_2 = pmos(m = p.wcm)(d = v9, g = cm, s = VDD, b = VDD)
        Md1_1 = nmos(m = p.wd1)(d = v3, g = v5, s = VSS, b = VSS)
        Md1_2 = nmos(m = p.wd1)(d = v9, g = v6, s = VSS, b = VSS)

        Min_1 = pmos(m = p.win)(d = v7, g = inp.p, s = v5, b = v5)
        Min_2 = pmos(m = p.win)(d = v7, g = inp.n, s = v6, b = v6)
        Md_1 = nmos(m = p.wd1)(d = v5, g = v5, s = VSS, b = VSS)
        Md_2 = nmos(m = p.wd1)(d = v6, g = v6, s = VSS, b = VSS)
        Mn_gm_1 = nmos(m = p.wn_gm)(d = v5, g = v6, s = VSS, b = VSS)
        Mn_gm_2 = nmos(m = p.wn_gm)(d = v6, g = v5, s = VSS, b = VSS)

        # Biasing
        Mref = pmos(m = p.wref)(d = v1, g = ref, s = v2, b = v2) 
        Mtailr = pmos(m = p.wtailr)(d = v2, g = v1, s = VDD, b = VDD)
        Mtail = pmos(m = p.wtail)(d = v7, g = v1, s = VDD, b = VDD)
        Mtail1 = pmos(m = p.wtail1)(d = v3, g = v1, s = VDD, b = VDD)
        Mtail2 = pmos(m = p.wtail2)(d = v9, g = v1, s = VDD, b = VDD)


        # Compensation Network
        Cc_1 = h.Cap(c = p.Cc)(p = v4, n = v5) # Miller Capacitance
        Cc_2 = h.Cap(c = p.Cc)(p = v8, n = v6)
        Rf_1 = h.Res(r = p.Rf)(p = v3, n = v4)
        Rf_2 = h.Res(r = p.Rf)(p = v9, n = v8)

    return DiffOta


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
