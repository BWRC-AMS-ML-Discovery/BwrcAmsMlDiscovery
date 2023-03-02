"""
# Discovery Client
"""

# Std-Lib Imports
from dataclasses import asdict

# PyPi Imports
import httpx

# Local Imports
from ..shared import Example

THE_SERVER_URL = "localhost:8000"


def alive() -> str:
    resp = httpx.get(f"http://{THE_SERVER_URL}/")
    return resp.text


def example(example: Example) -> Example:
    resp = httpx.post(f"http://{THE_SERVER_URL}/example", json=asdict(example))
    return Example(**resp.json())
