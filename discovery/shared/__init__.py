"""
# Discovery 
Shared server-client code
"""

# Local Imports
from .dataclasses import dataclass
from typing import Optional


@dataclass
class Example:
    """# Example of a dataclass that can be used as a POST body"""

    txt: str
    num: int


@dataclass
class ObjParams:
    """# Object for parameters"""

    w: int  # Width
    l: int  # Length
    v: int  # Voltage (mV)
    #x1: Optional[int] = 0
    #x2: Optional[int] = 0
    #x3: Optional[str] = "Default"


@dataclass
class Measurements:
    """# Output from a very secret SPICE simulation"""

    m1: float  # Measurement 1
    m2: float  # Measurement 2
    mtype: Optional[str] = None # Measurement type

@dataclass
class GenList:
    """# Output list of generators"""

    gens: list  # List of generators

@dataclass
class Topology:
    """# Output Topology"""

    topology: str # Topology



