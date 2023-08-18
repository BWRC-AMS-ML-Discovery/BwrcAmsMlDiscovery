from .autockt_gym_env_config import AutoCktParams, AutoCktParam
from typing import TypeVar, Generic, Sequence
from dataclasses import asdict, is_dataclass
from shared.typing import Number

InputType = TypeVar("InputType")


class AutoCktParamsManager(Generic[InputType]):
    def __init__(
        self,
        params_ranges: AutoCktParams,
        params: InputType,
        actions_per_param: list[int],
    ):
        self.params_ranges = params_ranges
        self.flatten_init = self.flatten(params)
        print(f"-------------FLATTENED {self.flatten_init}--------------")
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

    def get_cur_params(self):
        return self.cur_params

    def flatten(self, i: InputType) -> list:  # Or maybe list
        if not is_dataclass(i):
            raise Exception  # Maybe make a few other such checks, here or elsewhere

        # Initialize the result list
        arr = []
        # Kick off our recursive flatteners
        self.flatten_dict(asdict(i), arr)
        # And return the list
        return arr

    def flatten_dict(self, d: dict[str, any], arr: list[Number]):
        """Flatten dictionary `d` into result array `arr`"""
        for (key, val) in d.items():
            if isinstance(val, dict):
                self.flatten_dict(val, arr)
            elif isinstance(val, Sequence) and not isinstance(
                val, str
            ):  # List, tuple, etc
                self.flatten_seq(val, arr)
            elif isinstance(val, (int, float)):
                arr.append(val)
            else:
                raise TypeError  # Non-numeric primitive, fail

    def flatten_seq(self, seq: Sequence, arr: list[Number]):
        """Flatten Sequence `seq` into result array `arr`"""
        for val in seq:
            if isinstance(val, Sequence) and not isinstance(val, str):
                self.flatten_seq(val, arr)
            elif isinstance(val, dict):
                self.flatten_dict(val, arr)
            elif isinstance(val, (int, float)):
                arr.append(val)
            else:
                raise TypeError
