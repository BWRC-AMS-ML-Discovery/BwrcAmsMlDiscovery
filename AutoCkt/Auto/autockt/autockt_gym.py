# PyPI imports
import numpy as np
import gym
from gym import spaces

# Local imports
from .autockt_gym_env_config import (
    AutoCktParams,
    AutoCktSpecs,
    AutoCktGymEnvConfig,
    AutoCktCircuitOptimization,
)

from .autockt_gym_ideal_specs_mng import SpecManager


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
        #create spec manager
        self.sm = SpecManager(specs)

        # Necessary for the gym.Env API
        self._build_action_space(params, actions_per_param)
        self._build_observation_space(params, specs)


    def reset(self):
        params = None #get from param manager
        cur_norm, ideal_norm = self.sm.reset(params)
        self.ob = np.concatenate(
            [cur_norm, ideal_norm, params]
        )
        return self.ob

    def step(self, action):
        params = None #get from param manager
        cur_spec, ideal_spec, cur_norm, ideal_norm = self.sm.step(params)
        reward = None #calc from cur_spec and ideal_spec

        done = False
        #do something related to reward 

        self.ob = np.concatenate(
            [cur_norm, ideal_norm, params]
        )
        
        #update env steps

        return self.ob, reward, done, {}

    def _build_action_space(
        self,
        params: AutoCktParams,
        actions_per_param: list[int],
    ):
        # TODO We can generalize actions
        num_actions_per_param = len(actions_per_param)

        self.action_space = spaces.Dict(
            {
                param.name: spaces.Discrete(
                    num_actions_per_param,
                )
                for param in params
            }
        )

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
        self.observation_space = spaces.Box(
            low=np.full(num_fields, -np.inf),
            high=np.full(num_fields, np.inf),
        )
