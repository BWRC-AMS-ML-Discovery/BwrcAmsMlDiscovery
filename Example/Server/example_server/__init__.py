"""
# Example `Discovery` Server Implementation 
"""

import discovery_server as ds
from discovery_server import Config
from example_shared import example, Example


def example_server_start(cfg: Config):
    """Retrieve values from .env and then configure and start the server"""

    ds.configure(cfg)
    ds.start_server()


@example.impl
def example_func(example: Example) -> Example:
    """# Example RPC Implementation"""

    return Example(txt=example.txt * example.num, num=1)
