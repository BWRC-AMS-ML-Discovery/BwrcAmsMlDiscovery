from typing import Type, Callable
from eval_engines.rewards import (
    settaluri_reward,
)

from shared.typing import Number

from dataclasses import dataclass, fields

@dataclass
class EvalEnginesConfig:
    PARAMS_RANGE : list
    NORM_CONSTANT : list
    TARGET_RANGE : list

    def __init__(self):
        self.PARAMS_RANGE = [
            ["mp1", [1, 100, 1]],
            ["mp3", [1, 100, 1]],
            ["mn1", [1, 100, 1]],
            ["mn3", [1, 100, 1]],
            ["mn4", [1, 100, 1]],
            ["mn5", [1, 100, 1]],
            ["cc", [1, 100, 1]],
        ]
        self.NORM_CONSTANT = [["gain", 350], ["ibias", 0.001], ["phm", 60], ["ugbw", 950000.0]]
        self.TARGET_RANGE = [
            ["gain_min", [200, 400]],
            ["ibias_max", [1.0e6, 2.5e7]],
            ["phm_min", [60, 60.0000001]],
            ["ugbw_min", [0.0001, 0.01]],
        ]

    def get_params_range(self):
        return self.PARAMS_RANGE
    
    def get_norm_constant(self):
        return self.NORM_CONSTANT
    
    def get_target_range(self):
        return self.TARGET_RANGE

config = EvalEnginesConfig()

