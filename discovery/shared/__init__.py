"""
# Discovery 
Shared server-client code
"""

# Std-Lib Imports
from enum import Enum

# PyPi Imports
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
