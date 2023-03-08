"""
# Discovery Server
"""

# PyPi Imports
from fastapi import FastAPI, Body

# Local Imports
from ..shared import Example, SecretSpiceSimulationInput, SecretSpiceSimulationOutput


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


@app.post("/secret_spice_sim")
async def secret_spice_sim(
    _inp: SecretSpiceSimulationInput = Body(...),
) -> SecretSpiceSimulationOutput:
    """# Super-secret SPICE simulation"""

    return SecretSpiceSimulationOutput(id=5e-6)
