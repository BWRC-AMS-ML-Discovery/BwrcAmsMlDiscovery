# Local Imports
from autockt.client import Config, start as start_client
from autockt.trainer import autockt_train
from autockt_shared import CircuitOptimization, AutoCktGymEnvConfig

from dotenv import dotenv_values


def train(
    circuit_optimization: CircuitOptimization,
    experiment_name: str = "train_45nm_ngspice",
    num_workers: int = 1,
):
    """Training entry point for a script, running `circuit_optimization`."""

    # Load the .env file
    env = dotenv_values()

    # And get the server URL
    THE_SERVER_URL = env.get("THE_SERVER_URL", None)
    if not THE_SERVER_URL:
        raise ValueError("THE_SERVER_URL not set in .env file")
    cfg = Config(server_url=THE_SERVER_URL, enable_https=True)
    start_client(cfg)

    gym_env_config = AutoCktGymEnvConfig(
        circuit_optimization=circuit_optimization,
        actions_per_param=[-1, 0, 2],
    )

    autockt_train(
        experiment_name,
        gym_env_config,
        num_workers,
    )
