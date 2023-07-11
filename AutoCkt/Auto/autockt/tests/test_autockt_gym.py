from autockt.autockt_gym import AutoCktGym
import IPython
from autockt.autockt_gym_env_config import (
    AutoCktCircuitOptimization,
    AutoCktGymEnvConfig,
    AutoCktParam,
    AutoCktParams,
    AutoCktSpec,
    AutoCktSpecs,
)
from eval_engines.rewards import settaluri_reward
from example_client import AutoCktInput, AutoCktOutput


def test():
    circuit_optimization = AutoCktCircuitOptimization(
        params=AutoCktParams(
            [
                AutoCktParam("mp1", (1, 100), step=1, init=34),
                AutoCktParam("mn1", (1, 100), step=1, init=34),
                AutoCktParam("mp3", (1, 100), step=1, init=34),
                AutoCktParam("mn3", (1, 100), step=1, init=34),
                AutoCktParam("mn4", (1, 100), step=1, init=34),
                AutoCktParam("mn5", (1, 100), step=1, init=15),
                AutoCktParam("cc", (0.1e-12, 10.0e-12), step=0.1e-12, init=2.1e-12),
            ]
        ),
        specs=AutoCktSpecs(  # FIXME Numbers right?
            [
                AutoCktSpec("gain", (200, 400), normalize=350),
                AutoCktSpec("ugbw", (1.0e6, 2.5e7), normalize=9.5e5),
                AutoCktSpec("phm", (60, 60.0000001), normalize=60),
                AutoCktSpec("ibias", (0.0001, 0.01), normalize=0.001),
            ]
        ),
        input_type=AutoCktInput,
        output_type=AutoCktOutput,
        reward=settaluri_reward,
    )

    gym_env_config = AutoCktGymEnvConfig(
        circuit_optimization=circuit_optimization,
        actions_per_param=[-1, 0, 2],
    )

    env = AutoCktGym(gym_env_config)
    # env.reset()
    # env.step([2, 2, 2, 2, 2, 2, 2])


def main():
    test()
    IPython.embed()


if __name__ == "__main__":
    main()
