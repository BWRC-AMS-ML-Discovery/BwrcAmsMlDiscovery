from dotenv import dotenv_values
from example_client import (
    test_auto_ckt,
    example_client_start,
    Config,
)


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
    cfg = Config(server_url=THE_SERVER_URL, enable_https=False)

    example_client_start(cfg)

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
