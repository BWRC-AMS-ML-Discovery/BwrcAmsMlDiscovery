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
    """
    Why not define a dataclass when we want to use different parameters?
    Because it might just be too tedious when we simply want to control
    which parameters to vary.
    """

    params: list[AutoCktParam]


@dataclass
class AutoCktSpec:
    name: str
    range: Range
    normalize: Number


@dataclass
class AutoCktSpecs:
    """
    Why not define a dataclass when we want to achieve different specs?
    Because it might just be too tedious when we simply want to control
    which specs to achieve.
    """

    specs: list[AutoCktSpec]


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
