from .autockt_gym_env_config import AutoCktParams
from shared.typing import Number


class AutoCktParamsManager:
    def __init__(self, params_ranges: AutoCktParams):
        self.params_ranges = params_ranges

    def reset_to_init(self):
        """returns the init params dict for resetting the env"""
        params_init_dict = {param.name: param.init for param in self.params_ranges}
        self.cur_params = params_init_dict

    def step(self, cur_action: list[Number]):
        """based on action space move by action's idx"""
        # Convert to a numpy array and flatten it if it's not already 1D
        for idx, (name, _) in enumerate(self.cur_params.items()):
            step_update = self.cur_params[name] + cur_action[name]
            if (
                step_update <= self.params_ranges[idx].range.max
                and step_update >= self.params_ranges[idx].range.min
            ):
                self.cur_params[name] = step_update

    def get_cur_params(self) -> dict:
        return self.cur_params
