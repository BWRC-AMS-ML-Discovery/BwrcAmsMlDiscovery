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
# THE_SERVER_URL = env.get("THE_SERVER_URL", None)
THE_SERVER_URL = "http://localhost:8001"
if not THE_SERVER_URL:
    raise ValueError("THE_SERVER_URL not set in .env file")

#options contained in the client
options = {
    'THE_SERVER_URL': THE_SERVER_URL,
}

def configure(**kwargs):
    # print(options['THE_SERVER_URL'])
    for key, value in kwargs.items():
        # print(f"{key} :  {value}")
        if key in options:
            options[key] = value
        else:
            print(f"ignoring unknown option: {key}")
    # print(options['THE_SERVER_URL'])

"""
# Built-In Endpoints
"""


def alive() -> str:
    """Server aliveness check"""
    resp = httpx.get(f"http://{options['THE_SERVER_URL']}/")
    return resp.text


def version() -> GitInfo:
    """Server version"""
    resp = httpx.get(f"http://{options['THE_SERVER_URL']}/version")
    return GitInfo(**resp.json())


"""
# User-Defined Endpoints

Set up a client function for each defined `Rpc`.
"""


def _setup_client_rpcs():
    # Import the list of RPCs
    from discovery_shared.rpc import rpcs

    # And set up a client function for each
    for rpc in rpcs.values():
        if rpc.func is not None:
            msg = f"RPC {rpc.name} already has a function defined, cannot be set up as a client"
            raise RuntimeError(msg)

        # Create the client function
        def f(inp: rpc.input_type) -> rpc.return_type:
            url = f"http://{options['THE_SERVER_URL']}/{rpc.name}"
            resp = httpx.post(url, json=asdict(inp))
            return rpc.return_type(**resp.json())

        # Give it the same name as the RPC
        f.__name__ = rpc.name
        f.__doc__ = rpc.docstring
        # Set it as the function for the RPC
        rpc.func = f


_setup_client_rpcs()
