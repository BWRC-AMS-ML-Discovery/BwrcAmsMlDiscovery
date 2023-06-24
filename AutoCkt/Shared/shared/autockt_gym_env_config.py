# Stdlib imports
from typing import Callable

# PyPI imports
from pydantic.dataclasses import dataclass


Number = int | float


@dataclass
class Range:
    min: Number
    max: Number


@dataclass
class AutoCktParam:
    name: str
    range: Range


@dataclass
class AutoCktParams:
    pass


@dataclass
class AutoCktSpec:
    name: str
    range: Range


@dataclass
class AutoCktSpecs:
    pass


@dataclass
class AutoCktGymEnvConfig:
    params: AutoCktParams
    specs: AutoCktSpecs
    input_type: type
    output_type: type
    reward: Callable[[TODO], float]
