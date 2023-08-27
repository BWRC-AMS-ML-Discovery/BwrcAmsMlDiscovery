# Std-Lib Imports
from dataclasses import asdict

# PyPi Imports
from dotenv import dotenv_values
import hdl21 as h

# Workspace Imports
from sample_shared import (
    sample,
    Sample,
    secret_spice,
    SecretSpiceSimulationInput,
    SecretSpiceSimulationOutput,
    simulate_that_opamp,
    OpAmpParams,
    VlsirProtoBufKind,
    VlsirProtoBufBinary,
)

# The client library will create client stubs for all defined RPCs, including all those functions above.
import discovery_client as dc
from discovery_client import Config


def sample_client_start(cfg: Config):
    """retrieve values from .env file then configure nad start the client"""

    dc.configure(cfg)

    if cfg.enable_https:
        dc.client_start()
    else:
        # Short-circuiting by directly calling server functions
        import sample_server as _


"""
Now we can just call the RPCs as though they were implemented locally.
"""


def do_simple_sample():
    sample_resp = sample(Sample(txt="Hello", num=3))
    return sample_resp


def do_sample_stuff():
    """# Call a few sample RPCs"""
    sample_resp = sample(Sample(txt="Hello", num=3))
    print(sample_resp)

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
