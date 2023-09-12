"""
# Example Discovery App
Shared server-client code
"""

# Std-Lib Imports
from typing import Optional


# PyPi Imports

# Workspace Imports
from discovery_shared.dataclasses import dataclass
from discovery_shared.rpc import Rpc


@dataclass
class Example:
    """# Example of a dataclass that can be used as a POST body"""

    txt: str
    num: int


example = Rpc(
    name="example",
    input_type=Example,
    return_type=Example,
    docstring="Example RPC",
)


@dataclass
class InverterBetaRatioInput:
    # def __init__(self, wp, wn):
    #   self.wp = wp
    #    self.wn = wn
    wp: Optional[float] = None
    wn: Optional[float] = None

    def __init__(self, params):
        if params:
            assert (
                len(params) == 2
            ), f"Number of parameters must be 2, currently there are {len(params)}"
            self.wp = params[0]
            self.wn = params[1]

    def to_vec(self) -> list:
        return [self.wp, self.wn]


@dataclass
class InverterBetaRatioOutput:
    trise: float
    tfall: float

    def to_vec(self) -> list:
        return [self.trise, self.tfall]


inverter_beta_ratio = Rpc(
    name="inverter_beta_ratio",
    input_type=InverterBetaRatioInput,
    return_type=InverterBetaRatioOutput,
    docstring="Inverter Beta Ratio",
)


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
    """
    TODO What do we wanna vary?
    """

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


@dataclass
class LatchOutput:
    """
    TODO What do we get out?
    """


latch_sim = Rpc(
    name="latch_sim",
    input_type=LatchInput,
    return_type=LatchOutput,
    docstring="Latch simulation",
)


@dataclass
class FlipFlopInput:
    """
    TODO Is this correct?
    """

    l1: LatchInput
    l2: LatchInput


@dataclass
class FlipFlopOutput:
    """
    TODO What do we get out?
    """


flip_flop_sim = Rpc(
    name="flip_flop_sim",
    input_type=FlipFlopInput,
    return_type=FlipFlopOutput,
    docstring="FlipFlop simulation",
)


@dataclass
class FoldedCascodeInput:
    """
    TODO What do we wanna vary?
    """

    w15_16: int
    w5_6: int
    w2_8: int
    w9_10: int
    w11_12: int
    w13_14: int
    w17: int
    w1_2: int
    w7_8: int
    w18: int


@dataclass
class FoldedCascodeOutput:
    """
    TODO What do we get out?
    """


folded_cascode_sim = Rpc(
    name="folded_cascode_sim",
    input_type=FoldedCascodeInput,
    return_type=FoldedCascodeOutput,
    docstring="FoldedCascode simulation",
)


@dataclass
class LDOInput:
    """
    TODO What do we wanna vary?
    """

    w1a: int
    w1b: int
    w2a: int
    w2b: int
    w3: int
    w4a: int
    w4b: int


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
    """
    TODO What do we wanna vary?
    """

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


@dataclass
class TwoStageOpAmpNgmOutput:
    """
    TODO What do we get out?
    """


two_stage_op_amp_ngm_sim = Rpc(
    name="two_stage_op_amp_ngm_sim",
    input_type=TwoStageOpAmpNgmInput,
    return_type=TwoStageOpAmpNgmOutput,
    docstring="TwoStageOpAmpNgm simulation",
)
