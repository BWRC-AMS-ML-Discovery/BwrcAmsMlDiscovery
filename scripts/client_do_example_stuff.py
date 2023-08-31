from dotenv import dotenv_values
from example_client import (
    do_simple_example,
    example_client_start,
    Config,
)


def main():
    # Load the .env file
    env = dotenv_values()

    # And get the server URL
    THE_SERVER_URL = env.get("THE_SERVER_URL", None)
    if not THE_SERVER_URL:
        raise ValueError("THE_SERVER_URL not set in .env file")
    cfg = Config(server_url=THE_SERVER_URL, enable_https=True)
    example_client_start(cfg)

    try:
        do_simple_example()
    except RecursionError:
        print("RecursionError: needs renaming to avoid the same function name")
        pass


if __name__ == "__main__":
    main()
