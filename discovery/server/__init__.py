"""
# Discovery Server
"""

# PyPi Imports
import hdl21 as h
import vlsirtools.spice as vsp
from fastapi import FastAPI, Body

# Local Imports
from ..shared import (
    Example,
    SecretSpiceSimulationInput,
    SecretSpiceSimulationOutput,
    OpAmpParams,
    VlsirProtoBufKind,
    VlsirProtoBufBinary,
)
from ..shared.git import GitInfo


app = FastAPI(
    debug=False,
    title="BWRC AMS ML CktGym",
    description="BWRC AMS ML CktGym",
    version="0.0.1",
)


@app.get("/")
async def alive() -> str:
    """# The root entry point
    Just an indication that the server is alive and can be reached."""

    return "bwrc_ams_ml_discovery_server_alive"


@app.get("/version")
async def version() -> GitInfo:
    """# Get the server git version info"""

    return GitInfo.get()


@app.post("/example")
async def example(example: Example = Body(...)) -> Example:
    """# Example POST RPC endpoint"""

    return Example(txt=example.txt * example.num, num=1)


@app.post("/secret_spice_sim")
async def secret_spice_sim(
    _inp: SecretSpiceSimulationInput = Body(...),
) -> SecretSpiceSimulationOutput:
    """# Super-secret SPICE simulation"""

    return SecretSpiceSimulationOutput(id=5e-6)


@app.post("/simulate_that_opamp")
async def simulate_that_opamp(
    params: OpAmpParams = Body(...),
) -> VlsirProtoBufBinary:
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


@app.post("/simulate_on_the_server")
async def simulate_on_the_server(
    inp: VlsirProtoBufBinary = Body(...),
) -> VlsirProtoBufBinary:
    """# Simulate a circuit on the server
    Decodes a `SimInput` VLSIR protobuf from `inp`, simulates it, and returns a `SimResult` VLSIR protobuf."""

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
