"""
# Example Discovery App
Shared server-client code
"""


# Workspace Imports
from discovery_shared.dataclasses import dataclass
from discovery_shared.rpc import Rpc


@dataclass
class Example:
    """# Example of a dataclass that can be used as a POST body"""

    txt: str
    num: int


example = Rpc(
    name="example",
    input_type=Example,
    return_type=Example,
    docstring="Example RPC",
)


@dataclass
class SecretSpiceSimulationInput:
    """# Input to a very secret SPICE simulation"""

    w: int  # Width
    l: int  # Length
    v: int  # Voltage (mV)


@dataclass
class SecretSpiceSimulationOutput:
    """# Output from a very secret SPICE simulation"""

    id: float  # Id (A)


secret_spice = Rpc(
    name="secret_spice",
    input_type=SecretSpiceSimulationInput,
    return_type=SecretSpiceSimulationOutput,
    docstring="Secret SPICE simulation",
)


class VlsirProtoBufKind(Enum):
    """# VLSIR ProtoBuf Kind
    Enumerated types for `VlsirProtoBufBinary` data."""

    CKT_PACKAGE = "CKT_PACKAGE"  # Circuit Package
    SIM_INPUT = "SIM_INPUT"  # SimInput
    SIM_RESULT = "SIM_RESULT"  # SimResult


@dataclass
class VlsirProtoBufBinary:
    """# VLSIR ProtoBuf-Encoded Binary Data"""

    kind: VlsirProtoBufKind
    proto_bytes: bytes


@h.paramclass
class OpAmpParams:
    nf_something = h.Param(dtype=int, desc="Number of fingers of something", default=2)


simulate_that_opamp = Rpc(
    name="simulate_that_opamp",
    input_type=OpAmpParams,
    return_type=VlsirProtoBufBinary,
    docstring="Some op-amp simulation",
)


@dataclass
class SampleMlInputs:
    """
    # Sample ML Optimizer Inputs
    Now you can have inputs to your ML thing like so:
    """

    input_range: Tuple[int, int]
    initial_value_of_something: float

    # The point here: the objective function can be an `Rpc`
    the_objective_function: Rpc


simulate_on_the_server = Rpc(
    name="simulate_on_the_server",
    input_type=VlsirProtoBufBinary,
    return_type=VlsirProtoBufBinary,
    docstring="Simulation on the Server",
)
