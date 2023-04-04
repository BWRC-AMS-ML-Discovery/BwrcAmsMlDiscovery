"""
# Discovery 
Shared server-client code
"""

# Local Imports
import hdl21 as h
from .dataclasses import dataclass
from hdl21.sim import *

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
class TestSimInput:
    """# Input for Circuit Module to be built in HDL21"""

    def __init__(self, new_name, new_i, new_o, new_s):
        self.name = new_name
        self.i = new_i
        self.o = new_o
        self.s = new_s

@dataclass
class TestOutput:
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
class SpiceInput:
    """# Input for spice in hdl21"""

    def __init__(self, pkg, top, opt, an, ctrls):
        self.top = top
        self.pkg = pkg
        self.opt = opt
        self.an = an
        self.ctrls = ctrls

@dataclass
class SpiceOutput:
    """# Output for spice in hdl21"""

    def __init__(self, sim_input):
        self.r = h.Sim(pkg = sim_input.pkg, top = sim_input.top, opts = sim_input.opts, an = sim_input.an, ctrls = sim_input.ctrls)
        self.i = h.Input()
        self.o = h.Output(width=module_input.o)
        self.s = h.Signal()

    def tostring(self):
        return (f'Type: TestSpiceSimOutput\n'
                f'Attributes:\n'
                f'  Name: {self.m}\n'
                f'  SpiceOutput: {self.r}\n'
                f'  o: {self.o}')
