# Std-Lib Imports
from dataclasses import asdict

# PyPi Imports
from dotenv import dotenv_values
import httpx
import hdl21 as h

# Workspace Imports
import discovery_client
import example_shared

from example_shared import (
    Example,
    SecretSpiceSimulationInput,
    SecretSpiceSimulationOutput,
    OpAmpParams,
    VlsirProtoBufBinary,
    VlsirProtoBufKind,
    InverterBetaRatioInput,
    InverterBetaRatioOutput,
)

"""
# Get all the `Shared` functions as RPCs
"""

discovery_client.something(some_rpcs_we_import)


def example(example: Example) -> Example:
    """Example POST endpoint"""
    resp = httpx.post(f"http://{THE_SERVER_URL}/example", json=asdict(example))
    return Example(**resp.json())


def secret_spice_sim(inp: SecretSpiceSimulationInput) -> SecretSpiceSimulationOutput:
    """Invoke a (very secret) SPICE simulation"""
    resp = httpx.post(f"http://{THE_SERVER_URL}/secret_spice_sim", json=asdict(inp))
    return SecretSpiceSimulationOutput(**resp.json())


def simulate_that_opamp(params: OpAmpParams) -> h.sim.SimResultProto:
    """# Run the `ThatOpAmp` generator and simulate it, all on the server"""

    # Send our request to the server
    resp = httpx.post(
        f"http://{THE_SERVER_URL}/simulate_that_opamp", json=asdict(params)
    )
    print(resp.text)
    resp = VlsirProtoBufBinary(**resp.json())

    # Got some data back! Decode it from protobuf into a `SimResultProto`.
    sim_result = h.sim.SimResultProto.ParseFromString(resp.proto_bytes)
    print(sim_result)
    return sim_result


def elaborate_that_opamp_here_and_simulate_on_the_server(
    params: OpAmpParams,
) -> h.sim.SimResultProto:
    """# Run `ThatOpAmp` generator here, and send the result to the server for simulation"""

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
        opamp = ThatOpAmp(params=params)(VDD=VDD, VSS=VSS)
        vdd = h.Vdc(dc=1)(p=VDD, n=VSS)

    @h.sim.sim
    class OpAmpSim:
        tb = Tb
        op = h.sim.Op()

    # Turn it into VLSIR protobuf
    proto_python_objects = h.sim.to_proto(OpAmpSim)
    proto_bytes = proto_python_objects.SerializeToString()
    send_me_to_server = VlsirProtoBufBinary(
        kind=VlsirProtoBufKind.SIM_INPUT, proto_bytes=proto_bytes
    )

    # And figure out how to send it to the server
    from_the_server: VlsirProtoBufBinary = httpx.post(
        f"http://{THE_SERVER_URL}/simulate_on_the_server",
        json=asdict(send_me_to_server),
    )

    # Got some data back! Decode it from protobuf into a `SimResultProto`.
    sim_result = h.sim.SimResultProto.ParseFromString(from_the_server.proto_bytes)
    print(sim_result)
    return sim_result


def inverter_beta_ratio(inp: InverterBetaRatioInput) -> InverterBetaRatioOutput:
    """Invoke a (very secret) SPICE simulation"""
    resp = httpx.post(f"http://{THE_SERVER_URL}/inverter_beta_ratio", json=asdict(inp))
    return InverterBetaRatioOutput(**resp.json())


def local_inverter_beta_ratio(inp: InverterBetaRatioInput):
    wp = inp.wp
    wn = inp.wn
    output = (wp - 23) ** 2 + (wn - 4) ** 2
    return InverterBetaRatioOutput(
        trise=output / 2,
        tfall=output / 2,
    )
