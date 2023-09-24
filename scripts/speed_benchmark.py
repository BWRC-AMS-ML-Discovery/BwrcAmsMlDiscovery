import time
from dotenv import dotenv_values
from autockt.client import (
    start as start_client,
    Config,
)
from autockt_shared import auto_ckt_sim_hdl21, OpAmpInput, auto_ckt_sim

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
    cfg = Config(server_url="34.83.44.225", enable_https=ENABLE_HTTPS)

    start_client(cfg)

    to_test = OpAmpInput(3, 3, 3, 3, 3, 3, 1e-12)

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
