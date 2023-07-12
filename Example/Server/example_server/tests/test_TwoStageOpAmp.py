""" 
# Fully Differential OTA Example 

Highlights the capacity to use `Diff` signals and `Pair`s of instances 
for differential circuits. 

"""

import os
from pathlib import Path
from copy import deepcopy
import hdl21 as h
import hdl21.sim as hs
import vlsirtools.spice as vsp
from hdl21.external_module import SpiceType
from hdl21.prefix import µ, NANO

from ..TwoStageOpAmp import (
    OpAmp,
    find_I_vdd,
    find_dc_gain,
    find_ugbw,
    find_phm,
)


PARENT_PATH = Path(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SPICE_MODEL_45NM_BULK_PATH = PARENT_PATH / "45nm_bulk.txt"


""" 
Create a small "PDK" consisting of an externally-defined Nmos and Pmos transistor. 
Real versions will have some more parameters; these just have multiplier "m". 
"""


@h.paramclass
class MosParams:
    """
    ! Unused
    """

    m = h.Param(dtype=int, desc="Transistor Multiplier")


@hs.sim
class MosDcopSim:
    """# Mos Dc Operating Point Simulation Input"""

    @h.module
    class Tb:
        """# Basic Mos Testbench"""

        VSS = h.Port()  # The testbench interface: sole port VSS
        vdc = h.Vdc(dc=1.2)(n=VSS)  # A DC voltage source
        dcin = h.Diff()
        sig_out = h.Signal()
        i_bias = h.Signal()
        sig_p = h.Vdc(dc=0.6, ac=0.5)(p=dcin.p, n=VSS)
        sig_n = h.Vdc(dc=0.6, ac=-0.5)(p=dcin.n, n=VSS)
        Isource = h.Isrc(dc=3e-5)(p=vdc.p, n=i_bias)

        inst = OpAmp()(VDD=vdc.p, VSS=VSS, ibias=i_bias, inp=dcin, out=sig_out)

    # Simulation Stimulus
    op = hs.Op()
    ac = hs.Ac(sweep=hs.LogSweep(1e1, 1e10, 10))
    mod = hs.Include(SPICE_MODEL_45NM_BULK_PATH)


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

    print(
        "Gain:            "
        + str(find_dc_gain(2 * results["ac"].data["v(xtop.sig_out)"]))
    )
    print(
        "UGBW:            "
        + str(find_ugbw(results["ac"].freq, 2 * results["ac"].data["v(xtop.sig_out)"]))
    )
    print(
        "Phase margin:    "
        + str(find_phm(results["ac"].freq, 2 * results["ac"].data["v(xtop.sig_out)"]))
    )
    print("Ivdd:            " + str(find_I_vdd(results["ac"].data["i(v.xtop.vvdc)"])))

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


def test():
    main()


if __name__ == "__main__":
    main()
