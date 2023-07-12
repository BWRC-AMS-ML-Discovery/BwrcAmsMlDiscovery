"""
# Example Server
"""

# Stdlib Imports
from dataclasses import asdict

# PyPi Imports
import hdl21 as h
import vlsirtools.spice as vsp

import discovery_server as ds
from dotenv import dotenv_values

# Workspace Imports
from example_shared import (
    example,
    Example,
    secret_spice,
    SecretSpiceSimulationInput,
    SecretSpiceSimulationOutput,
    simulate_that_opamp,
    simulate_on_the_server,
    OpAmpParams,
    VlsirProtoBufKind,
    VlsirProtoBufBinary,
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
from .mocks.TwoStageOpAmp import (
    OpAmpParams as TwoStageOpAmpParams,
    OpAmpSim,
    find_dc_gain,
    find_I_vdd,
    find_phm,
    find_ugbw,
)


def example_server_start():
    """Retrieve values from .env and then configure and start the server"""

    env = dotenv_values()

    THE_SERVER_HOST = env.get("THE_SERVER_HOST", None)
    if not THE_SERVER_HOST:
        raise ValueError("THE_SERVER_HOST not set in .env file")

    THE_SERVER_PORT = env.get("THE_SERVER_PORT", None)
    if not THE_SERVER_PORT:
        raise ValueError("THE_SERVER_PORT not set in .env file")

    ds.configure(ds.Config(port=THE_SERVER_PORT, host=THE_SERVER_HOST))
    ds.start_server()


@example.impl
def example_func(example: Example) -> Example:
    """# Example RPC"""

    return Example(txt=example.txt * example.num, num=1)


@secret_spice.impl
def secret_spice_sim(inp: SecretSpiceSimulationInput) -> SecretSpiceSimulationOutput:
    """# Super-secret SPICE simulation"""

    return SecretSpiceSimulationOutput(id=5e-6)


@simulate_that_opamp.impl
async def simulate_that_opamp(params: OpAmpParams) -> VlsirProtoBufBinary:
    """# Some op-amp simulation"""

    @h.generator
    def ThatOpAmp(params: OpAmpParams) -> h.Module:
        """# That OpAmp"""

        @h.module
        class ThatOpAmp:
            VDD, VSS = h.Ports(2)
            n1 = h.Nmos(npar=params.nf_something)(d=VDD, g=VDD, s=VSS, b=VSS)

        return ThatOpAmp

    @h.module
    class Tb:
        VSS = h.Port()
        VDD = h.Signal()
        opamp = ThatOpAmp(params)(VDD=VDD, VSS=VSS)
        vdd = h.Vdc(dc=1)(p=VDD, n=VSS)

    @h.sim.sim
    class OpAmpSim:
        tb = Tb
        op = h.sim.Op()

    sim_options = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE, fmt=vsp.ResultFormat.VLSIR_PROTO
    )

    # Run that sim!!!
    somehow_this_is_a_coroutine = await OpAmpSim.run_async(opts=sim_options)
    ## FIXME: who on earth made this double-await a thing?!?
    ## Get some better tests in async-land @dan_fritchman
    sim_result = await somehow_this_is_a_coroutine

    # And bundle it up into our return type
    return VlsirProtoBufBinary(
        kind=VlsirProtoBufKind.SIM_RESULT,
        proto_bytes=sim_result.SerializeToString(),
    )


@simulate_on_the_server.impl
async def simulate_on_the_server(inp: VlsirProtoBufBinary) -> VlsirProtoBufBinary:
    """# Simulate a circuit on the server
    Decodes a `SimInput` VLSIR protobuf from `inp`, simulates it, and returns a `SimResult` VLSIR protobuf.
    """

    if inp.kind != VlsirProtoBufKind.SIM_INPUT:
        raise ValueError(f"Expected a simulation input, not {inp.kind}")

    # Got what should be a `SimInput`. First deserialize it from bytes.
    sim_input = vsp.SimInput.ParseFromString(inp.proto_bytes)
    if not isinstance(sim_input, vsp.SimInput):
        raise ValueError(f"Expected a `SimInput`, not {sim_input}")

    sim_options = vsp.SimOptions(
        simulator=vsp.SupportedSimulators.NGSPICE,  ## or your favorite simulator. or make this part of the input?
        fmt=vsp.ResultFormat.VLSIR_PROTO,
    )

    # Finally! Run the simulation!!
    sim_result = await vsp.spice.sim(sim_input, sim_options)
    ## FIXME: same "double await" as above
    sim_result = await sim_result

    # And bundle it up into our return type
    return VlsirProtoBufBinary(
        kind=VlsirProtoBufKind.SIM_RESULT,
        proto_bytes=sim_result.SerializeToString(),
    )


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
