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
class Param:
    name: str
    range: Range


@dataclass
class Params:
    pass


@dataclass
class Specs:
    pass


@dataclass
class AutoCktGymEnvConfig:
    params: Params
    specs: Specs
    input_type: type
    output_type: type
    reward: Callable[[], float]
