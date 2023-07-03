# PyPI imports
import numpy as np
import gym
from gym import spaces
from autockt.envs.create_design_and_simulate_lib import create_design_and_simulate

# Local imports
from .autockt_gym_env_config import (
    AutoCktParams,
    AutoCktSpecs,
    AutoCktGymEnvConfig,
    AutoCktCircuitOptimization,
)

from .autockt_gym_params_mng import AutoCktParamsManager
from .autockt_gym_ideal_specs_mng import SpecManager
from shared.typing import Number


class AutoCktGym(gym.Env):
    metadata = {
        "render.modes": ["human"],
    }

    def __init__(
        self,
        env_config: AutoCktGymEnvConfig,  # FIXME It's actually an EnvContext(dict)
    ):
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
                        reward=reward,
                    ):
                        pass
        # create spec manager
        self.params_manager = AutoCktParamsManager(params, actions_per_param)
        self.sm = SpecManager(specs)

        # Necessary for the gym.Env API
        self.action_space = self._build_action_space(params, actions_per_param)
        self.observation_space = self._build_observation_space(params, specs)

    def reset(self):
        # ----------------- Params -----------------
        # reset parameters to init value
        self.params_manager.reset_to_init()
        # get parameters
        cur_params = self.params_manager.get_cur_params()

        # ----------------- Specs -----------------
        cur_norm, ideal_norm = self.sm.reset(cur_params)
        self.ob = np.concatenate([cur_norm, ideal_norm, cur_params])
        return self.ob

    def step(self, action):
        """action: a list of actions from action space to take upon parameters"""

        # ----------------- Params -----------------
        # def step(self, action: list[Number]):
        # update parameters by each action
        self.params_manager.step(action)
        # retrieve current parameters
        cur_params = self.params_manager.get_cur_params()

        # ----------------- Specs -----------------
        cur_spec, ideal_spec, cur_norm, ideal_norm = self.sm.step(cur_params)
        reward = None  # calc from cur_spec and ideal_spec

        done = False
        # do something related to reward

        self.ob = np.concatenate([cur_norm, ideal_norm, cur_params])

        # update env steps

        return self.ob, reward, done, {}

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

    def update(self, params_dict):
        """returns the updated sim results of specs"""
        # run param vals and simulate
        result = create_design_and_simulate(params_dict)
        cur_specs = np.array(list(result.values()))
        return cur_specs
