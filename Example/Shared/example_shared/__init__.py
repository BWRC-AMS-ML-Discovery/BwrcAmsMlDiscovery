"""
# Example Discovery App
Shared server-client code
"""

# Std-Lib Imports
from enum import Enum
from typing import Optional, Tuple


# PyPi Imports
import hdl21 as h

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


@dataclass
class InverterBetaRatioInput:
    # def __init__(self, wp, wn):
    #   self.wp = wp
    #    self.wn = wn
    wp: Optional[float] = None
    wn: Optional[float] = None

    def __init__(self, params):
        if params:
            assert (
                len(params) == 2
            ), f"Number of parameters must be 2, currently there are {len(params)}"
            self.wp = params[0]
            self.wn = params[1]

    def to_vec(self) -> list:
        return [self.wp, self.wn]


@dataclass
class InverterBetaRatioOutput:
    trise: float
    tfall: float

    def to_vec(self) -> list:
        return [self.trise, self.tfall]


inverter_beta_ratio = Rpc(
    name="inverter_beta_ratio",
    input_type=InverterBetaRatioInput,
    return_type=InverterBetaRatioOutput,
    docstring="Inverter Beta Ratio",
)


# TODO Ask Dan if he made changes to these
# Because these were lost due to a merge conflict,
# and I manually copied them from a previous commit.
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
class ExampleMlInputs:
    """
    # Example ML Optimizer Inputs
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


@dataclass
class AutoCktInput:
    """
    Input type for AutoCkt library, a state of result
    """

    mp1: int  # number of units of specific pmos transistor
    mn1: int  # number of units of specific nmos transistor
    mp3: int  # number of units of specific pmos transistor
    mn3: int  # number of units of specific nmos transistor
    mn4: int  # number of units of specific nmos transistor
    mn5: int  # number of units of specific nmos transistor
    cc: float  # Or maybe `str`, or the Hdl21/ VLSIR `Prefixed` fixed-point type


@dataclass
class AutoCktOutput:
    """
    Output type for AutoCkt library, a spec of circuit design
    """

    gain: float
    ugbw: float
    phm: float
    ibias: float


auto_ckt_sim = Rpc(
    name="auto_ckt_sim",
    input_type=AutoCktInput,
    return_type=AutoCktOutput,
    docstring="Simulation on the Server",
)

auto_ckt_sim_hdl21 = Rpc(
    name="auto_ckt_sim_hdl21",
    input_type=AutoCktInput,
    return_type=AutoCktOutput,
    docstring="Simulation on the Server",
)
