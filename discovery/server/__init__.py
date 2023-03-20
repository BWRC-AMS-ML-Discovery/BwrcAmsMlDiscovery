"""
# Discovery Server
"""

# PyPi Imports
from fastapi import FastAPI, Body

# Local Imports
from ..shared import Example, SecretSpiceSimulationInput, SecretSpiceSimulationOutput
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


@app.post("/secret_spice_sim")
async def secret_spice_sim(
    _inp: SecretSpiceSimulationInput = Body(...),
) -> SecretSpiceSimulationOutput:
    """# Super-secret SPICE simulation"""

    return SecretSpiceSimulationOutput(id=5e-6)


# Requires auth


from .firebase_auth import auth  # Todo
from ..shared import WhoAmIInput, WhoAmIOutput


@app.post("/whoami")
async def whoami(
    _inp: WhoAmIInput = Body(...),
) -> None:
    return WhoAmIOutput(current_user="me")
