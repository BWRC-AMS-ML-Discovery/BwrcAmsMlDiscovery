"""
# AutoCkt 
## Discovery RPC Protocol Client
"""

# Workspace Imports
## Import the RPC definitions so that `discovery` finds them.
import autockt_shared as _

# The client library will create client stubs for all defined RPCs, including all those functions above.
import discovery_client as dc
from discovery_client import Config


def start(cfg: Config):
    """retrieve values from .env file then configure nad start the client"""

    dc.configure(cfg)

    if cfg.enable_https:
        dc.client_start()
    else:
        # Short-circuiting by directly calling server functions
        import autockt_server as _
