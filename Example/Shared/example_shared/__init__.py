"""
# Example Discovery App
Shared server-client code
"""

# Std-Lib Imports
from typing import Optional


# PyPi Imports

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
