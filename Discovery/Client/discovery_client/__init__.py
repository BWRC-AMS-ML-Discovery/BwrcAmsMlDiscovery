"""
# Discovery Client
"""

# Std-Lib Imports
from dataclasses import asdict

# PyPi Imports
from dotenv import dotenv_values
import httpx

# Workspace Imports
from discovery_shared.git import GitInfo


# Load the .env file
env = dotenv_values()

# And get the server URL
THE_SERVER_URL = env.get("THE_SERVER_URL", None)
if not THE_SERVER_URL:
    raise ValueError("THE_SERVER_URL not set in .env file")

"""
# Built-In Endpoints
"""


def alive() -> str:
    """Server aliveness check"""
    resp = httpx.get(f"http://{THE_SERVER_URL}/")
    return resp.text


def version() -> GitInfo:
    """Server version"""
    resp = httpx.get(f"http://{THE_SERVER_URL}/version")
    return GitInfo(**resp.json())


"""
# User-Defined Endpoints

Set up a client function for each defined `Rpc`.
"""


def _setup_client_rpcs():

    #TODO: Find a better way to enable this? Very similar to ENABLE_HTTP
    ENABLE_MOCK_RPC = False
    rpcs_dict = None
    if ENABLE_MOCK_RPC:
        # enable mock rpcs to remove redundant rpcs that occur when importing both discovery_client and example_server in pytest
        from .mock import mock_rpcs
        rpcs_dict = mock_rpcs
    else:
        # Import the list of RPCs
        from discovery_shared.rpc import rpcs
        rpcs_dict = rpcs

    # And set up a client function for each
    for rpc in rpcs_dict.values():
        if rpc.func is not None:
            msg = f"RPC {rpc.name} already has a function defined, cannot be set up as a client"
            raise RuntimeError(msg)

        # Create the client function
        # FIXME type annotations incorrect, can use a function generator to fix.
        # rpc needs to be evaluated at create time not run time.
        def f(inp: rpc.input_type, *, rpc=rpc) -> rpc.return_type:
            url = f"http://{THE_SERVER_URL}/{rpc.name}"
            resp = httpx.post(url, json=asdict(inp))
            return rpc.return_type(**resp.json())

        # Give it the same name as the RPC
        f.__name__ = rpc.name
        f.__doc__ = rpc.docstring
        # Set it as the function for the RPC
        rpc.func = f


_setup_client_rpcs()
