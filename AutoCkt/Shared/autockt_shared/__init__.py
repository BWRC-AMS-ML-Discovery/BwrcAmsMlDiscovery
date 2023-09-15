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


@dataclass
class AutoCktInput:
    """
    Input type for AutoCkt library, a state of result
    """

    mp1: int  # number of units of specific pmos transistor
    mn1: int  # number of units of specific nmos transistor
    mp3: int  # number of units of specific pmos transistor
    mn3: int  # number of units of specific nmos transistor
    mn4: int  # number of units of specific nmos transistor
    mn5: int  # number of units of specific nmos transistor
    cc: float  # Or maybe `str`, or the Hdl21/ VLSIR `Prefixed` fixed-point type


@dataclass
class AutoCktOutput:
    """
    Output type for AutoCkt library, a spec of circuit design
    """

    gain: float
    ugbw: float
    phm: float
    ibias: float


auto_ckt_sim = Rpc(
    name="auto_ckt_sim",
    input_type=AutoCktInput,
    return_type=AutoCktOutput,
    docstring="Simulation on the Server",
)

auto_ckt_sim_hdl21 = Rpc(
    name="auto_ckt_sim_hdl21",
    input_type=AutoCktInput,
    return_type=AutoCktOutput,
    docstring="Simulation on the Server",
)


@dataclass
class LatchInput:

    w1: int
    w2: int
    w3: int
    w4: int
    w5: int
    w6: int
    w7: int
    w8: int
    w9: int
    w10: int
    VDD: h.Scalar


@dataclass
class LatchOutput:

    power: float
    output_delay: float
    setup_time: float


latch_sim = Rpc(
    name="latch_sim",
    input_type=LatchInput,
    return_type=LatchOutput,
    docstring="Latch simulation",
)


@dataclass
class FlipFlopInput:

    l1: LatchInput
    l2: LatchInput


@dataclass
class FlipFlopOutput:

    power: float
    output_delay: float
    setup_time: float
    hold_time: float


flip_flop_sim = Rpc(
    name="flip_flop_sim",
    input_type=FlipFlopInput,
    return_type=FlipFlopOutput,
    docstring="FlipFlop simulation",
)


@dataclass
class FoldedCascodeInput:

    w1_2: int
    w5_6: int
    w7_8: int
    w9_10: int
    w11_12: int
    w13_14: int
    w15_16: int
    w17: int
    w18: int

    cl: h.Scalar
    cc: h.Scalar
    rc: h.Scalar

    wb0: int
    wb1: int
    wb2: int
    wb3: int
    wb4: int
    wb5: int
    wb6: int
    wb7: int
    wb8: int
    wb9: int
    wb10: int
    wb11: int
    wb12: int
    wb13: int
    wb14: int
    wb15: int
    wb16: int
    wb17: int
    wb18: int
    wb19: int

    ibias: h.Scalar
    Vcm: h.Scalar


@dataclass
class FoldedCascodeOutput:

    gain: float
    ugbw: float
    phm: float
    ibias: float


folded_cascode_sim = Rpc(
    name="folded_cascode_sim",
    input_type=FoldedCascodeInput,
    return_type=FoldedCascodeOutput,
    docstring="FoldedCascode simulation",
)


@dataclass
class LDOInput:

    w1: int
    w2: int
    w3: int
    w4: int
    w5: int
    w6: int
    w7r: int
    w8: int
    wc: int
    w10: int
    wpass: int
    VDD: h.Scalar
    Cc: h.Scalar
    Cf1: h.Scalar
    Cf2: h.Scalar
    Rrf1: h.Scalar
    Rrf2: h.Scalar
    ibias: h.Scalar


@dataclass
class LDOOutput:
    """
    TODO What do we get out?
    """


ldo_sim = Rpc(
    name="ldo_sim",
    input_type=LDOInput,
    return_type=LDOOutput,
    docstring="LDO simulation",
)


@dataclass
class TwoStageOpAmpNgmInput:

    wtail1: int
    wtail2: int
    wcm: int
    win: int
    wref: int
    wd1: int
    wd: int
    wn_gm: int
    wtail: int
    wtailr: int
    Cc: float
    Rf: float
    VDD: float
    Vcm: float
    Vref: float
    ibias: float


@dataclass
class TwoStageOpAmpNgmOutput:

    gain: float
    ugbw: float
    phm: float
    ibias: float


two_stage_op_amp_ngm_sim = Rpc(
    name="two_stage_op_amp_ngm_sim",
    input_type=TwoStageOpAmpNgmInput,
    return_type=TwoStageOpAmpNgmOutput,
    docstring="TwoStageOpAmpNgm simulation",
)
