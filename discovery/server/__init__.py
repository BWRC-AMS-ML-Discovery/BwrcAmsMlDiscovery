"""
# Discovery Server
"""

# PyPi Imports
from fastapi import FastAPI, Body

# Local Imports
from ..shared import *
from ..shared.git import GitInfo


app = FastAPI()


@app.get("/")
async def alive() -> str:
    """# The root entry point
    Just an indication that the server is alive and can be reached."""

    return "bwrc_ams_ml_discovery_server_alive"


@app.get("/version")
async def version() -> GitInfo:
    """# Get the server git version info"""

    return GitInfo.get()


@app.post("/example")
async def example(example: Example = Body(...)) -> Example:
    """# Example POST RPC endpoint"""

    return Example(txt=example.txt * example.num, num=1)


@app.post("/create_point")
async def create_point(
    _inp: PointInput = Body(...),
) -> PointOutput:

    return PointOutput(_inp)