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


def _get_best_crossing(yvec: numpy.array, val: float) -> tuple[int, bool]:
    zero_crossings = numpy.where(numpy.diff(numpy.sign(yvec - val)))[0]
    if len(zero_crossings) == 0:
        return 0, False
    if abs((yvec - val)[zero_crossings[0]]) < abs((yvec - val)[zero_crossings[0] + 1]):
        return zero_crossings[0], True
    else:
        return (zero_crossings[0] + 1), True


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
    w5 = h.Param(dtype=int, desc="Width of NMOS M5", default=10)
    w6 = h.Param(dtype=int, desc="Width of PMOS M6", default=20)
    w7 = h.Param(dtype=int, desc="Width of PMOS M7", default=20)
    w8 = h.Param(dtype=int, desc="Width of PMOS M8", default=20)
    w9 = h.Param(dtype=int, desc="Width of NMOS M9", default=10)
    w10 = h.Param(dtype=int, desc="Width of NMOS M10", default=10)
    VDD = h.Param(dtype=h.Scalar, desc="VDD voltage", default=1.2)


@h.generator
def LatchGen(p: LatchParams) -> h.Module:
    """# Latch"""

    @h.module
    class Latch:
        # IO Interface
        VDD, VSS = 2 * h.Input()
        CLK, CKB = 2 * h.Input()
        D = h.Input()
        Q = h.Output()

        clk_vdd, ckb_vdd, clk_gnd, ckb_gnd = h.Signals(4)
        QB = h.Signal()

        # Input Inverter
        in_inv_mn = nmos(m=p.w1)(d=QB, g=D, s=clk_gnd, b=clk_gnd)  # NMOS of input Inv
        in_inv_mp = pmos(m=p.w2)(d=QB, g=D, s=ckb_vdd, b=ckb_vdd)  # PMOS of input Inv

        # Output Inverter
        out_inv_mn = nmos(m=p.w3)(d=QB, g=Q, s=ckb_gnd, b=ckb_gnd)  # NMOS of output Inv
        out_inv_mp = pmos(m=p.w4)(d=QB, g=Q, s=clk_vdd, b=clk_vdd)  # PMOS of output Inv

        # QB -> Q Inverter
        qb_inv_mn = nmos(m=p.w5)(d=Q, g=QB, s=VSS, b=VSS)  # NMOS of QB Inv
        qb_inv_mp = pmos(m=p.w6)(d=Q, g=QB, s=VDD, b=VDD)  # PMOS of QB Inv

        # VDD CLK Gate
        vdd_gate_clk = pmos(m=p.w7)(d=clk_vdd, g=CLK, s=VDD, b=VDD)  # VDD gate for CLK
        vdd_gate_ckb = pmos(m=p.w8)(d=ckb_vdd, g=CKB, s=VDD, b=VDD)  # VDD gate for CKB

        # GND CLK Gate
        gnd_gate_ckg = nmos(m=p.w9)(d=ckb_gnd, g=CKB, s=VSS, b=VSS)  # GND gate for CKB
        gnd_gate_clk = nmos(m=p.w10)(d=clk_gnd, g=CLK, s=VSS, b=VSS)  # GND gate for CLK

    return Latch


# FIXME: Need to get
# (i) settling time;
# (ii) power consumption


