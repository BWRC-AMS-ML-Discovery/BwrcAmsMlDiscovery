# Std-Lib Imports
from dataclasses import asdict

# PyPi Imports
from dotenv import dotenv_values
import hdl21 as h

# Workspace Imports
from example_shared import (
    example,
    Example,
    secret_spice,
    SecretSpiceSimulationInput,
    SecretSpiceSimulationOutput,
    simulate_that_opamp,
    OpAmpParams,
    VlsirProtoBufKind,
    VlsirProtoBufBinary,
    inverter_beta_ratio,
    InverterBetaRatioInput,
    InverterBetaRatioOutput,
    simulate_on_the_server,
    auto_ckt_sim,
    auto_ckt_sim_hdl21,
    AutoCktInput,
    AutoCktOutput,
)

# The client library will create client stubs for all defined RPCs, including all those functions above.
import discovery_client as dc


# FIXME Maybe put this variable somewhere else?
ENABLE_HTTP = False
if not ENABLE_HTTP:
    dc.client_start = lambda: None
    # Short-circuiting by directly calling server functions
    import example_server as _


def example_client_start():
    """retrieve values from .env file then configure nad start the client"""

    # Load the .env file
    env = dotenv_values()

    # And get the server URL
    THE_SERVER_URL = env.get("THE_SERVER_URL", None)
    if not THE_SERVER_URL:
        raise ValueError("THE_SERVER_URL not set in .env file")

    # set server_url
    dc.configure(dc.Config(server_url=THE_SERVER_URL))
    dc.client_start()


"""
Now we can just call the RPCs as though they were implemented locally.
"""


def test_auto_ckt():
    """testing auto ckt rpcs"""
    to_test = AutoCktInput(3, 3, 3, 3, 3, 3, 1e-12)
    test = auto_ckt_sim(to_test)
    return test


def do_simple_example():
    example_resp = example(Example(txt="Hello", num=3))
    return example_resp


def do_example_stuff():
    """# Call a few example RPCs"""
    example_resp = example(Example(txt="Hello", num=3))
    print(example_resp)

    secret_spice_resp = secret_spice(SecretSpiceSimulationInput(w=1, l=2, v=3))
    print(secret_spice_resp)

    simulate_that_opamp_resp = simulate_that_opamp(OpAmpParams(nf_something=3))
    print(simulate_that_opamp_resp)


# FIXME needs renaming to avoid the same name
def simulate_that_opamp(params: OpAmpParams) -> h.sim.SimResultProto:
    """# Run the `ThatOpAmp` generator and simulate it, all on the server"""

    # Call our RPC function
    protos: VlsirProtoBufBinary = simulate_that_opamp(params)

    # Got some data back! Decode it from protobuf into a `SimResultProto`.
    sim_result = h.sim.SimResultProto.ParseFromString(protos.proto_bytes)
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
    from_the_server: VlsirProtoBufBinary = simulate_on_the_server(send_me_to_server)

    # Got some data back! Decode it from protobuf into a `SimResultProto`.
    sim_result = h.sim.SimResultProto.ParseFromString(from_the_server.proto_bytes)
    return sim_result


def local_inverter_beta_ratio(inp: InverterBetaRatioInput):
    wp = inp.wp
    wn = inp.wn
    output = (wp - 23) ** 2 + (wn - 4) ** 2
    return InverterBetaRatioOutput(
        trise=output / 2,
        tfall=output / 2,
    )
