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

from pydantic.dataclasses import dataclass

#mock rpcs class
@dataclass
class MockRpc:
    """
    # Remote Procedure Call
    Shared server-client code
    """

    name: str  # RPC name. Serves as the endpoint name.
    input_type: Type  # Input type
    return_type: Type  # Return type

    docstring: str = ""  # Docstring
    # Inner Function
    # An http POST in the client, and a function call in the server
    func: Callable | None = None

    def __post_init__(self) -> "Rpc":
        # Register to dictionary
        mock_rpcs[self.name] = self

    def __call__(self, *args, **kwargs) -> "self.return_type":
        """# Call our RPC function
        Dispatches to the inner callable.
        This would only be invoked if directly importing from the shared version, but should remain handy.
        Our return-type annotation here is pseudo-code, but you get the point."""
        return self.func(*args, **kwargs)


mock_rpcs: Dict[str, MockRpc] = dict()
def mock_example(input) -> str:
    return "mock example"

rpc = Rpc(name=mock_example.__name__,  
          func=mock_example, 
          input_type=list(inspect.signature(mock_example).parameters.values())[0].annotation, 
          return_type=inspect.signature(mock_example).return_annotation)
