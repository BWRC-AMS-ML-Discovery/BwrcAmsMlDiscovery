"""
# AutoCkt Server
"""

# Stdlib Imports
from dataclasses import asdict

# PyPi Imports
import hdl21 as h
import vlsirtools.spice as vsp
from hdl21.prefix import µ, NANO, PICO

import discovery_server as ds
from discovery_server import Config
from dotenv import dotenv_values

# Workspace Imports
from autockt_shared import (
    OpAmpInput,
    OpAmpOutput,
    FlipFlopInput,
    FlipFlopOutput,
    FoldedCascodeInput,
    LDOInput,
    LDOOutput,
    LatchInput,
    LatchOutput,
    TwoStageOpAmpNgmInput,
    latch_sim,
    flip_flop_sim,
    folded_cascode_sim,
    ldo_sim,
    two_stage_op_amp_ngm_sim,
    auto_ckt_sim,
    auto_ckt_sim_hdl21,
)
from .auto_ckt_sim_lib import (
    create_design,
    simulate,
    translate_result,
)

# FIXME: move all these dependencies into `tb` as well
from .tb import (
    find_dc_gain,
    find_I_vdd,
    find_phm,
    find_ugbw,
)


# FIXME should be async? FastAPI says both are ok.
@auto_ckt_sim.impl
def auto_ckt_sim(inp: OpAmpInput) -> OpAmpOutput:
    """
    AutoCkt Simulation
    """
    # print(f"input {inp}")
    tmpdir, design_folder, fpath = create_design(inp)

    # print(f"design created {design_folder}")
    # TODO Error return?
    info = simulate(fpath)

    # print(f"simualted {info}")

    specs = translate_result(tmpdir, design_folder)
    # print(f"to specs {specs}")
    return specs


from .Latch import LatchParams, Latch_inner


@latch_sim.impl
def latch_sim(inp: LatchInput) -> LatchOutput:
    """
    Latch Simulation
    """
    opts = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE,
        fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
        rundir="./scratch",  # Set the working directory for the simulation. Uses a temporary directory by default.
    )
    if not vsp.ngspice.available():
        print("ngspice is not available. Skipping simulation.")
        return

    ifdebug = False

    params = LatchParams(
        w1=inp.w1,
        w2=inp.w2,
        w3=inp.w3,
        w4=inp.w4,
        w5=inp.w5,
        w6=inp.w6,
        w7=inp.w7,
        w8=inp.w8,
        w9=inp.w9,
        w10=inp.w10,
        VDD=inp.VDD,
    )
    ifwork, output_delay, power = Latch_inner(params, 5 * NANO, 0, ifdebug)
    if ifdebug:
        print("clk->q delay:    " + str(output_delay))
        print("power:           " + str(power))
        print("==============================")
    shift_min = 5 * NANO
    shift_max = 11 * NANO
    cursor = (shift_min + shift_max) / 2
    ifwork, temp_delay, power_null = Latch_inner(params, cursor, 1, ifdebug)
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
        ifwork, temp_delay, power_null = Latch_inner(params, cursor, round, ifdebug)
        if ifdebug:
            print("round:           " + str(round))
            print("clk->q delay:    " + str(temp_delay))
            print("max shift:       " + str(float(shift_max)))
            print("min shift:       " + str(float(shift_min)))
            print("==============================")

    setup_time = 10 * NANO - cursor

    return LatchOutput(power=power, output_delay=output_delay, setup_time=setup_time)


from .FF import FFParams, FF_inner


@flip_flop_sim.impl
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


from .FoldedCascode import (
    FoldedCascodeParams,
    FoldedCascodeSim,
    find_dc_gain,
    find_I_vdd,
    find_phm,
    find_ugbw,
)


@folded_cascode_sim.impl
def folded_cascode_sim(inp: FoldedCascodeInput) -> OpAmpOutput:
    """
    FoldedCascode Simulation
    """
    opts = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE,
        fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
        rundir="./scratch",  # Set the working directory for the simulation. Uses a temporary directory by default.
    )
    if not vsp.ngspice.available():
        print("ngspice is not available. Skipping simulation.")
        return

    params = FoldedCascodeParams(
        w1_2=inp.w1_2,
        w5_6=inp.w5_6,
        w7_8=inp.w7_8,
        w9_10=inp.w9_10,
        w11_12=inp.w11_12,
        w13_14=inp.w13_14,
        w15_16=inp.w15_16,
        w17=inp.w17,
        w18=inp.w18,
        # VDD=inp.VDD,
        cl=inp.cl,
        cc=inp.cc,
        rc=inp.rc,
        wb0=inp.wb0,
        wb1=inp.wb1,
        wb2=inp.wb2,
        wb3=inp.wb3,
        wb4=inp.wb4,
        wb5=inp.wb5,
        wb6=inp.wb6,
        wb7=inp.wb7,
        wb8=inp.wb8,
        wb9=inp.wb9,
        wb10=inp.wb10,
        wb11=inp.wb11,
        wb12=inp.wb12,
        wb13=inp.wb13,
        wb14=inp.wb14,
        wb15=inp.wb15,
        wb16=inp.wb16,
        wb17=inp.wb17,
        wb18=inp.wb18,
        wb19=inp.wb19,
        ibias=inp.ibias,
        Vcm=inp.Vcm,
    )

    # Run the simulation!
    results = FoldedCascodeSim(params).run(opts)

    # Extract our metrics from those results
    ac_result = results["ac"]
    sig_out = ac_result.data["v(xtop.sig_out)"]

    gain = find_dc_gain(2 * sig_out)
    ugbw = find_ugbw(ac_result.freq, 2 * sig_out)
    phm = find_phm(ac_result.freq, 2 * sig_out)
    idd = ac_result.data["i(v.xtop.vvdc)"]
    ibias = find_I_vdd(idd)

    # And return them as an `OpAmpOutput`
    return OpAmpOutput(
        ugbw=ugbw,
        gain=gain,
        phm=phm,
        ibias=ibias,
    )


@ldo_sim.impl
def ldo_sim(inp: LDOInput) -> LDOOutput:
    """
    LDO Simulation
    """
    # TODO implement
