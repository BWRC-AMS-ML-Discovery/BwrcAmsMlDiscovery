"""
# Discovery Client
"""

# Std-Lib Imports
from dataclasses import asdict

# PyPi Imports
import hdl21 as h
from dotenv import dotenv_values
import httpx

# Local Imports
from ..shared import (
    Example,
    SecretSpiceSimulationInput,
    SecretSpiceSimulationOutput,
    OpAmpParams,
    VlsirProtoBufBinary,
    VlsirProtoBufKind,
    InverterBetaRatioInput,
    InverterBetaRatioOutput,
)
from ..shared.git import GitInfo

# Load the .env file
env = dotenv_values()

# And get the server URL
THE_SERVER_URL = env.get("THE_SERVER_URL", None)
if not THE_SERVER_URL:
    raise ValueError("THE_SERVER_URL not set in .env file")


def alive() -> str:
    """Server aliveness check"""
    resp = httpx.get(f"http://{THE_SERVER_URL}/")
    return resp.text


def version() -> GitInfo:
    """Server version"""
    resp = httpx.get(f"http://{THE_SERVER_URL}/version")
    print(resp)
    return GitInfo(**resp.json())


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
