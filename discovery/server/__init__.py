"""
# Discovery Server
"""

# Std-Lib Imports
import functools
from typing import Optional, List, Any
from dataclasses import asdict

# PyPi Imports
from fastapi import FastAPI, Body

# Local Imports
from ..shared import dataclass, Example


app = FastAPI()


@app.get("/")
async def alive() -> str:
    """# The root entry point
    Just an indication that the server is alive and can be reached."""

    return "bwrc_ams_ml_discovery_server_alive"


@app.post("/example")
async def example(example: Example = Body(...)) -> Example:
    """# Example POST endpoint"""

    return Example(txt=example.txt * example.num, num=1)
