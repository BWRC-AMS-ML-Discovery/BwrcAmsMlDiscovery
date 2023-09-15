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


def _get_delay(out: numpy.array, clk: numpy.array, time: numpy.array) -> float:
    VDD_voltage = 1.2
    out_crossing = numpy.where(numpy.diff(numpy.sign(out - 0.5 * VDD_voltage)))[0]
    out_crossing_time = []
    for t in out_crossing:
        out_crossing_time.append(time[t])
    clk_crossing = numpy.where(numpy.diff(numpy.sign(clk - 0.5 * VDD_voltage)))[0]
    clk_crossing_time = []
    for t in clk_crossing:
        clk_crossing_time.append(time[t])
    crossing_count = 0
    crossing_sum = 0
    for t in clk_crossing_time:
        crossing_count += 1
        crossing_sum += (
            t
            - clk_crossing_time[
                numpy.where(
                    numpy.diff(numpy.sign(clk_crossing_time - out_crossing_time[0]))
                )[0][0]
            ]
        )
    delay = crossing_sum / crossing_count
    return delay


def _get_FF_power(Idc: numpy.array, VDD: float) -> float:
    Ivdd = -numpy.average(Idc)
    power = VDD * Ivdd
    return power


@h.paramclass
class FFParams:
    """Parameter class"""

    # L1 = Latch.LatchParams()
    # L2 = Latch.LatchParams()

    L1 = h.Param(
        dtype=Latch.LatchParams, desc="params of Latch1", default=Latch.LatchParams()
    )
    L2 = h.Param(
        dtype=Latch.LatchParams, desc="params of Latch2", default=Latch.LatchParams()
    )


@h.generator
def FFgen(p: FFParams) -> h.Module:
    """# FF"""

    @h.module
    class FF:
        # IO Interface
        VDD, VSS = 2 * h.Input()
        CLK, CKB = 2 * h.Input()
        D = h.Input()
        Q = h.Output()

        intermediate_signal = h.Signal()

        # Sampling latch
        Sampling_latch = Latch.LatchGen(p.L1)(
            VDD=VDD, VSS=VSS, CLK=CKB, CKB=CLK, D=D, Q=intermediate_signal
        )

        # Holding latch
        Holding_latch = Latch.LatchGen(p.L2)(
            VDD=VDD, VSS=VSS, CLK=CLK, CKB=CKB, D=intermediate_signal, Q=Q
        )

    return FF


# def FFSim() -> h.sim.Sim:
#     """# FF Simulation Input"""


@hs.sim
class FFSimGen:
    @h.module
    class Tb:
        """# Basic Mos Testbench"""

        VSS = h.Port()  # The testbench interface: sole port VSS
        vdc = h.Vdc(dc=1.2)(n=VSS)  # A DC voltage source

        input_params = h.PulseVoltageSourceParams(
            delay=0 * NANO,
            v1=1.2,
            v2=0,
            period=20 * NANO,
            width=10 * NANO,
            fall=0,
            rise=0,
        )
        vin = h.PulseVoltageSource(input_params)(n=VSS)

        clock_params = h.PulseVoltageSourceParams(
            delay=5 * NANO,
            v1=0,
            v2=1.2,
            period=10 * NANO,
            width=5 * NANO,
            fall=0,
            rise=0,
        )
        clk_b_params = h.PulseVoltageSourceParams(
            delay=5 * NANO,
            v1=1.2,
            v2=0,
            period=10 * NANO,
            width=5 * NANO,
            fall=0,
            rise=0,
        )
        CLK = h.PulseVoltageSource(clock_params)(n=VSS)
        CKB = h.PulseVoltageSource(clk_b_params)(n=VSS)

        sig_out = h.Signal()

        inst = FFgen()(VDD=vdc.p, VSS=VSS, D=vin.p, CLK=CLK.p, CKB=CKB.p, Q=sig_out)

    # Simulation Stimulus
    op = hs.Op()
    # ac = hs.Ac(sweep=hs.LogSweep(1e1, 1e10, 10))
    tr = hs.Tran(tstop=31 * NANO, tstep=1 * h.prefix.p, name="mytran")
    mod = hs.Include("../45nm_bulk.txt")

    # return FFSimGen


def main():
    # h.netlist(LatchGen(), sys.stdout)
    h.netlist(FFgen(FFParams()), sys.stdout)

    opts = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE,
        fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
        rundir="./scratch",  # Set the working directory for the simulation. Uses a temporary directory by default.
    )
    if not vsp.ngspice.available():
        print("ngspice is not available. Skipping simulation.")
        return

    # Run the simulation!
    results = FFSimGen.run(opts)

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
    plt.savefig("FF_sim.png")

    print("====================")
    delay = _get_delay(
        results["tr"].data["v(xtop.sig_out)"],
        results["tr"].data["v(xtop.clk_p)"],
        results["tr"].data["time"],
    )
    print("delay:    " + str(delay))
    """     VDD_voltage = 1.2
    out_crossing = numpy.where(numpy.diff(numpy.sign(results["tr"].data["v(xtop.sig_out)"] - 0.5*VDD_voltage)))[0]
    print("out_crossing:    "+str(out_crossing))
    out_crossing_time=[]
    for t in out_crossing:
        out_crossing_time.append(results["tr"].data["time"][t])
    print("out_crossing_time:    "+str(out_crossing_time))
    clk_crossing = numpy.where(numpy.diff(numpy.sign(results["tr"].data["v(xtop.clk_p)"] - 0.5*VDD_voltage)))[0]
    print("vin_crossing:    "+str(clk_crossing))
    clk_crossing_time=[]
    for t in clk_crossing:
        clk_crossing_time.append(results["tr"].data["time"][t])
    print("clk_crossing_time:    "+str(clk_crossing_time))
    crossing_count=0
    crossing_sum = 0
    for t in clk_crossing_time:
        crossing_count += 1
        crossing_sum += t - clk_crossing_time[numpy.where(numpy.diff(numpy.sign(clk_crossing_time - out_crossing_time[0])))[0][0]]
    delay = crossing_sum / crossing_count
    print("delay:    "+str(delay)) """

    # Ivdd = -numpy.average(results["tr"].data["i(v.xtop.vvdc)"])
    # print("Ivdd:            "+str(Ivdd))

    power = _get_FF_power(results["tr"].data["i(v.xtop.vvdc)"], 1.2)
    print("Power:            " + str(power))

    print("====================")
    time_crossing = numpy.where(
        numpy.diff(numpy.sign(results["tr"].data["time"] - 0.75e-8))
    )[0]
    print("time1:    " + str(time_crossing))
    time_crossing = numpy.where(
        numpy.diff(numpy.sign(results["tr"].data["time"] - 1.75e-8))
    )[0]
    print("time2:    " + str(time_crossing))
    time_crossing = numpy.where(
        numpy.diff(numpy.sign(results["tr"].data["time"] - 2.75e-8))
    )[0]
    print("time2:    " + str(time_crossing))


if __name__ == "__main__":
    main()
