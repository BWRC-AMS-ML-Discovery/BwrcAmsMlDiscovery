"""
# Discovery Server
"""

# PyPi Imports
from fastapi import FastAPI, Body

# Workspace Imports
from discovery_shared.rpc import Rpc, _rpcs
from discovery_shared.git import GitInfo


app = FastAPI(
    debug=False,
    title="BWRC AMS ML CktGym",
    description="BWRC AMS ML CktGym",
    version="0.0.1",
)

# Local Imports
from .mock import *
from .user import *


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
