"""
# Discovery Server
"""

# PyPi Imports
from fastapi import FastAPI, Body
import uvicorn

# Workspace Imports
from discovery_shared.git import GitInfo


app = FastAPI(
    debug=False,
    title="BWRC AMS Discovery CktGym",
    description="BWRC AMS Discovery CktGym",
    version="0.0.1",
)

# Local Imports
from .mock import *
from .user import *

"""
#Config and Server Start 
"""
options = {
    "temp_config" : 0,
}

def configure(**kwargs):
    for key, value in kwargs.items():
        if key in options:
            options[key] = value
        else:
            print("ignoring unknown option")

def start_server():
    uvicorn.run(app, port=8002, host="127.0.0.1")


"""
# Built-In Endpoints
"""

@app.get("/")
async def alive() -> str:
    """# The root entry point
    Just an indication that the server is alive and can be reached."""

    return "bwrc_ams_ml_discovery_server_alive"


@app.get("/version")
async def version() -> GitInfo:
    """# Get the server git version info"""

    return GitInfo.get()


def _setup_server_rpcs():
    """# Set up server RPCs"""
    from discovery_shared.rpc import rpcs

    for rpc in rpcs.values():
        if rpc.func is None:
            # Now here the function *must be* defined. We just wrap it with API-server stuff.
            msg = f"RPC {rpc.name} does not have a function defined, cannot be set up as a server"
            raise RuntimeError(msg)

        # Create the server endpoint
        async def f(arg: rpc.input_type = Body(...)) -> rpc.return_type:
            return await rpc.func(arg)

        # Give it the server-function's metadata
        f.__name__ = rpc.name
        f.__doc__ = rpc.docstring

        # And register it with the API server
        decorator = app.post(f"/{rpc.name}")
        decorator(f)


_setup_server_rpcs()
