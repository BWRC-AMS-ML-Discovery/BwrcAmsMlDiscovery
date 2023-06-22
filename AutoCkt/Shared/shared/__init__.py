"""
# Local AutoCkt Dep
Shared code
"""

# Std-Lib Imports
from typing import Optional, Union
from collections import OrderedDict
from typing import List

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

