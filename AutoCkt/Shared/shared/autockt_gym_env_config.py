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
    step: Number


@dataclass
class AutoCktParams:
    params: dict[str, AutoCktParam]


@dataclass
class AutoCktSpec:
    name: str
    range: Range
    normalize: Number


@dataclass
class AutoCktSpecs:
    specs: dict[str, AutoCktSpec]


@dataclass
class AutoCktGymEnvConfig:
    params: AutoCktParams
    specs: AutoCktSpecs
    input_type: type
    output_type: type
    reward: Callable[
        [AutoCktSpec, AutoCktSpec],
        # TODO The input to reward can be expanded to (s_t, a_t, s_{t+1}),
        # as defined in OpenAI's Spinning Up intro to RL:
        # https://spinningup.openai.com/en/latest/spinningup/rl_intro.html#reward-and-return
        float,
    ]