@hs.sim
class LatchSim:
    @h.module
    class Tb:
        """# Basic Mos Testbench"""

        VSS = h.Port()  # The testbench interface: sole port VSS
        vdc = h.Vdc(dc=1.2)(n=VSS)  # A DC voltage source

        input_params = h.PulseVoltageSourceParams(
            delay=2 * NANO,
            v1=1.2,
            v2=0,
            period=10 * NANO,
            width=5 * NANO,
            fall=0,
            rise=0,
        )
        vin = h.PulseVoltageSource(input_params)(n=VSS)

        clock_params = h.PulseVoltageSourceParams(
            delay=1 * NANO,
            v1=0,
            v2=1.2,
            period=20 * NANO,
            width=10 * NANO,
            fall=0,
            rise=0,
        )
        clk_b_params = h.PulseVoltageSourceParams(
            delay=1 * NANO,
            v1=1.2,
            v2=0,
            period=20 * NANO,
            width=10 * NANO,
            fall=0,
            rise=0,
        )
        CLK = h.PulseVoltageSource(clock_params)(n=VSS)
        CKB = h.PulseVoltageSource(clk_b_params)(n=VSS)

        sig_out = h.Signal()

        inst = LatchGen()(VDD=vdc.p, VSS=VSS, D=vin.p, CLK=CLK.p, CKB=CKB.p, Q=sig_out)

    # Simulation Stimulus
    op = hs.Op()
    # ac = hs.Ac(sweep=hs.LogSweep(1e1, 1e10, 10))
    tr = hs.Tran(tstop=31 * NANO, tstep=1 * h.prefix.p, name="mytran")
    mod = hs.Include("../45nm_bulk.txt")


def main():
    # h.netlist(LatchGen(), sys.stdout)
    h.netlist(LatchGen(LatchParams()), sys.stdout)

    opts = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE,
        fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
        rundir="./scratch",  # Set the working directory for the simulation. Uses a temporary directory by default.
    )
    if not vsp.ngspice.available():
        print("ngspice is not available. Skipping simulation.")
        return

    # Run the simulation!
    results = LatchSim.run(opts)

    print(results)
    print("====================")
    print(results["tr"])
    print("====================")
    print(results["tr"].data["time"])
    print("====================")
    print(results["tr"].data["v(xtop.sig_out)"])
    print("====================")
    print("v(xtop.clk_p)")
    print(results["tr"].data["v(xtop.clk_p)"])
    print("====================")
    print("v(xtop.vin_p)")
    print(results["tr"].data["v(xtop.vin_p)"])
    print("====================")
    print(type(results["tr"].data["v(xtop.sig_out)"]))
    print("====================")
    # print(results["tr"].data["time"].transpose()+results["tr"].data["v(xtop.sig_out)"].transpose())
    table1 = numpy.vstack(
        (
            results["tr"].data["time"],
            results["tr"].data["v(xtop.sig_out)"],
            results["tr"].data["v(xtop.clk_p)"],
            results["tr"].data["v(xtop.vin_p)"],
        )
    )
    print(table1)
    print("====================")
    table2 = table1.T
    print(table2)
    print("====================")
    table3 = numpy.vstack(
        (["time", "v(xtop.sig_out)", "v(xtop.clk_p)", "v(xtop.vin_p)"], table2)
    )
    print(table3)
    numpy.savetxt("Latch.csv", table2, delimiter=",")

    from matplotlib import pyplot as plt

    plt.plot(
        results["tr"].data["time"],
        results["tr"].data["v(xtop.sig_out)"],
        label="sig_out",
    )
    plt.plot(
        results["tr"].data["time"], results["tr"].data["v(xtop.clk_p)"], label="clk_p"
    )
    plt.plot(
        results["tr"].data["time"], results["tr"].data["v(xtop.vin_p)"], label="vin_p"
    )
    plt.legend()
    plt.show()
    plt.savefig("Latch_sim.png")

    print("====================")
    out_crossing = numpy.where(
        numpy.diff(numpy.sign(results["tr"].data["v(xtop.sig_out)"] - 0.6))
    )[0]
    print("out_crossing:    " + str(out_crossing))
    vin_crossing = numpy.where(
        numpy.diff(numpy.sign(results["tr"].data["v(xtop.vin_p)"] - 0.6))
    )[0]
    print("vin_crossing:    " + str(vin_crossing))

    # print("Gain:            "+str(find_dc_gain(2*results["ac"].data["v(xtop.sig_out)"])))
    # print("UGBW:            "+str(find_ugbw(results["ac"].freq,2*results["ac"].data["v(xtop.sig_out)"])))
    # print("Phase margin:    "+str(find_phm(results["ac"].freq,2*results["ac"].data["v(xtop.sig_out)"])))
    # print("Ivdd:            "+str(find_I_vdd(results["ac"].data["i(v.xtop.vvdc)"])))


if __name__ == "__main__":
    main()
