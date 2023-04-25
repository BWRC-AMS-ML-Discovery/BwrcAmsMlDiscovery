# PyPI Imports
import httpx


# Local Imports
from ..auth import authenticated_request
from ...shared.mock import (
    MockInverterBetaRatioInput,
    MockInverterBetaRatioOutput,
)
from ...shared import (
    InverterBetaRatioInput,
    InverterBetaRatioOutput,
)


def mock_inverter_beta_ratio(
    inp: MockInverterBetaRatioInput,
) -> MockInverterBetaRatioOutput:
    return authenticated_request(
        httpx.post,
        "/mock/inverter_beta_ratio",
        inp,
    )


def inverter_beta_ratio(
    inp: InverterBetaRatioInput,
) -> InverterBetaRatioOutput:
    return authenticated_request(
        httpx.post,
        "/inverter_beta_ratio",
        inp,
    )
