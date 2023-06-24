# PyPI imports
import gym

# Local imports
from shared.autockt_gym_env_config import AutoCktGymEnvConfig


class AutoCktGym(gym.Env):
    metadata = {
        "render.modes": ["human"],
    }

    def __init__(self, env_config: AutoCktGymEnvConfig):
        # Custom attributes (not from gym.Env)
        pass
