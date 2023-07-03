from example_client import AutoCktOutput
from shared.typing import Number


# TODO: remove target_output, can be assumed from rl model
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

    # adapted TwoAmp reward using new variables
    def reward(curr_output, target_output):
        # populate relative for each key input of target
        output_relative = {}
        for key in target_output:
            output_relative[key] = calc_relative(
                getattr(curr_output, key), target_output[key]
            )

        pos_val = []
        reward = 0.0
        for key in output_relative:
            rel_spec = output_relative[key]
            if key == "ibias":
                rel_spec = rel_spec * -1.0  # /10.0
            if rel_spec < 0:
                reward += rel_spec
                pos_val.append(0)
            else:
                pos_val.append(1)

        return reward if reward < -0.02 else 10

    # run the reward function
    return reward(curr_output, target_output)
