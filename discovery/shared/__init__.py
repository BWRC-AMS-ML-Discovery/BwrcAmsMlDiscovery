"""
# Discovery 
Shared server-client code
"""

# Local Imports
from .dataclasses import dataclass
#import hdl21 as h


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

"""# HDL Raw Polygon Schema"""

@dataclass
class PointInput:
    def __init__(self, x, y):
        self.x = x
        self.y = y

@dataclass
class PointOutput:
    def __init__(self, point):
        self.x = point.x
        self.y = point.y

    def __str__(self):
        return (f'Type: PointOutput\n'
                f'Attributes:\n'
                f'  x: {self.x}\n'
                f'  y: {self.y}')



@dataclass
class LayerInput:
    def __init__(self, number, purpose):
        self.x = number
        self.y = purpose

@dataclass
class LayerOutput:
    def __init__(self, point):
        self.x = point.number
        self.y = point.purpose

    def __str__(self):
        return (f'Type: LayerOutput\n'
                f'Attributes:\n'
                f'  x: {self.number}\n'
                f'  y: {self.purpose}')

'''
@dataclass
class RectangeInput:

@dataclass
class RectangleOutput:


@dataclass
class PolygonInput:

@dataclass
class PolygonOutput:


@dataclass
class PathInput:

@dataclass
class PathOutput:


@dataclass
class LayerShapesInput:

@dataclass
class LayerShapesOutput:


@dataclass
class TextElementInput:

@dataclass
class TextElementOutput:


@dataclass
class InstanceInput:

@dataclass
class InstanceOutput:


@dataclass
class LayoutInput:

@dataclass
class LayoutOutput:


@dataclass
class AbstractInput:

@dataclass
class AbstractOutput:


@dataclass
class AbstractPortInput:

@dataclass
class AbstractPortOutput:


@dataclass
class CellInput:

@dataclass
class CellOutput:


@dataclass
class LibraryInput:

@dataclass
class LibraryOutput:'''