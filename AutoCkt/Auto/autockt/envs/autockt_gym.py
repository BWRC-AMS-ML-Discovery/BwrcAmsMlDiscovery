# PyPI imports
import gym


class AutoCktGym(gym.Env):
    metadata = {
        "render.modes": ["human"],
    }

    def __init__(self, env_config):
        # Custom attributes (not from gym.Env)
        pass
