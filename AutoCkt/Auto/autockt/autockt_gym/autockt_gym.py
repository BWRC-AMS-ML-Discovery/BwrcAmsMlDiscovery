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


class AutoCktGym(gym.Env):
    metadata = {
        "render.modes": ["human"],
    }

    def __init__(self, env_config: AutoCktGymEnvConfig):
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

        # Necessary for the gym.Env API
        self._build_action_space(params, actions_per_param)
        self._build_observation_space(params, specs)

    def reset(self):
        pass

    def step(self, action):
        pass

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
            len(params),  # Current params in this step
            len(specs),  # Current simulated specs based on params in this step
            len(specs),  # Ideal (target) specs in this episode
        )

        # TODO Currently space is infinite
        self.observation_space = spaces.Box(
            low=np.full(num_fields, -np.inf),
            high=np.full(num_fields, np.inf),
        )
