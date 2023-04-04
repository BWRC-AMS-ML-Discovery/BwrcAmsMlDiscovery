"""
# Discovery Client
"""

# Std-Lib Imports
from dataclasses import asdict

# PyPi Imports
from dotenv import dotenv_values
import httpx

# Local Imports
from ..shared import *
from ..shared.git import GitInfo

# Load the .env file
env = dotenv_values()

# And get the server URL
THE_SERVER_URL = env.get("THE_SERVER_URL", None)
if not THE_SERVER_URL:
    raise ValueError("THE_SERVER_URL not set in .env file")


def alive() -> str:
    """Server aliveness check"""
    resp = httpx.get(f"http://{THE_SERVER_URL}/")
    return resp.text


def version() -> GitInfo:
    """Server version"""
    resp = httpx.get(f"http://{THE_SERVER_URL}/version")
    print(resp)
    return GitInfo(**resp.json())


def example(example: Example) -> Example:
    """Example POST endpoint"""
    resp = httpx.post(f"http://{THE_SERVER_URL}/example", json=asdict(example))
    return Example(**resp.json())


def point(inp: PointInput) -> PointOutput:

    resp = httpx.post(f"http://{THE_SERVER_URL}/point", json=asdict(inp))
    return PointOutput(**resp.json())

