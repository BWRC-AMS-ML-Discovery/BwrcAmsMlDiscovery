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

THE_SERVER_PORT = env.get("THE_SERVER_PORT", None)
if not THE_SERVER_PORT:
    raise ValueError("THE_SERVER_PORT not set in .env file")

THE_SERVER_HOST = env.get("THE_SERVER_HOST", None)
if not THE_SERVER_HOST:
    raise ValueError("THE_SERVER_HOST not set in .env file")
"""
#Client Config
"""

#put all client config variables in here
options = {
    'THE_SERVER_URL': THE_SERVER_URL,
    'THE_SERVER_PORT': THE_SERVER_PORT,
    'THE_SERVER_HOST': THE_SERVER_HOST,
}

def configure(**kwargs):
    #searchs for corresponding key in optiions dict and updates if it exists
    for key, value in kwargs.items():
        if key in options:
            options[key] = value
        else:
            print(f"ignoring unknown option: {key}")


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
