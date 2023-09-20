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
from .latch import LatchInput


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


def flip_flop_reward(
    curr_output: FlipFlopOutput,  # This is from simulation
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
        [
            ParamSpec("mp1", (1, 100), step=1, init=34),
            ParamSpec("mn1", (1, 100), step=1, init=34),
            ParamSpec("mp3", (1, 100), step=1, init=34),
            ParamSpec("mn3", (1, 100), step=1, init=34),
            ParamSpec("mn4", (1, 100), step=1, init=34),
            ParamSpec("mn5", (1, 100), step=1, init=15),
            ParamSpec("cc", (0.1e-12, 10.0e-12), step=0.1e-12, init=2.1e-12),
        ]
    ),
    specs=MetricSpecs(
        # TODO Change these
        [
            MetricSpec("delay", (0, 10e-9), normalize=1e-9),
            MetricSpec("setup_time", (0, 10e-9), normalize=1e-9),
            MetricSpec("hold_time", (0, 10e-9), normalize=1e-9),
            MetricSpec("ibias", (0, 1), normalize=1e-3),
        ]
    ),
    input_type=FlipFlopInput,
    output_type=FlipFlopOutput,
    simulation=flip_flop_sim,
    reward=flip_flop_reward,
)
