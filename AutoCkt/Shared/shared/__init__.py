"""
# Local AutoCkt Dep
Shared code
"""

# Std-Lib Imports
import pickle
import random
from typing import Optional
from collections import OrderedDict
from typing import List

# Workspace Imports
from dataclasses import dataclass, fields


@dataclass
class Spec:
    gain: float
    ibias: float
    phm: float
    ugbw: float

    def keys(self) -> List[str]:
        return [f.name for f in fields(self)]

    def values(self) -> List[float]:
        return [getattr(self, f.name) for f in fields(self)]


@dataclass
class Normalize(Spec):
    pass


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
class Params:
    mp1: Range
    mp3: Range
    mn1: Range
    mn3: Range
    mn4: Range
    mn5: Range
    cc: Range

    def keys(self) -> List[str]:
        return [f.name for f in fields(self)]

    def values(self) -> List[Range]:
        return [getattr(self, f.name) for f in fields(self)]


@dataclass
class TargetSpecs:
    gain_min: Range
    ibias_max: Range
    phm_min: Range
    ugbw_min: Range

    def keys(self) -> List[str]:
        return [f.name for f in fields(self)]

    def values(self) -> List[Range]:
        return [getattr(self, f.name) for f in fields(self)]


@dataclass
class CktInput(OrderedDict):
    params: dict[str, Range]
    normalize: dict[str, float]
    target_specs: dict[str, Range]


class ParamManager:
    """
    A Processor for Managing Parameters handling
    input and output and other mechanism inside RL script
    """

    def __init__(self):
        self.spec = Spec(0.0, 0.0, 0.0, 0.0)
        self.params = Params(
            Range(1, 100, 1),
            Range(1, 100, 1),
            Range(1, 100, 1),
            Range(1, 100, 1),
            Range(1, 100, 1),
            Range(1, 100, 1),
            Range(1, 100, 1),
        )
        self.norm = Normalize(0.0, 0.0, 0.0, 0.0)

    def load_spec(self, params: list, target: list, norm: list) -> CktInput:
        """
        params: parameters range, n# of ranges with step sizes, n * 3 for each [min, max, step]
        target: ideal spec range, n# of ranges without step sizes, n * 2 for each [min, max]
        norm: normalizing constants, 4# of constraints
        """

        params_field_names = [f.name for f in fields(Params)]
        target_field_names = [f.name for f in fields(TargetSpecs)]
        normalize_field_names = [f.name for f in fields(Normalize)]

        params_values = {
            name: Range(param[0], param[1], param[2])
            for name, param in zip(params_field_names, params)
        }
        target_values = {
            name: Range(param[0], param[1])
            for name, param in zip(target_field_names, target)
        }

        normalize_values = {
            name: value for name, value in zip(normalize_field_names, norm)
        }

        ckt = CktInput(params_values, normalize_values, target_values)

        self.params = Params(**params_values)
        self.spec = TargetSpecs(**target_values)
        self.norm = Normalize(**normalize_values)
        return ckt

    def get_spec(self) -> Spec:
        """
        return the spec for initial setup
        """
        return self.spec

    def get_param(self) -> Params:
        """
        return the parameters passed in for initial setup
        """
        return self.params

    def get_norm(self) -> Spec:
        """
        return the normalizing constants passed in for initial setup
        """
        return self.norm
