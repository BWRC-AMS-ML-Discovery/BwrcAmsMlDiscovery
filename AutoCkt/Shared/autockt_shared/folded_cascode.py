# Std-Lib Imports
from dataclasses import dataclass

# Workspace Imports
from discovery_shared import Rpc

# Local Imports
from .opamp_output import OpAmpOutput
from .cktopt import (
    AutoCktCircuitOptimization,
    AutoCktSpec,
    AutoCktSpecs,
    AutoCktParam,
    AutoCktParams,
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


circuit_optimization = AutoCktCircuitOptimization(
    params=AutoCktParams(
        [
            AutoCktParam("w1_2", (2, 24), step=2, init=10),
            AutoCktParam("w5_6", (2, 24), step=2, init=10),
            AutoCktParam("w7_8", (2, 24), step=2, init=10),
            AutoCktParam("w9_10", (2, 24), step=2, init=10),
            AutoCktParam("w11_12", (2, 24), step=2, init=10),
            AutoCktParam("w13_14", (2, 24), step=2, init=10),
            AutoCktParam("w15_16", (2, 24), step=2, init=10),
            AutoCktParam("w17", (2, 24), step=2, init=10),
            AutoCktParam("w18", (2, 24), step=2, init=10),
            AutoCktParam("cl", (8e-15, 30e-15), step=2e-15, init=10e-15),
            AutoCktParam("cc", (2e-15, 24e-15), step=2e-15, init=10e-15),
            AutoCktParam("rc", (0.6e3, 1.7e3), step=0.1e3, init=1e3),
            AutoCktParam("wb0", (2, 24), step=2, init=10),
            AutoCktParam("wb1", (2, 24), step=2, init=10),
            AutoCktParam("wb2", (2, 24), step=2, init=10),
            AutoCktParam("wb3", (2, 24), step=2, init=10),
            AutoCktParam("wb4", (2, 24), step=2, init=10),
            AutoCktParam("wb5", (2, 24), step=2, init=10),
            AutoCktParam("wb6", (2, 24), step=2, init=10),
            AutoCktParam("wb7", (2, 24), step=2, init=10),
            AutoCktParam("wb8", (2, 24), step=2, init=10),
            AutoCktParam("wb9", (2, 24), step=2, init=10),
            AutoCktParam("wb10", (2, 24), step=2, init=10),
            AutoCktParam("wb11", (2, 24), step=2, init=10),
            AutoCktParam("wb12", (2, 24), step=2, init=10),
            AutoCktParam("wb13", (2, 24), step=2, init=10),
            AutoCktParam("wb14", (2, 24), step=2, init=10),
            AutoCktParam("wb15", (2, 24), step=2, init=10),
            AutoCktParam("wb16", (2, 24), step=2, init=10),
            AutoCktParam("wb17", (2, 24), step=2, init=10),
            AutoCktParam("wb18", (2, 24), step=2, init=10),
            AutoCktParam("wb19", (2, 24), step=2, init=10),
            AutoCktParam("ibias", (30e-6, 52e-6), step=2e-6, init=40e-6),
            AutoCktParam("Vcm", (0, 1.2), step=0.1, init=1),
        ]
    ),
    specs=AutoCktSpecs(
        [
            AutoCktSpec("gain", (200, 400), normalize=350),
            AutoCktSpec("ugbw", (1.0e6, 2.5e7), normalize=9.5e5),
            AutoCktSpec("phm", (60, 60.0000001), normalize=60),
            AutoCktSpec("ibias", (0.0001, 0.01), normalize=0.001),
        ]
    ),
    input_type=FoldedCascodeInput,
    output_type=OpAmpOutput,
    simulation=folded_cascode_sim,
    reward=folded_cascode_reward,
)
