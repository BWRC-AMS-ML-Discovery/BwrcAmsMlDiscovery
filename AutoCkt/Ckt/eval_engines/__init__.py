from typing import Type, Callable

from shared import (
    CircuitOptimization
)

from dataclasses import dataclass, fields

@dataclass
class EvalEnginesConfig:
    PARAMS_RANGE : list
    NORM_CONSTANT : list
    TARGET_RANGE : list
    CIRCUIT_OPT : CircuitOptimization

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

        self.CIRCUIT_OPT = None

    def get_params_range(self):
        return self.PARAMS_RANGE
    
    def get_norm_constant(self):
        return self.NORM_CONSTANT
    
    def get_target_range(self):
        return self.TARGET_RANGE
    
    def get_circuit_opt(self):
        return self.CIRCUIT_OPT

    def create_circuit_optimization(self, input:Type, output:Type, reward:Callable):
        self.CIRCUIT_OPT = CircuitOptimization(
            ckt_input_type= input,
            ckt_output_type= output,
            reward_fnc = reward,
        )


config = EvalEnginesConfig()
