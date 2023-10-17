from copy import deepcopy
from typing import TypeVar, Generic, Sequence
from dataclasses import asdict, is_dataclass

from autockt_shared.cktopt import ParamSpecs, Number

InputType = TypeVar("InputType")


class ParamSpecsManager(Generic[InputType]):
    def __init__(
        self,
        params_ranges: ParamSpecs,
        actions_per_param: list[int],
    ):
        self.params_template = deepcopy(params_ranges)
        self.params_ranges = self.flatten_init(params_ranges)
        self.actions_per_param = actions_per_param

    def reset_to_init(self):
        """returns the init params dict for resetting the env"""
        params_init_dict = {param.name: param.init for param in self.params_template}
        self.cur_params = params_init_dict

    def step(self, cur_action):
        """based on action space move by action's idx"""
        # Convert to a numpy array and flatten it if it's not already 1D
        # for idx, (name, _) in enumerate(self.cur_params.items()):
        #     action_idx = cur_action[name]
        #     step_update = (
        #         self.cur_params[name]
        #         + self.actions_per_param[action_idx] * self.params_template[idx].step
        #     )

        #     if step_update > self.params_template[idx].range.max:
        #         step_update = self.params_template[idx].range.max
        #     elif step_update < self.params_template[idx].range.min:
        #         step_update = self.params_template[idx].range.min

        #     self.cur_params[name] = step_update

        for idx, param_metrics in enumerate(self.params_ranges):
            ##params_ranges: [1.0, 100.0, 1.0, 34.0], each are mix, max, step, init
            min = param_metrics[0]
            max = param_metrics[1]
            step = param_metrics[2]
            init = param_metrics[3]
            name = self.params_template[idx].name
            action_idx = cur_action[name]
            step_update = (
                self.cur_params[name] + self.actions_per_param[action_idx] * step
            )
            if step_update > max:
                step_update = max
            elif step_update < min:
                step_update = min

            self.cur_params[name] = step_update

    def get_cur_params(self):
        return self.cur_params

    def flatten_init(self, l: list) -> list:
        res = []
        for ele in l:
            res.append(self.flatten(ele))
        return res

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
        for key, val in d.items():
            if isinstance(val, dict):
                self.flatten_dict(val, arr)
            # todo from sequence to list and tuple
            elif isinstance(val, str):
                continue
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
