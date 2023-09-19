from dataclasses import asdict

# PyPI imports
import numpy as np
import gym
from gym import spaces
from pydantic.tools import parse_obj_as

# Local imports
from autockt_shared.cktopt import (
    AutoCktParams,
    AutoCktSpecs,
    AutoCktGymEnvConfig,
    AutoCktCircuitOptimization,
)

from .autockt_gym_params_mng import AutoCktParamsManager
from .autockt_gym_ideal_specs_mng import SpecManager


class AutoCktGym(gym.Env):
    metadata = {
        "render.modes": ["human"],
    }

    def __init__(
        self,
        env_config: AutoCktGymEnvConfig,  # It's actually an EnvContext(dict)
    ):
        # Adapter due to Ray converting dataclass to dict
        env_config = parse_obj_as(AutoCktGymEnvConfig, env_config)

        # Extract variables
        match env_config:
            case AutoCktGymEnvConfig(
                circuit_optimization=circuit_optimization,
                actions_per_param=actions_per_param,
            ):
                match circuit_optimization:
                    case AutoCktCircuitOptimization(
                        params=params,
                        specs=specs,
                        input_type=input_type,
                        output_type=output_type,
                        simulation=simulation,
                        reward=reward,
                    ):
                        pass

        self.input_type = input_type
        self.output_type = output_type
        self.simulation = simulation
        self.reward = reward

        # create managers
        self.params_manager = AutoCktParamsManager(params, actions_per_param)
        self.spec_manager = SpecManager(specs)

        # Necessary for the gym.Env API
        self.action_space = self._build_action_space(params, actions_per_param)
        self.observation_space = self._build_observation_space(params, specs)

    def reset(self):
        # ----------------- Params -----------------
        self.params_manager.reset_to_init()
        cur_params = self.params_manager.get_cur_params()

        # ----------------- Simulation -----------------
        result = self.simulation(self.input_type(**cur_params))

        # ----------------- Specs -----------------
        self.spec_manager.update(asdict(result))
        cur_norm, ideal_norm = self.spec_manager.reset()

        # ----------------- Observation -----------------
        observation = np.concatenate(
            [
                list(cur_norm.values()),
                list(ideal_norm.values()),
                list(cur_params.values()),
            ]
        )
        return observation

    def step(self, action):
        """action: a list of actions from action space to take upon parameters"""

        # ----------------- Params -----------------
        self.params_manager.step(action)
        cur_params = self.params_manager.get_cur_params()

        # ----------------- Simulation -----------------
        result = self.simulation(self.input_type(**cur_params))

        # ----------------- Specs -----------------
        self.spec_manager.update(asdict(result))
        cur_spec, ideal_spec, cur_norm, ideal_norm = self.spec_manager.step()

        reward = self.reward(result, ideal_spec)  # calc from result and ideal_spec

        # TODO 10 is very arbitrary
        # do something related to reward
        done = reward >= 10

        # ----------------- Observation -----------------
        observation = np.concatenate(
            [
                list(cur_norm.values()),
                list(ideal_norm.values()),
                list(cur_params.values()),
            ]
        )

        # TODO update env steps

        return observation, reward, done, {}

    def _build_action_space(
        self,
        params: AutoCktParams,
        actions_per_param: list[int],
    ):
        # TODO We can generalize actions
        num_actions_per_param = len(actions_per_param)

        action_space = spaces.Dict(
            {
                param.name: spaces.Discrete(
                    num_actions_per_param,
                )
                for param in params
            }
        )

        return action_space

    def _build_observation_space(
        self,
        params: AutoCktParams,
        specs: AutoCktSpecs,
    ):
        # TODO We can observe more things
        num_fields = sum(
            [
                len(params),  # Current params in this step
                len(specs),  # Current simulated specs based on params in this step
                len(specs),  # Ideal (target) specs in this episode
            ]
        )

        # TODO Currently space is infinite
        observation_space = spaces.Box(
            low=np.full(num_fields, -np.inf),
            high=np.full(num_fields, np.inf),
        )

        return observation_space
