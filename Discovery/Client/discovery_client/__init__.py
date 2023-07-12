"""
# Discovery Client

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
import os
from dataclasses import asdict

# PyPi Imports
import dotenv
import httpx

# Workspace Imports
from discovery_shared.git import GitInfo
from pydantic.dataclasses import dataclass


# FIXME Probably should be Config?
dotenv.load_dotenv()


@dataclass
class Config:
    """# Server Configuration"""

    server_url: str = "localhost:8000"


# Create the module-scope configuration
config = Config()


def configure(cfg: Config) -> None:
    """Set the module-scope `Config`."""
    global config
    config = cfg


def client_start():
    """perform client start operations and sets up local client rpcs"""
    # TODO: is there anything else to add here
    _setup_client_rpcs()


"""
# Built-In Endpoints
"""


def alive() -> str:
    """Server aliveness check"""
    resp = httpx.get(f"http://{config.server_url}/")
    return resp.text


def version() -> GitInfo:
    """Server version"""
    resp = httpx.get(f"http://{config.server_url}/version")
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
            url = f"http://{config.server_url}/{rpc.name}"
            resp = httpx.post(
                url,
                json=asdict(inp),
                auth=(
                    os.environ["DISCOVERY_USERNAME"],
                    os.environ["DISCOVERY_API_KEY"],
                ),
            )
            return rpc.return_type(**resp.json())

        # Give it the same name as the RPC
        f.__name__ = rpc.name
        f.__doc__ = rpc.docstring
        # Set it as the function for the RPC
        rpc.func = f
