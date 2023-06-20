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


@dataclass
class StepSize:
    step: float | int


@dataclass
class ParamRange:
    range: Range
    step: Optional[StepSize]


@dataclass
class Params:
    mp1: ParamRange
    mp3: ParamRange
    mn1: ParamRange
    mn3: ParamRange
    mn4: ParamRange
    mn5: ParamRange
    cc: ParamRange


@dataclass
class TargetSpecs:
    gain_min: ParamRange
    ibias_max: ParamRange
    phm_min: ParamRange
    ugbw_min: ParamRange


@dataclass
class CktInput:
    params: Params
    normalize: Normalize
    target_specs: TargetSpecs


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

        params_values = {
            name: ParamRange(
                Range(param["range"][0], param["range"][1]),
                StepSize(param["step"]) if "step" in param else 1,
            )
            for name, param in zip(params_field_names, params)
        }

        target_values = {
            name: ParamRange(Range(param["range"][0], param["range"][1]))
            for name, param in zip(target_field_names, target)
        }

        ckt = CktInput(
            Params(**params_values), Normalize(*norm), TargetSpecs(**target_values)
        )

        return ckt
