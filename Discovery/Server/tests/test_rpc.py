from dataclasses import dataclass
from fastapi.testclient import TestClient
from discovery_server import app, _setup_server_rpcs
from discovery_server.auth import (
    AuthenticatedInput,
)
from discovery_shared.rpc import (
    _rpc,
    rpcs,
)


@dataclass
class AuthKey:
    token: str


import pytest


@_rpc
def mock_rpc_func(
    arg: AuthenticatedInput,
) -> AuthKey:  # Adjust the input and return types if needed
    return AuthKey(token="Mock RPC function called")


def test_setup_server_rpcs():
    # Initialize a TestClient
    client = TestClient(app)

    _setup_server_rpcs()

    response = client.post(
        "/mock_rpc_func",
        json={
            "inp": "test_input",
            "auth_key": {"token": ""},
        },
    )

    # Assert that the status code is 200 (success) and the response body is as expected
    assert response.json() == {"token": "Mock RPC function called"}

    # Clean up by removing the mock RPC function from the rpcs dictionary
    del rpcs["mock_rpc_func"]


# If you're using pytest, you can run this test function with the command: pytest -k test_setup_server_rpcs
