"""
# Latch Example

"""

import hdl21 as h
import hdl21.sim as hs
import vlsirtools.spice as vsp
from hdl21.prefix import NANO, PICO
import numpy

from autockt_shared import FlipFlopInput, FlipFlopOutput

# import Latch
from .Latch import LatchParams, LatchGen


def _get_delay(
    out: numpy.array, clk: numpy.array, time: numpy.array, ifdebug=False
) -> float:
    VDD_voltage = 1.2
    out_crossing = numpy.where(numpy.diff(numpy.sign(out - 0.5 * VDD_voltage)))[0]
    out_crossing_time = []
    for t in out_crossing:
        out_crossing_time.append(time[t])
    clk_crossing = numpy.where(numpy.diff(numpy.sign(clk - 0.5 * VDD_voltage)))[0]
    clk_crossing_time = []
    for y in clk_crossing:
        clk_crossing_time.append(time[y])
    #     print("time[y]:            "+str(time[y]))
    # print("clk_crossing_time:       "+str(out_crossing_time))

    crossing_count = 0
    crossing_sum = 0
    for t in out_crossing_time:
        crossing_count += 1
        clk_time_to_subtract = clk_crossing_time[
            numpy.where(numpy.diff(numpy.sign(clk_crossing_time - t)))[0][0]
        ]
        crossing_sum += t - clk_time_to_subtract
        if ifdebug:
            print(str(clk_time_to_subtract) + " -> " + str(t))
    delay = crossing_sum / crossing_count

    if ifdebug:
        print("out_crossing:            " + str(out_crossing))
        print("out_crossing_time:       " + str(out_crossing_time))
        print("clk_crossing:            " + str(clk_crossing))
        print("clk_crossing_time:       " + str(clk_crossing_time))

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

    L1 = h.Param(dtype=LatchParams, desc="params of Latch1", default=LatchParams())
    L2 = h.Param(dtype=LatchParams, desc="params of Latch2", default=LatchParams())


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
        Sampling_latch = LatchGen(p.L1)(
            VDD=VDD, VSS=VSS, CLK=CKB, CKB=CLK, D=D, Q=intermediate_signal
        )

        # Holding latch
        Holding_latch = LatchGen(p.L2)(
            VDD=VDD, VSS=VSS, CLK=CLK, CKB=CKB, D=intermediate_signal, Q=Q
        )

    return FF


def FFSim(params: FFParams, input_shift: float) -> h.sim.Sim:
    """# FF Simulation Input"""

    @hs.sim
    class FFSimGen:
        @h.module
        class Tb:
            """# Basic Mos Testbench"""

            VSS = h.Port()  # The testbench interface: sole port VSS
            vdc = h.Vdc(dc=1.2)(n=VSS)  # A DC voltage source

            input_params = h.PulseVoltageSourceParams(
                delay=input_shift,
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

            inst = FFgen(params)(
                VDD=vdc.p, VSS=VSS, D=vin.p, CLK=CLK.p, CKB=CKB.p, Q=sig_out
            )

        # Simulation Stimulus
        op = hs.Op()
        # ac = hs.Ac(sweep=hs.LogSweep(1e1, 1e10, 10))
        tr = hs.Tran(tstop=31 * NANO, tstep=1 * h.prefix.p, name="mytran")
        mod = hs.Include("../45nm_bulk.txt")

    return FFSimGen


def FF_inner(
    params: FFParams, input_shift: float, round: int, ifdebug=False
) -> tuple[bool, float, float]:
    """# FF Generation & Simulation
    Inner implementation. Also used for testing."""

    if not vsp.ngspice.available():
        raise RuntimeError(f"Cannot find ngspice simulator")

    # Create a set of simulation input for it
    sim_input = FFSim(params, input_shift)

    # Simulation options
    opts = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE,
        fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
        rundir="./scratch",  # Set the working directory for the simulation. Uses a temporary directory by default.
    )

    # Run the simulation!
    results = sim_input.run(opts)

    if ifdebug:
        from matplotlib import pyplot as plt

        plt.cla()
        plt.plot(
            results["tr"].data["time"],
            results["tr"].data["v(xtop.sig_out)"],
            label="sig_out",
        )
        plt.plot(
            results["tr"].data["time"],
            results["tr"].data["v(xtop.clk_p)"],
            label="clk_p",
        )
        plt.plot(
            results["tr"].data["time"],
            results["tr"].data["v(xtop.vin_p)"],
            label="vin_p",
        )
        plt.legend()
        plt.show()
        plt.savefig("FF_sim_" + str(round) + ".png")

    if results["tr"].data["v(xtop.sig_out)"][7517] > 0.12:
        return False, 0, 0
    if results["tr"].data["v(xtop.sig_out)"][17529] < 1.08:
        return False, 0, 0
    if results["tr"].data["v(xtop.sig_out)"][27546] > 0.12:
        return False, 0, 0

    # Extract our metrics from those results
    output_delay = _get_delay(
        results["tr"].data["v(xtop.sig_out)"],
        results["tr"].data["v(xtop.clk_p)"],
        results["tr"].data["time"],
        ifdebug,
    )
    power = _get_FF_power(results["tr"].data["i(v.xtop.vvdc)"], 1.2)

    # And return them as an `OpAmpOutput`
    return True, output_delay, power


