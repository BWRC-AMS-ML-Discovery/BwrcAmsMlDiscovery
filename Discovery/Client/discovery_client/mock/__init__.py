# PyPI Imports
import httpx


# Local Imports
from ..auth import authenticated_request
from ...shared.mock import (
    MockInverterBetaRatioInput,
    MockInverterBetaRatioOutput,
)


def mock_inverter_beta_ratio(
    inp: MockInverterBetaRatioInput,
) -> MockInverterBetaRatioOutput:
    return authenticated_request(
        httpx.post,
        "/mock/inverter_beta_ratio",
        inp,
    )
