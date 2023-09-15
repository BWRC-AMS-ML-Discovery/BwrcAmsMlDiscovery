from autockt.autockt_gym import AutoCktGym
import IPython
from autockt_shared.cktopt import (
    AutoCktCircuitOptimization,
    AutoCktGymEnvConfig,
    AutoCktParam,
    AutoCktParams,
    AutoCktSpec,
    AutoCktSpecs,
)
from dotenv import dotenv_values
from autockt_shared.rewards import settaluri_reward
from autockt import (
    OpAmpInput,
    OpAmpOutput,
    auto_ckt_sim,
    start_client,
    Config,
)


def _test_https() -> AutoCktGym:
    env = dotenv_values()

    # And get the server URL
    THE_SERVER_URL = env.get("THE_SERVER_URL", None)
    if not THE_SERVER_URL:
        raise ValueError("THE_SERVER_URL not set in .env file")
    cfg = Config(server_url=THE_SERVER_URL, enable_https=True)

    start_client(cfg)

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
        input_type=OpAmpInput,
        output_type=OpAmpOutput,
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
