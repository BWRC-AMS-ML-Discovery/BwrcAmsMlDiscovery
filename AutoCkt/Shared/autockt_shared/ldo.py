# Std-Lib Imports
from dataclasses import dataclass

# Workspace Imports
from discovery_shared import Rpc

# Local Imports
from .cktopt import (
    CircuitOptimization,
    MetricSpec,
    MetricSpecs,
    ParamSpec,
    ParamSpecs,
    Number,
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
    VDD: int
    Cc: int
    Cf1: int
    Cf2: int
    Rrf1: int
    Rrf2: int
    ibias: int


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


def ldo_reward(
    curr_output: LDOOutput,  # This is from simulation
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
        # TODO Change these
        # TODO Action space for length of MOS (14nm, 100nm, 200nm)
        [
            ParamSpec("w1", (1, 40), step=1, init=10),
            ParamSpec("w2", (1, 40), step=1, init=10),
            ParamSpec("w3", (1, 40), step=1, init=10),
            ParamSpec("w4", (1, 40), step=1, init=10),
            ParamSpec("w5", (1, 40), step=1, init=10),
            ParamSpec("w6", (1, 40), step=1, init=10),
            ParamSpec("w7r", (1, 40), step=1, init=10),
            ParamSpec("w8", (1, 40), step=1, init=10),
            ParamSpec("w9", (1, 40), step=1, init=10),
            ParamSpec("w10", (1, 40), step=1, init=10),
            ParamSpec("wpass", (1, 40), step=1, init=10),
            ParamSpec("w1", (1, 40), step=1, init=10),
            ParamSpec("w1", (1, 40), step=1, init=10),
            ParamSpec("w1", (1, 40), step=1, init=10),
            ParamSpec("w1", (1, 40), step=1, init=10),
            ParamSpec("mn1", (1, 40), step=1, init=34),
            ParamSpec("mp3", (1, 40), step=1, init=34),
            ParamSpec("mn3", (1, 40), step=1, init=34),
            ParamSpec("mn4", (1, 40), step=1, init=34),
            ParamSpec("mn5", (1, 40), step=1, init=15),
            ParamSpec("cc", (0.1e-12, 10.0e-12), step=0.1e-12, init=2.1e-12),
        ]
    ),
    specs=MetricSpecs(
        # TODO Change these
        [
            MetricSpec("gain", (1, 2), normalize=1.5),
            MetricSpec("ugbw", (1.0e6, 2.5e7), normalize=9.5e5),
            MetricSpec("phm", (60, 60.0000001), normalize=60),
            MetricSpec("ibias", (0.0001, 0.01), normalize=0.001),
        ]
    ),
    input_type=LDOInput,
    output_type=LDOOutput,
    simulation=ldo_sim,
    reward=ldo_reward,
)
