from dotenv import dotenv_values
from autockt_shared import OpAmpInput, auto_ckt_sim
from autockt_client import (
    start as start_client,
    Config,
)


def test_auto_ckt():
    """testing auto ckt rpcs"""
    to_test = OpAmpInput(3, 3, 3, 3, 3, 3, 1e-12)
    test = auto_ckt_sim(to_test)
    return test


def main():
    """
    Not picked up by pytest
    """
    # Load the .env file
    env = dotenv_values()

    # And get the server URL
    THE_SERVER_URL = env.get("THE_SERVER_URL", None)
    if not THE_SERVER_URL:
        raise ValueError("THE_SERVER_URL not set in .env file")
    cfg = Config(server_url=THE_SERVER_URL, enable_https=True)

    start_client(cfg)

    test()


def test():
    """
    Picked up by pytest
    """
    reinforcement_learning_env = {"steps": 5, "update": None}

    for reinforcement_learning_step in range(
        reinforcement_learning_env["steps"],
    ):
        result = test_auto_ckt()

        print(f"{result=}")

        reinforcement_learning_env["update"] = result


if __name__ == "__main__":
    main()
