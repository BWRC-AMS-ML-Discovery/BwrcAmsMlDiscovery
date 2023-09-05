"""
# Example Server
"""

# Stdlib Imports
from dataclasses import asdict

# PyPi Imports
import hdl21 as h
import vlsirtools.spice as vsp

import discovery_server as ds
from discovery_server import Config
from dotenv import dotenv_values

# Workspace Imports
from example_shared import (
    FlipFlopInput,
    FlipFlopOutput,
    FoldedCascodeInput,
    FoldedCascodeOutput,
    LDOInput,
    LDOOutput,
    LatchInput,
    LatchOutput,
    TwoStageOpAmpNgmInput,
    TwoStageOpAmpNgmOutput,
    latch_sim,
    flip_flop_sim,
    folded_cascode_sim,
    ldo_sim,
    two_stage_op_amp_ngm_sim,
    example,
    Example,
    inverter_beta_ratio,
    InverterBetaRatioInput,
    InverterBetaRatioOutput,
    auto_ckt_sim,
    auto_ckt_sim_hdl21,
    AutoCktInput,
    AutoCktOutput,
)
from .auto_ckt_sim_lib import (
    create_design,
    simulate,
    translate_result,
)
from .TwoStageOpAmp import (
    OpAmpParams as TwoStageOpAmpParams,
    OpAmpSim,
    find_dc_gain,
    find_I_vdd,
    find_phm,
    find_ugbw,
)


def example_server_start(cfg: Config):
    """Retrieve values from .env and then configure and start the server"""

    ds.configure(cfg)
    ds.start_server()


@example.impl
def example_func(example: Example) -> Example:
    """# Example RPC"""

    return Example(txt=example.txt * example.num, num=1)


@inverter_beta_ratio.impl
async def inverter_beta_ratio(inp: InverterBetaRatioInput) -> InverterBetaRatioOutput:
    """# Super-elaborate inverter beta ratio simulation"""
    wp = inp.wp
    wn = inp.wn
    the_ratio = 1.2

    # TODO implement

    # Mock a paraboloid
    output = (wp - 3) ** 2 + (wn - 4) ** 2
    return InverterBetaRatioOutput(
        trise=output / 2,
        tfall=output / 2,
    )


# FIXME should be async? FastAPI says both are ok.
@auto_ckt_sim.impl
def auto_ckt_sim(inp: AutoCktInput) -> AutoCktOutput:
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


@auto_ckt_sim_hdl21.impl
def auto_ckt_sim_hdl21(inp: AutoCktInput) -> AutoCktOutput:
    """
    AutoCkt Simulation
    """
    if not vsp.ngspice.available():
        raise RuntimeError

    # Convert our input into `OpAmpParams`
    # FIXME Is this correct?
    params = TwoStageOpAmpParams(
        wp1=inp.mp1,
        wn1=inp.mn1,
        wp3=inp.mp3,
        wn3=inp.mn3,
        wn4=inp.mn4,
        wn5=inp.mn5,
        Cc=inp.cc,
        # FIXME Extra, don't need?
        wp2=inp.mp1,
        wn2=inp.mn1,
    )

    # Create a set of simulation input for it
    sim_input = OpAmpSim(params)
    print(sim_input)
    print(params)

    # Simulation options
    opts = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE,
        fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
        rundir="./scratch",  # Set the working directory for the simulation. Uses a temporary directory by default.
    )

    # Run the simulation!
    results = sim_input.run(opts)

    # Extract our metrics from those results
    ac_result = results["ac"]
    sig_out = ac_result.data["v(xtop.sig_out)"]
    gain = find_dc_gain(2 * sig_out)
    ugbw = find_ugbw(ac_result.freq, 2 * sig_out)
    phm = find_phm(ac_result.freq, 2 * sig_out)
    idd = ac_result.data["i(v.xtop.vvdc)"]
    ibias = find_I_vdd(idd)

    # And return them as an `AutoCktOutput`
    return AutoCktOutput(
        ugbw=ugbw,
        gain=gain,
        phm=phm,
        ibias=ibias,
    )


@latch_sim.impl
def latch_sim(inp: LatchInput) -> LatchOutput:
    """
    Latch Simulation
    """
    # TODO implement


@flip_flop_sim.impl
def flip_flop_sim(inp: FlipFlopInput) -> FlipFlopOutput:
    """
    FlipFlop Simulation
    """
    # TODO implement


from .FoldedCascode import (
    FoldedCascodeParams,
    FoldedCascodeSim,
    find_dc_gain,
    find_I_vdd,
    find_phm,
    find_ugbw,
)


@folded_cascode_sim.impl
def folded_cascode_sim(inp: FoldedCascodeInput) -> FoldedCascodeOutput:
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

    params = ngmOpAmpParams(
        w15_16=inp.w15_16,
        w5_6=inp.w5_6,
        w2_8=inp.w2_8,
        w9_10=inp.w9_10,
        w11_12=inp.w11_12,
        w13_14=inp.w13_14,
        w17=inp.w17,
        w1_2=inp.w1_2,
        w7_8=inp.w7_8,
        w18=inp.w18,
        VDD=inp.VDD,
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

    # And return them as an `FoldedCascodeOutput`
    return FoldedCascodeOutput(
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


from .TwoStageOpAmp_ngm import (
    ngmOpAmpParams,
    ngmOpAmpSim,
    find_dc_gain,
    find_I_vdd,
    find_phm,
    find_ugbw,
)


@two_stage_op_amp_ngm_sim.impl
def two_stage_op_amp_ngm_sim(inp: TwoStageOpAmpNgmInput) -> TwoStageOpAmpNgmOutput:
    """
    TwoStageOpAmpNgm Simulation
    """
    opts = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE,
        fmt=vsp.ResultFormat.SIM_DATA,  # Get Python-native result types
        rundir="./scratch",  # Set the working directory for the simulation. Uses a temporary directory by default.
    )
    if not vsp.ngspice.available():
        print("ngspice is not available. Skipping simulation.")
        return

    # Run the simulation!
    params = ngmOpAmpParams(
        wtail1=inp.wtail1,
        wtail2=inp.wtail2,
        wcm=inp.wcm,
        win=inp.win,
        wref=inp.wref,
        wd1=inp.wd1,
        wd=inp.wd,
        wn_gm=inp.wn_gm,
        wtail=inp.wtail,
        wtailr=inp.wtailr,
        VDD=inp.vdd,
        Cc=inp.Cc,
        Rf=inp.Rf,
        Vcm=inp.Vcm,
        Vref=inp.Vref,
        ibias=inp.ibias,
    )
    sim_input = ngmOpAmpSim(params)

    # Run the simulation!
    results = sim_input.run(opts)

    # Extract our metrics from those results
    ac_result = results["ac"]
    sig_out = ac_result.data["v(xtop.sig_out)"]

    gain = find_dc_gain(2 * sig_out)
    ugbw = find_ugbw(ac_result.freq, 2 * sig_out)
    phm = find_phm(ac_result.freq, 2 * sig_out)
    idd = ac_result.data["i(v.xtop.vvdc)"]
    ibias = find_I_vdd(idd)

    # And return them as an `TwoStageOpAmpNgmOutput`
    return TwoStageOpAmpNgmOutput(
        ugbw=ugbw,
        gain=gain,
        phm=phm,
        ibias=ibias,
    )
