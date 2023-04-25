# Local Imports
from discovery.server import app
from discovery.server.auth import authenticated_service
from discovery.server.auth.user import User
from discovery.shared.mock import (
    MockInverterBetaRatioInput,
    MockInverterBetaRatioOutput,
)
from discovery.shared import (
    InverterBetaRatioInput,
    InverterBetaRatioOutput,
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


@authenticated_service(app.post, "/inverter_beta_ratio")
async def inverter_beta_ratio(
    inp: InverterBetaRatioInput, user: User
) -> InverterBetaRatioOutput:
    """
    # Super-elaborate inverter beta ratio simulation
    This uses a different input/output type.
    """
    wp = inp.wp
    wn = inp.wn
    the_ratio = 1.2

    # Mock a paraboloid
    output = (wp - 3) ** 2 + (wn - 4) ** 2
    return InverterBetaRatioOutput(
        trise=output / 2,
        tfall=output / 2,
    )
