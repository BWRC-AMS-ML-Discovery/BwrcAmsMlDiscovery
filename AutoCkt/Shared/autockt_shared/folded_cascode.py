# Std-Lib Imports
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

    cl: int
    cc: int
    rc: int

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

    ibias: int
    Vcm: int


folded_cascode_sim = Rpc(
    name="folded_cascode_sim",
    input_type=FoldedCascodeInput,
    return_type=OpAmpOutput,
    docstring="FoldedCascode simulation",
)


def folded_cascode_reward(
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
        [
            ParamSpec("w1_2", (2, 24), step=2, init=10),
            ParamSpec("w5_6", (2, 24), step=2, init=10),
            ParamSpec("w7_8", (2, 24), step=2, init=10),
            ParamSpec("w9_10", (2, 24), step=2, init=10),
            ParamSpec("w11_12", (2, 24), step=2, init=10),
            ParamSpec("w13_14", (2, 24), step=2, init=10),
            ParamSpec("w15_16", (2, 24), step=2, init=10),
            ParamSpec("w17", (2, 24), step=2, init=10),
            ParamSpec("w18", (2, 24), step=2, init=10),
            ParamSpec("cl", (8e-15, 30e-15), step=2e-15, init=10e-15),
            ParamSpec("cc", (2e-15, 24e-15), step=2e-15, init=10e-15),
            ParamSpec("rc", (0.6e3, 1.7e3), step=0.1e3, init=1e3),
            ParamSpec("wb0", (2, 24), step=2, init=10),
            ParamSpec("wb1", (2, 24), step=2, init=10),
            ParamSpec("wb2", (2, 24), step=2, init=10),
            ParamSpec("wb3", (2, 24), step=2, init=10),
            ParamSpec("wb4", (2, 24), step=2, init=10),
            ParamSpec("wb5", (2, 24), step=2, init=10),
            ParamSpec("wb6", (2, 24), step=2, init=10),
            ParamSpec("wb7", (2, 24), step=2, init=10),
            ParamSpec("wb8", (2, 24), step=2, init=10),
            ParamSpec("wb9", (2, 24), step=2, init=10),
            ParamSpec("wb10", (2, 24), step=2, init=10),
            ParamSpec("wb11", (2, 24), step=2, init=10),
            ParamSpec("wb12", (2, 24), step=2, init=10),
            ParamSpec("wb13", (2, 24), step=2, init=10),
            ParamSpec("wb14", (2, 24), step=2, init=10),
            ParamSpec("wb15", (2, 24), step=2, init=10),
            ParamSpec("wb16", (2, 24), step=2, init=10),
            ParamSpec("wb17", (2, 24), step=2, init=10),
            ParamSpec("wb18", (2, 24), step=2, init=10),
            ParamSpec("wb19", (2, 24), step=2, init=10),
            ParamSpec("ibias", (30e-6, 52e-6), step=2e-6, init=40e-6),
            ParamSpec("Vcm", (0, 1.2), step=0.1, init=1),
        ]
    ),
    specs=MetricSpecs(
        [
            MetricSpec("gain", (200, 400), normalize=350),
            MetricSpec("ugbw", (1.0e6, 2.5e7), normalize=9.5e5),
            MetricSpec("phm", (60, 60.0000001), normalize=60),
            MetricSpec("ibias", (0.0001, 0.01), normalize=0.001),
        ]
    ),
    input_type=FoldedCascodeInput,
    output_type=OpAmpOutput,
    simulation=folded_cascode_sim,
    reward=folded_cascode_reward,
)
