# Std-Lib Imports
from dataclasses import dataclass

# Workspace Imports
from discovery_shared import Rpc

# Local Imports
from .cktopt import (
    AutoCktCircuitOptimization,
    AutoCktSpec,
    AutoCktSpecs,
    AutoCktParam,
    AutoCktParams,
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


circuit_optimization = AutoCktCircuitOptimization(
    params=AutoCktParams(
        # TODO Change these
        # TODO Action space for length of MOS (14nm, 100nm, 200nm)
        [
            AutoCktParam("w1", (1, 40), step=1, init=10),
            AutoCktParam("w2", (1, 40), step=1, init=10),
            AutoCktParam("w3", (1, 40), step=1, init=10),
            AutoCktParam("w4", (1, 40), step=1, init=10),
            AutoCktParam("w5", (1, 40), step=1, init=10),
            AutoCktParam("w6", (1, 40), step=1, init=10),
            AutoCktParam("w7r", (1, 40), step=1, init=10),
            AutoCktParam("w8", (1, 40), step=1, init=10),
            AutoCktParam("w9", (1, 40), step=1, init=10),
            AutoCktParam("w10", (1, 40), step=1, init=10),
            AutoCktParam("wpass", (1, 40), step=1, init=10),
            AutoCktParam("w1", (1, 40), step=1, init=10),
            AutoCktParam("w1", (1, 40), step=1, init=10),
            AutoCktParam("w1", (1, 40), step=1, init=10),
            AutoCktParam("w1", (1, 40), step=1, init=10),
            AutoCktParam("mn1", (1, 40), step=1, init=34),
            AutoCktParam("mp3", (1, 40), step=1, init=34),
            AutoCktParam("mn3", (1, 40), step=1, init=34),
            AutoCktParam("mn4", (1, 40), step=1, init=34),
            AutoCktParam("mn5", (1, 40), step=1, init=15),
            AutoCktParam("cc", (0.1e-12, 10.0e-12), step=0.1e-12, init=2.1e-12),
        ]
    ),
    specs=AutoCktSpecs(
        # TODO Change these
        [
            AutoCktSpec("gain", (1, 2), normalize=1.5),
            AutoCktSpec("ugbw", (1.0e6, 2.5e7), normalize=9.5e5),
            AutoCktSpec("phm", (60, 60.0000001), normalize=60),
            AutoCktSpec("ibias", (0.0001, 0.01), normalize=0.001),
        ]
    ),
    input_type=LDOInput,
    output_type=LDOOutput,
    simulation=ldo_sim,
    reward=ldo_reward,
)
