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
    VDD: int


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


def latch_reward(
    curr_output: LatchOutput,  # This is from simulation
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
        [
            AutoCktParam("w1", (1, 100), step=1, init=10),
            AutoCktParam("w2", (1, 100), step=1, init=20),
            AutoCktParam("w3", (1, 100), step=1, init=10),
            AutoCktParam("w4", (1, 100), step=1, init=20),
            AutoCktParam("w5", (1, 100), step=1, init=10),
            AutoCktParam("w6", (1, 100), step=1, init=20),
            AutoCktParam("w7", (1, 100), step=1, init=20),
            AutoCktParam("w8", (1, 100), step=1, init=20),
            AutoCktParam("w9", (1, 100), step=1, init=10),
            AutoCktParam("w10", (1, 100), step=1, init=10),
        ]
    ),
    specs=AutoCktSpecs(
        # TODO Change these
        [
            AutoCktSpec("delay", (0, 10e-9), normalize=1e-9),
            AutoCktSpec("setup_time", (0, 10e-9), normalize=1e-9),
            AutoCktSpec("hold_time", (0, 10e-9), normalize=1e-9),
            AutoCktSpec("ibias", (0, 1), normalize=1e-3),
        ]
    ),
    input_type=LatchInput,
    output_type=LatchOutput,
    simulation=latch_sim,
    reward=latch_reward,
)
