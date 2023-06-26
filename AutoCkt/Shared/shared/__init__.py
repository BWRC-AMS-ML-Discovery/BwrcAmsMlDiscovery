"""
# Local AutoCkt Dep
Shared code

FIXME This folder should be renamed to autockt_shared
"""

# Std-Lib Imports
from typing import Optional, Union
from collections import OrderedDict
from typing import List, Callable, Type
from shared.typing import Number

# Workspace Imports
from dataclasses import dataclass, fields


@dataclass
class Range:
    min: float | int
    max: float | int
    step: Optional[float | int] = None

    def __iter__(self):
        """iter tool for looping."""
        value = self.min
        if self.step is None:
            step = self.max - self.min
        else:
            step = self.step
        while value <= self.max:
            yield value
            value += step

    def get_value_at_index(self, index):
        """Return the value at the specified index."""
        if index == 0:
            return self.min
        elif index == -1:
            return self.max
        else:
            return self.min + index * (
                self.step if self.step is not None else (self.max - self.min)
            )

    def __len__(self):
        """Return the total number of steps from min to max."""
        if self.step is None:
            return (
                1  # When step is None, we assume only one value, i.e., from min to max
            )
        else:
            return int((self.max - self.min) / self.step) + 1


@dataclass
class Spec:
    ranges: dict[str, Range]


@dataclass
class Normalize:
    constants: dict[str, Union[float, int]]


@dataclass
class Params:
    ranges: dict[str, Range]


@dataclass
class TargetSpecs:
    ranges: dict[str, Range]


@dataclass
class CktInput:
    params: Params
    normalize: Normalize
    target_specs: TargetSpecs


@dataclass
class CircuitOptimization:
    #auto ckt input and output
    param : Params
    specs : Spec
    target_specs : Spec

    #clients input and output 
    input_type: Type
    output_type: Type

    #reward function to be used by RL model
    reward_fnc: Callable[["Self.OutputType", dict[str, Number]], float]

    #assume auto is of type spec maybe change this
    def specs_to_output_type(self, specs, output_type):
        curr_output = output_type(       
            ugbw = specs[0],
            gain = specs[1],
            phm = specs[2],
            ibias = specs[3]
        )
        return curr_output

    def __call__(self, *args, **kwargs):
        #some convertion operation to go from what the ml model has to the client reward function's expected input
        self.specs = kwargs['cur_spec']
        self.target_specs = kwargs['specs_ideal']

        #convert between types
        curr_output = self.auto_ckt_to_output_type(self.specs, self.output_type)

        #do other convertions as well before passing to reward func

        return self.reward_fnc(curr_output, self.target_specs)

