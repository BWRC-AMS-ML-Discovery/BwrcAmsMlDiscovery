# PyPI Imports
import httpx

import inspect
from discovery_shared.rpc import Rpc
from typing import Callable, Type, Dict

# Local Imports
from ..auth import authenticated_request
from discovery_shared.mock import (
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
