"""
# Discovery Server
"""

# PyPi Imports
from fastapi import FastAPI, Body

# Local Imports
from ..shared import (
    Example,
    SecretSpiceSimulationInput,
    SecretSpiceSimulationOutput,
    InverterBetaRatioInput,
    InverterBetaRatioOutput,
)
from ..shared.git import GitInfo


app = FastAPI(
    debug=False,
    title="BWRC AMS ML CktGym",
    description="BWRC AMS ML CktGym",
    version="0.0.1",
)


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


@app.post("/inverter_beta_ratio")
async def inverter_beta_ratio(
    inp: InverterBetaRatioInput = Body(...),
) -> InverterBetaRatioOutput:
    """# Super-elaborate inverter beta ratio simulation"""
    wp = inp.wp
    wn = inp.wn
    the_ratio = 1.2

    # TODO implement
    # Mock a paraboloid

    output = (wp - 3) ** 2 + (wn - 4) ** 2
    return InverterBetaRatioOutput(
        trise=output / 2,
        tfall=output / 2,
    )

    return InverterBetaRatioOutput(
        trise=1e-9 * the_ratio * wp / (the_ratio * wp + wn),
        tfall=1e-9 * wn / (the_ratio * wp + wn),
    )
