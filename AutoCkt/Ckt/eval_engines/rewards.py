from example_client import AutoCktOutput
from shared.typing import Number
import numpy as np


# TODO: remove target_output, can be assumed from rl model
def settaluri_reward(
    curr_output: AutoCktOutput,  # This is from simulation
    target_output: dict[str, Number],  # This is from Specs
):
    """
    Reward: doesn't penalize for overshooting spec, is negative
    """
    # FIXME a func here, unbounded
    if (
        curr_output.ugbw > something
    ):  # constraints like this, need to be randomly generated
        return -reward
    fom = (
        np.log(curr_output.ugbw)
        * curr_output.phm
        * curr_output.gain
        / curr_output.ibias
        * (-1.0)
    )

    def calc_relative(curr: Number, ideal: Number):
        # ideal = float(ideal)  # Not sure if this is necessary
        relative = (curr - ideal) / (curr + ideal)
        return relative

    # adapted TwoAmp reward using new variables
    def reward(curr_output, target_output):
        # populate relative for each key input of target
        output_relative = {}
        # print(f"curr output {curr_output}  target_output {target_output}")
        for key in target_output:
            output_relative[key] = calc_relative(
                getattr(curr_output, key),  # curr_output[key],
                target_output[key],
            )
        pos_val = []
        reward = 0.0
        for key in output_relative:
            rel_spec = output_relative[key]

            if key == "ibias":
                rel_spec = rel_spec * -1.0
                # /10.0
            if rel_spec < 0:
                reward += rel_spec
                pos_val.append(0)
            else:
                pos_val.append(1)
        # reward, pos_val = fom_calculator(output_relative, pos_val, reward)

        # TODO this 10 seems pretty arbitrary
        return reward

    # run the reward function
    return reward(curr_output, target_output)


def fom_calculator(output_relative, pos_val=[], reward=0.0):
    # TODO this fom can be changed to other fom metrics
    for key in output_relative:
        rel_spec = output_relative[key]

        if key == "ibias":
            rel_spec = rel_spec * -1.0
            # /10.0
        if rel_spec < 0:
            reward += rel_spec
            pos_val.append(0)
        else:
            pos_val.append(1)
    # log for bandwidth
    return reward, pos_val
