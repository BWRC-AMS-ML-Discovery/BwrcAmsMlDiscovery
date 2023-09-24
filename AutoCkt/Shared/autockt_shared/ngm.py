# Std-Lib Imports
from typing import Optional, Union
from dataclasses import dataclass

# Workspace Imports
from discovery_shared import Rpc

# Local Imports
from .opamp_output import OpAmpOutput
from .cktopt import (
    CircuitOptimization,
    MetricSpec,
    MetricSpecs,
    ParamSpec,
    ParamSpecs,
    Number,
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


two_stage_op_amp_ngm_sim = Rpc(
    name="two_stage_op_amp_ngm_sim",
    input_type=TwoStageOpAmpNgmInput,
    return_type=OpAmpOutput,
    docstring="TwoStageOpAmpNgm simulation",
)


def two_stage_op_amp_ngm_reward(
    curr_output: OpAmpOutput,  # This is from simulation
    target_output: dict[str, Number],  # This is from Specs
):
    """
    TODO Implement
    """

    def calc_relative(curr: Number, ideal: Number):
        # ideal = float(ideal)  # Not sure if this is necessary
        relative = curr / ideal
        return relative

    # adapted TwoAmp reward using new variables
    def reward(curr_output, target_output):
        # populate relative for each key input of target
        pos_val = []
        reward = 1.0
        for key in target_output:
            reward = reward * calc_relative(
                getattr(curr_output, key),
                target_output[key],
            )

        # TODO this 10 seems pretty arbitrary
        return reward

    # run the reward function
    return reward(curr_output, target_output)


circuit_optimization = CircuitOptimization(
    params=ParamSpecs(
        # TODO Double Check these
        [
            ParamSpec("wtail1", (4, 20), step=2, init=10),
            ParamSpec("wtail2", (4, 20), step=2, init=10),
            ParamSpec("wcm", (4, 20), step=2, init=10),
            ParamSpec("win", (4, 20), step=2, init=10),
            ParamSpec("wref", (4, 20), step=2, init=10),
            ParamSpec("wd1", (4, 20), step=2, init=10),
            ParamSpec("wd", (4, 20), step=2, init=10),
            ParamSpec("wn_gm", (4, 20), step=2, init=10),
            ParamSpec("wtail", (4, 20), step=2, init=10),
            ParamSpec("wtailr", (4, 20), step=2, init=10),
            ParamSpec("Cc", (10e-15, 150e-15), step=5e-15, init=10e-15),
            ParamSpec("Rf", (0.1e3, 6e3), step=0.1e3, init=1e3),
        ]
    ),
    specs=MetricSpecs(
        # TODO Double Check these
        [
            MetricSpec("gain", (1, 40), normalize=10),
            MetricSpec("ugbw", (1.0e6, 2.5e7), normalize=9.5e5),
            MetricSpec("phm", (60, 75), normalize=60),
            MetricSpec("ibias", (0.0001, 0.01), normalize=0.001),
        ]
    ),
    input_type=TwoStageOpAmpNgmInput,
    output_type=OpAmpOutput,
    simulation=two_stage_op_amp_ngm_sim,
    reward=two_stage_op_amp_ngm_reward,
)
