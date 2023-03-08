"""
# Discovery Client
"""

# Std-Lib Imports
from dataclasses import asdict

# PyPi Imports
import httpx

# Local Imports
from ..shared import Example, SecretSpiceSimulationInput, SecretSpiceSimulationOutput

THE_SERVER_URL = "localhost:8001"


def alive() -> str:
    """Server aliveness check"""
    resp = httpx.get(f"http://{THE_SERVER_URL}/")
    return resp.text


def example(example: Example) -> Example:
    """Example POST endpoint"""
    resp = httpx.post(f"http://{THE_SERVER_URL}/example", json=asdict(example))
    return Example(**resp.json())


def secret_spice_sim(inp: SecretSpiceSimulationInput) -> SecretSpiceSimulationOutput:
    """Invoke a (very secret) SPICE simulation"""
    resp = httpx.post(f"http://{THE_SERVER_URL}/secret_spice_sim", json=asdict(inp))
    return SecretSpiceSimulationOutput(**resp.json())
