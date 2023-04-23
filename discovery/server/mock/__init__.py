# Local Imports
from discovery.server import app
from discovery.server.auth import authenticated_service
from discovery.shared.mock import (
    MockInverterBetaRatioInput,
    MockInverterBetaRatioOutput,
)


@authenticated_service(app.post, "/mock/inverter_beta_ratio")
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
