from .autockt_gym_env_config import AutoCktParams
from shared.typing import Number


class AutoCktParamsManager:
    def __init__(
        self,
        params_ranges: AutoCktParams,
        actions_per_param: list[int],
    ):
        self.params_ranges = params_ranges
        self.actions_per_param = actions_per_param

    def reset_to_init(self):
        """returns the init params dict for resetting the env"""
        params_init_dict = {param.name: param.init for param in self.params_ranges}
        self.cur_params = params_init_dict

    def step(self, cur_action):
        """based on action space move by action's idx"""
        # Convert to a numpy array and flatten it if it's not already 1D
        for idx, (name, _) in enumerate(self.cur_params.items()):
            action_idx = cur_action[name]
            step_update = (
                self.cur_params[name]
                + self.actions_per_param[action_idx] * self.params_ranges[idx].step
            )

            if step_update > self.params_ranges[idx].range.max:
                step_update = self.params_ranges[idx].range.max
            elif step_update < self.params_ranges[idx].range.min:
                step_update = self.params_ranges[idx].range.min

            self.cur_params[name] = step_update

    def get_cur_params(self) -> dict[str, Number]:
        return self.cur_params
