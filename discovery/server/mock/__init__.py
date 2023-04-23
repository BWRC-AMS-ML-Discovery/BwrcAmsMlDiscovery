# FastAPI Imports
from fastapi import Body


# Local Imports
from discovery.server import app
from discovery.shared.mock import (
    MockInverterBetaRatioInput,
    MockInverterBetaRatioOutput,
)
from discovery.shared.auth import AuthError, AuthenticatedInput, AuthenticatedOutput
from discovery.shared.path import path_to_inp_types

from discovery.server.auth.provider import verify_auth_key


def f(
    inp: MockInverterBetaRatioInput,
) -> MockInverterBetaRatioOutput:
    """# Super-elaborate inverter beta ratio simulation"""
    wp = inp.wp
    wn = inp.wn

    # Mock a paraboloid
    output = (wp - 3) ** 2 + (wn - 4) ** 2
    return MockInverterBetaRatioOutput(
        trise=output / 2,
        tfall=output / 2,
    )


@app.post("/mock/inverter_beta_ratio")
async def mock_inverter_beta_ratio(
    inp_auth: AuthenticatedInput = Body(...),
) -> AuthenticatedOutput:
    try:
        user = verify_auth_key(inp_auth.auth_key)
    except Exception as e:
        return AuthenticatedOutput(
            out=None,
            auth_err=AuthError(err=str(e)),
        )

    inp = path_to_inp_types["/mock/inverter_beta_ratio"](
        **inp_auth.inp,
    )

    return AuthenticatedOutput(
        out=f(inp),
        auth_err=None,
    )
