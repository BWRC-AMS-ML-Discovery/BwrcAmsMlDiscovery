"""
# Discovery Server

Example use case
```python
import discovery_server as ds 

# ... 
# Define all my RPCs etc
# ... 

ds.configure(ds.Config(port=8002, host="www.whatever.com")
ds.start_server()

```
"""

# Std-Lib Imports
from typing import Annotated, Optional

# PyPi Imports
from fastapi import FastAPI, Body, Depends
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import uvicorn

# Workspace Imports
from discovery_server.authentication import verify_credentials, dev_start

# from discovery_shared.git import GitInfo


app = FastAPI(
    debug=False,
    title="BWRC AMS ML Discovery CktGym",
    description="BWRC AMS ML Discovery CktGym",
    version="0.0.1",
)

security = HTTPBasic()


# Local Imports
# FIXME Can rewrite using RPC
from .mock import *
from .user import *

from pydantic.dataclasses import dataclass


@dataclass
class Config:
    """# Server Configuration"""

    port: int = 8000
    host: str = "127.0.0.1"
    dev: Optional[bool] = True


# Create the module-scope configuration
config = Config()


def configure(cfg: Config) -> None:
    """Set the module-scope `Config`."""
    global config
    config = cfg


"""
# Config and Server Start 
"""


def start_server():
    """starts the server using the given config and sets up local rpcs"""
    _setup_server_rpcs(config.dev)
    uvicorn.run(app, port=config.port, host=config.host)


"""
# Built-In Endpoints
"""


@app.get("/")
async def alive() -> str:
    """# The root entry point
    Just an indication that the server is alive and can be reached."""

    return "bwrc_ams_ml_discovery_server_alive"


# @app.get("/version")
# async def version() -> GitInfo:
#     """# Get the server git version info"""

#     return GitInfo.get()


def _setup_server_rpcs(dev: bool):
    """# Set up server RPCs"""
    from discovery_shared.rpc import rpcs

    for rpc in rpcs.values():
        if rpc.func is None:
            # Now here the function *must be* defined. We just wrap it with API-server stuff.
            msg = f"RPC {rpc.name} does not have a function defined, cannot be set up as a server"
            raise RuntimeError(msg)

        # Create the server endpoint
        # FIXME type annotations incorrect, can use a function generator to fix.
        # rpc needs to be evaluated at create time not run time.
        async def f(
            credentials: Annotated[HTTPBasicCredentials, Depends(security)],
            arg: rpc.input_type = Body(...),
            *,
            rpc=rpc,
        ) -> rpc.return_type:
            # FIXME Perhaps we want to use this User?

            if dev:
                dev_start()

            user = verify_credentials(credentials)

            return rpc.func(arg)

        # Give it the server-function's metadata
        f.__name__ = rpc.name
        f.__doc__ = rpc.docstring

        # And register it with the API server
        decorator = app.post(f"/{rpc.name}")
        decorator(f)
