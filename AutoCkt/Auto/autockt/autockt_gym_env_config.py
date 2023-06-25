# Stdlib imports
from typing import Callable, Generic, TypeVar

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
    step: Number
    init: Number


AutoCktParams = list[AutoCktParam]
"""
Why not define a dataclass when we want to use different parameters?
Because it might just be too tedious to create a new dataclass
when we simply want to control which parameters to vary.
"""


@dataclass
class AutoCktSpec:
    name: str
    range: Range
    normalize: Number


AutoCktSpecs = list[AutoCktSpec]
"""
Why not define a dataclass when we want to achieve different specs?
Because it might just be too tedious to create a new dataclass
when we simply want to control which specs to achieve.
"""


@dataclass
class AutoCktCircuitOptimization:
    params: AutoCktParams
    specs: AutoCktSpecs
    input_type: type
    output_type: type
    reward: Callable[
        ["Self.OutputType", "Self.OutputType"],  # TODO Typing
        # TODO The input to reward can be expanded to (s_t, a_t, s_{t+1}),
        # as defined in OpenAI's Spinning Up intro to RL:
        # https://spinningup.openai.com/en/latest/spinningup/rl_intro.html#reward-and-return
        float,
    ]


@dataclass
class AutoCktGymEnvConfig:
    circuit_optimization: AutoCktCircuitOptimization
    actions_per_param: list[
        int  # TODO Here, int is number of steps. Can be more general.
    ]