def flip_flop_sim(inp: FlipFlopInput) -> FlipFlopOutput:
    """
    FlipFlop Simulation
    """
    ifdebug = False

    params = FFParams(
        LatchParams(inp.l1), LatchParams(inp.l2)
    )  # TODO: Is this a correct way?
    ifwork, output_delay, power = FF_inner(params, 0, 0)
    if ifdebug:
        print("clk->q delay:    " + str(output_delay))
        print("power:           " + str(power))
        print("==============================")
    shift_min = 0 * NANO
    shift_max = 5 * NANO
    cursor = (shift_min + shift_max) / 2
    ifwork, temp_delay, power_null = FF_inner(params, cursor, 1)
    round = 1

    if ifdebug:
        print("round:           " + str(round))
        print("clk->q delay:    " + str(temp_delay))
        print("max shift:       " + str(float(shift_max)))
        print("min shift:       " + str(float(shift_min)))
        print("==============================")

    while (shift_max - shift_min) > 0.1 * PICO:
        if ifwork == False:
            shift_max = cursor
        elif temp_delay > 1.05 * output_delay:
            shift_max = cursor
        elif temp_delay == 1.05 * output_delay:
            break
        else:
            shift_min = cursor
        cursor = (shift_min + shift_max) / 2
        round += 1
        ifwork, temp_delay, power_null = FF_inner(params, cursor, round)

        if ifdebug:
            print("round:           " + str(round))
            print("clk->q delay:    " + str(temp_delay))
            print("max shift:       " + str(float(shift_max)))
            print("min shift:       " + str(float(shift_min)))
            print("==============================")

    setup_time = 5 * NANO - cursor

    shift_min = 0 * NANO
    shift_max = -10 * NANO + cursor
    cursor = (shift_min + shift_max) / 2
    ifwork, temp_delay, power_null = FF_inner(params, cursor, 100)
    round = 100

    if ifdebug:
        print("round:           " + str(round))
        print("clk->q delay:    " + str(temp_delay))
        print("max shift:       " + str(float(shift_max)))
        print("min shift:       " + str(float(shift_min)))
        print("==============================")

    while (shift_min - shift_max) > 0.1 * PICO:
        if ifwork == False:
            shift_max = cursor
        elif temp_delay > 1.05 * output_delay:
            shift_max = cursor
        elif temp_delay == 1.05 * output_delay:
            break
        else:
            shift_min = cursor
        cursor = (shift_min + shift_max) / 2
        round += 1
        ifwork, temp_delay, power_null = FF_inner(params, cursor, round)

        if ifdebug:
            print("round:           " + str(round))
            print("clk->q delay:    " + str(temp_delay))
            print("max shift:       " + str(float(shift_max)))
            print("min shift:       " + str(float(shift_min)))
            print("==============================")

    hold_time = 5 * NANO + cursor

    return FlipFlopOutput(
        power=power,
        output_delay=output_delay,
        setup_time=setup_time,
        hold_time=hold_time,
    )


def main():
    ifdebug = False

    params = FFParams()
    ifwork, output_delay, power = FF_inner(params, 0, 0)
    if ifdebug:
        print("clk->q delay:    " + str(output_delay))
        print("power:           " + str(power))
        print("==============================")
    shift_min = 0 * NANO
    shift_max = 5 * NANO
    cursor = (shift_min + shift_max) / 2
    ifwork, temp_delay, power_null = FF_inner(params, cursor, 1)
    round = 1

    if ifdebug:
        print("round:           " + str(round))
        print("clk->q delay:    " + str(temp_delay))
        print("max shift:       " + str(float(shift_max)))
        print("min shift:       " + str(float(shift_min)))
        print("==============================")

    while (shift_max - shift_min) > 0.1 * PICO:
        if ifwork == False:
            shift_max = cursor
        elif temp_delay > 1.05 * output_delay:
            shift_max = cursor
        elif temp_delay == 1.05 * output_delay:
            break
        else:
            shift_min = cursor
        cursor = (shift_min + shift_max) / 2
        round += 1
        ifwork, temp_delay, power_null = FF_inner(params, cursor, round)

        if ifdebug:
            print("round:           " + str(round))
            print("clk->q delay:    " + str(temp_delay))
            print("max shift:       " + str(float(shift_max)))
            print("min shift:       " + str(float(shift_min)))
            print("==============================")

    setup_time = 5 * NANO - cursor

    shift_min = 0 * NANO
    shift_max = -10 * NANO + cursor
    cursor = (shift_min + shift_max) / 2
    ifwork, temp_delay, power_null = FF_inner(params, cursor, 100)
    round = 100

    if ifdebug:
        print("round:           " + str(round))
        print("clk->q delay:    " + str(temp_delay))
        print("max shift:       " + str(float(shift_max)))
        print("min shift:       " + str(float(shift_min)))
        print("==============================")

    while (shift_min - shift_max) > 0.1 * PICO:
        if ifwork == False:
            shift_max = cursor
        elif temp_delay > 1.05 * output_delay:
            shift_max = cursor
        elif temp_delay == 1.05 * output_delay:
            break
        else:
            shift_min = cursor
        cursor = (shift_min + shift_max) / 2
        round += 1
        ifwork, temp_delay, power_null = FF_inner(params, cursor, round)

        if ifdebug:
            print("round:           " + str(round))
            print("clk->q delay:    " + str(temp_delay))
            print("max shift:       " + str(float(shift_max)))
            print("min shift:       " + str(float(shift_min)))
            print("==============================")

    hold_time = 5 * NANO + cursor

    print("Final Results:")
    print("clk->q delay:    " + str(output_delay * 1e9) + " ns")
    print("power:           " + str(power))
    print("setup time:      " + str(float(setup_time * 1e9)) + " ns")
    print("hold time:       " + str(float(hold_time * 1e9)) + " ns")


if __name__ == "__main__":
    main()
