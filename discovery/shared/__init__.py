"""
# Discovery
Shared server-client code
"""

# Local Imports
import hdl21 as h
from .dataclasses import dataclass


@dataclass
class Example:
    """# Example of a dataclass that can be used as a POST body"""

    txt: str
    num: int

@dataclass
class TestModuleInput:
    """# Input for Circuit Module to be built in HDL21"""

    def __init__(self, new_name, new_i, new_o, new_s):
        self.name = new_name
        self.i = new_i
        self.o = new_o
        self.s = new_s

@dataclass
class TestModuleOutput:
    """# Output for Circuit Module to be built in HDL21"""

    def __init__(self, module_input):
        self.m = h.Module(name=module_input.name)
        self.i = h.Input()
        self.o = h.Output(width=module_input.o)
        self.s = h.Signal()

    def tostring(self):
        return (f'Type: TestModuleOutput\n'
                f'Attributes:\n'
                f'  Name: {self.m}\n'
                f'  o: {self.o}')



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
