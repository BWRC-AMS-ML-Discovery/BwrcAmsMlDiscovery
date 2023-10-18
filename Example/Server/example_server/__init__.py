"""
# Example `Discovery` Server Implementation 
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
)


def example_server_start(cfg: Config):
    """Retrieve values from .env and then configure and start the server"""

    ds.configure(cfg)
    ds.start_server()


@example.impl
def example_func(example: Example) -> Example:
    """# Example RPC Implementation"""

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
