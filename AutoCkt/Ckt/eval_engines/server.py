import discovery_server as ds
from discovery_server import Config


def server_start(cfg: Config):
    """Retrieve values from .env and then configure and start the server"""

    ds.configure(cfg)
    ds.start_server()
