"""
# Discovery 
Shared server-client code
"""

import hdl21 as h

# Local Imports
from .dataclasses import dataclass


@dataclass
class Example:
    """# Example of a dataclass that can be used as a POST body"""

    txt: str
    num: int


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


@dataclass
class InverterBetaRatioInput:
    wp: float
    wn: float


@dataclass
class InverterBetaRatioOutput:
    trise: float
    tfall: float
