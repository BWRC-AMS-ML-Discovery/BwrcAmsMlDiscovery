"""
# Local AutoCkt Dep
Shared code
"""

# Std-Lib Imports
from typing import Optional

# Workspace Imports
from dataclasses import dataclass, fields


@dataclass
class Spec:
    gain: float
    ibias: float
    phm: float
    ugbw: float


@dataclass
class Normalize(Spec):
    pass


@dataclass
class Range:
    min: float | int
    max: float | int
    step: Optional[float | int] = None


@dataclass
class Params:
    mp1: Range
    mp3: Range
    mn1: Range
    mn3: Range
    mn4: Range
    mn5: Range
    cc: Range


@dataclass
class TargetSpecs:
    gain_min: Range
    ibias_max: Range
    phm_min: Range
    ugbw_min: Range


@dataclass
class CktInput:
    params: dict[str, Range]
    normalize: dict[str, float]
    target_specs: dict[str, Range]


class ParamManager:
    """
    A Processor for Managing Parameters handling
    input and output and other mechanism inside RL script
    """

    def input_spec(params: list, target: list, norm: list) -> CktInput:
        """
        params: parameters range, n# of ranges with step sizes, n * 3 for each [min, max, step]
        target: ideal spec range, n# of ranges without step sizes, n * 2 for each [min, max]
        norm: normalizing constants, 4# of constraints
        """

        params_field_names = [f.name for f in fields(Params)]
        target_field_names = [f.name for f in fields(TargetSpecs)]
        normalize_field_names = [f.name for f in fields(Normalize)]

        params_values = {
            name: {
                "min": param[0],
                "max": param[1],
                "step": param[2] if len(param) == 3 else None,
            }
            for name, param in zip(params_field_names, params)
        }

        target_values = {
            name: {
                "min": param[0],
                "max": param[1],
            }
            for name, param in zip(target_field_names, target)
        }

        normalize_values = {
            name: value for name, value in zip(normalize_field_names, norm)
        }

        ckt = CktInput(params_values, normalize_values, target_values)

        return ckt
