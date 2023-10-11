# Stdlib imports
from typing import Callable, Generic, TypeVar
from dataclasses import asdict

# PyPI imports
from pydantic.dataclasses import dataclass

# Local imports
from discovery_shared.rpc import Rpc


# FIXME When training, everything converts to float, why?
Number = float | int


@dataclass
class Range:
    min: Number
    max: Number


@dataclass
class ParamSpec:
    name: str
    range: Range
    step: Number
    init: Number


ParamSpecs = list[ParamSpec]
"""
Why not define a dataclass when we want to use different parameters?
Because it might just be too tedious to create a new dataclass
when we simply want to control which parameters to vary.
"""


@dataclass
class MetricSpec:
    name: str
    range: Range
    normalize: Number


MetricSpecs = list[MetricSpec]
"""
Why not define a dataclass when we want to achieve different specs?
Because it might just be too tedious to create a new dataclass
when we simply want to control which specs to achieve.
"""


@dataclass
class CircuitOptimization:
    params: ParamSpecs
    specs: MetricSpecs
    input_type: type
    output_type: type
    reward: Callable[
        ["Self.OutputType", dict[str, Number]],  # TODO Typing
        # TODO The input to reward can be expanded to (s_t, a_t, s_{t+1}),
        # as defined in OpenAI's Spinning Up intro to RL:
        # https://spinningup.openai.com/en/latest/spinningup/rl_intro.html#reward-and-return
        float,
    ]

    # rpc function which simulates
    simulation: Rpc


@dataclass
class AutoCktGymEnvConfig:
    circuit_optimization: CircuitOptimization
    actions_per_param: list[
        int  # TODO Here, int is number of steps. Can be more general.
    ]

    def __iter__(self):
        """
        FIXME Needs to be iterable, required by ray
        """
        yield from asdict(self).items()
