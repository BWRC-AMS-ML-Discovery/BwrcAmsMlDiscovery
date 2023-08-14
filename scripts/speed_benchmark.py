from dotenv import dotenv_values
from example_client import (
    example_client_start,
    Config,
)
import time
from example_client import auto_ckt_sim_hdl21, AutoCktInput, auto_ckt_sim

ENABLE_HTTPS = True


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
    cfg = Config(server_url=THE_SERVER_URL, enable_https=ENABLE_HTTPS)

    example_client_start(cfg)

    to_test = AutoCktInput(3, 3, 3, 3, 3, 3, 1e-12)

    start_time = time.time()
    auto_ckt_sim(to_test)
    end_time = time.time()
    print("total time (auto_ckt_sim): " + str(end_time - start_time))

    start_time = time.time()
    auto_ckt_sim_hdl21(to_test)
    end_time = time.time()
    print("total time (auto_ckt_sim_hdl21): " + str(end_time - start_time))


if __name__ == "__main__":
    main()
