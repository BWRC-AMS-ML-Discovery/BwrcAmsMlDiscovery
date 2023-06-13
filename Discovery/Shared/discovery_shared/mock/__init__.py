# Local Imports
from ..dataclasses import dataclass


@dataclass
class MockInverterBetaRatioInput:
    wp: float
    wn: float


@dataclass
class MockInverterBetaRatioOutput:
    trise: float
    tfall: float
