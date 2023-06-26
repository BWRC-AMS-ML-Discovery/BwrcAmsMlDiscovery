from example_client import AutoCktOutput
from shared.typing import Number


def settaluri_reward(
    curr_output: AutoCktOutput,  # This is from simulation
    target_output: dict[str, Number],  # This is from Specs
):
    """
    Reward: doesn't penalize for overshooting spec, is negative
    """

    def calc_relative(curr: Number, ideal: Number):
        ideal = float(ideal)  # Not sure if this is necessary
        relative = (curr - ideal) / (curr + ideal)
        return relative

    # FIXME
    raise NotImplementedError
