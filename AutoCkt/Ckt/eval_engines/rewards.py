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
        # ideal = float(ideal)  # Not sure if this is necessary
        relative = (curr - ideal) / (curr + ideal)
        return relative

    #adapted TwoAmp reward using new variables
    def reward(curr_output, target_output):
        curr_output_vals = list(curr_output.__dict__.values())[:4]
        output_id = list(curr_output.__dict__.keys())[:4]

        output_relative = calc_relative(curr_output_vals, target_output)

        pos_val = []
        reward = 0.0
        for i, rel_spec in enumerate(output_relative):
            if output_id[i] == "ibias_max":
                rel_spec = rel_spec * -1.0  # /10.0
            if rel_spec < 0:
                reward += rel_spec
                pos_val.append(0)
            else:
                pos_val.append(1)

        return reward if reward < -0.02 else 10

    #run the reward function
    return reward(curr_output, target_output)

