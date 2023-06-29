from .autockt_gym_env_config import AutoCktParams, AutoCktSpecs
import numpy as np


class AutoCktParamsManager:
    def __init__(self, params, action):
        self.params_ranges = params
        self.action_space = action

    def reset_to_init(self):
        """returns the init params dict for resetting the env"""
        params_init_dict = {param.name: param.init for param in self.params_ranges}
        self.cur_params = params_init_dict

    def step(self, cur_action):
        """based on action space move by action's idx"""
        # Convert to a numpy array and flatten it if it's not already 1D
        cur_action = list(np.array(cur_action).flatten())
        update_actions = [self.action_space[i] for i in cur_action]

        for idx, (name, _) in enumerate(self.cur_params.items()):
            step_update = self.cur_params[name] + update_actions[idx]
            if (
                step_update <= self.params_ranges[idx].range.max
                and step_update >= self.params_ranges[idx].range.min
            ):
                self.cur_params[name] = step_update

    def get_cur_params(self):
        return self.cur_params
