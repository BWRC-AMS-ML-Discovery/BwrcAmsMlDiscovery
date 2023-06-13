# Local Imports
from discovery_server import app
from discovery_server.auth import authenticated_service
from discovery_server.auth.user import User
from discovery_shared.mock import (
    MockInverterBetaRatioInput,
    MockInverterBetaRatioOutput,
)


@authenticated_service(app.post, "/mock/inverter_beta_ratio")
def mock_inverter_beta_ratio(
    inp: MockInverterBetaRatioInput, user: User
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
