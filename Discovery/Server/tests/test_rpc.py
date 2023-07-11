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


# Import pytest if you're using pytest as your testing framework
import pytest


# Define a mock RPC function
@_rpc
def mock_rpc_func(
    arg: AuthenticatedInput,
) -> AuthKey:  # Adjust the input and return types if needed
    return AuthKey(token="Mock RPC function called")


# Define a test function for _setup_server_rpcs
def test_setup_server_rpcs():
    # Initialize a TestClient
    client = TestClient(app)

    # Call the _setup_server_rpcs function to setup server RPCs
    _setup_server_rpcs()

    # Use TestClient to make a POST request to the mock_rpc_func endpoint and check the response
    response = client.post(
        "/mock_rpc_func",
        json={
            "inp": "test_input",
            "auth_key": {
                "token": "eyJhbGciOiJSUzI1NiIsImtpZCI6ImE1MWJiNGJkMWQwYzYxNDc2ZWIxYjcwYzNhNDdjMzE2ZDVmODkzMmIiLCJ0eXAiOiJKV1QifQ.eyJuYW1lIjoiV2F5bmUgV2FuZyIsInBpY3R1cmUiOiJodHRwczovL2xoMy5nb29nbGV1c2VyY29udGVudC5jb20vYS9BR05teXhaV0l5ZzYzTDFrQTZ5LVVpR3R1aVFpZkF2YzN4RXpRVUVSalgzRThnPXM5Ni1jIiwiaXNzIjoiaHR0cHM6Ly9zZWN1cmV0b2tlbi5nb29nbGUuY29tL2J3cmNhbXNtbGRpc2NvdmVyeWZpcmViYXNlIiwiYXVkIjoiYndyY2Ftc21sZGlzY292ZXJ5ZmlyZWJhc2UiLCJhdXRoX3RpbWUiOjE2NzkyODMyMTUsInVzZXJfaWQiOiJlRkRJSGxZOGFoUWRCY0tKaWUwYWpQb1Y1WWYyIiwic3ViIjoiZUZESUhsWThhaFFkQmNLSmllMGFqUG9WNVlmMiIsImlhdCI6MTY4OTAzODYyNSwiZXhwIjoxNjg5MDQyMjI1LCJlbWFpbCI6IndoaC5iZWFyQGJlcmtlbGV5LmVkdSIsImVtYWlsX3ZlcmlmaWVkIjp0cnVlLCJmaXJlYmFzZSI6eyJpZGVudGl0aWVzIjp7Imdvb2dsZS5jb20iOlsiMTEyNzkxMzI1NTM2NzUyOTgxNzExIl0sImVtYWlsIjpbIndoaC5iZWFyQGJlcmtlbGV5LmVkdSJdfSwic2lnbl9pbl9wcm92aWRlciI6Imdvb2dsZS5jb20ifX0.hDavf4lFclr1B-m4I_0xnIDVLDDCxcJBc7uadgIFCZn-l8NUmm0jV0r28OSQ0AeUyPMFnvWhND2I8d6IlO_IxntLDyLtUay7dvrzZ5kMxs7UyasXMYEiDDXfDoYvl4T4E2S9gKPsm7aUJ03ZyeiDsOC3pylDgkAj4_jufSNdsNAmwLf2QeEXgGSKhT4qwWDdGgTIG4pmia-NESs9laRkZTGwtGIGJjkVwndvl2BM1g-qpF7NsCmv10XFhSoIx_uTxReiwplf6hLBMZo9vpFkX9MuNm8hB-YdIE88EJfVy9dP4jclMZHNPoYi8OHcdeSFFTIJhGx1dsVA0M-njCz_-Q"
            },
        },
    )

    # Assert that the status code is 200 (success) and the response body is as expected
    assert response.json() == {"token": "Mock RPC function called"}

    # Clean up by removing the mock RPC function from the rpcs dictionary
    del rpcs["mock_rpc_func"]


# If you're using pytest, you can run this test function with the command: pytest -k test_setup_server_rpcs
