from autockt.autockt_gym import AutoCktGym
import IPython
from autockt.autockt_gym_env_config import (
    CircuitOptimization,
    AutoCktGymEnvConfig,
    ParamSpec,
    ParamSpecs,
    MetricSpec,
    MetricSpecs,
)
from dotenv import dotenv_values
from eval_engines.rewards import settaluri_reward
from example_client import (
    AutoCktInput,
    AutoCktOutput,
    auto_ckt_sim,
    example_client_start,
    Config,
)


def _test_https() -> AutoCktGym:
    env = dotenv_values()

    # And get the server URL
    THE_SERVER_URL = env.get("THE_SERVER_URL", None)
    if not THE_SERVER_URL:
        raise ValueError("THE_SERVER_URL not set in .env file")
    cfg = Config(server_url=THE_SERVER_URL, enable_https=True)

    example_client_start(cfg)

    circuit_optimization = CircuitOptimization(
        params=ParamSpecs(
            [
                ParamSpec("mp1", (1, 100), step=1, init=34),
                ParamSpec("mn1", (1, 100), step=1, init=34),
                ParamSpec("mp3", (1, 100), step=1, init=34),
                ParamSpec("mn3", (1, 100), step=1, init=34),
                ParamSpec("mn4", (1, 100), step=1, init=34),
                ParamSpec("mn5", (1, 100), step=1, init=15),
                ParamSpec("cc", (0.1e-12, 10.0e-12), step=0.1e-12, init=2.1e-12),
            ]
        ),
        specs=MetricSpecs(  # FIXME Numbers right?
            [
                MetricSpec("gain", (200, 400), normalize=350),
                MetricSpec("ugbw", (1.0e6, 2.5e7), normalize=9.5e5),
                MetricSpec("phm", (60, 60.0000001), normalize=60),
                MetricSpec("ibias", (0.0001, 0.01), normalize=0.001),
            ]
        ),
        input_type=AutoCktInput,
        output_type=AutoCktOutput,
        simulation=auto_ckt_sim,
        reward=settaluri_reward,
    )

    gym_env_config = AutoCktGymEnvConfig(
        circuit_optimization=circuit_optimization,
        actions_per_param=[-1, 0, 2],
    )

    env = AutoCktGym(gym_env_config)

    env.reset()
    env.step(
        {
            "mp1": 0,
            "mn1": 1,
            "mp3": 2,
            "mn3": 0,
            "mn4": 1,
            "mn5": 2,
            "cc": 0,
        }
    )

    return env


def main():
    env = _test_https()

    IPython.embed()


if __name__ == "__main__":
    main()
