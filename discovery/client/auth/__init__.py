# Std-Lib Imports
from dataclasses import asdict
from typing import Callable, Any


# PyPI Imports
import httpx


# Local Imports
from . import _maps
from discovery.client import env, THE_SERVER_URL
from discovery.shared.auth import AuthKey, AuthenticatedInput, AuthenticatedOutput


_token = env.get("DISCOVERY_AUTH_TOKEN", None)


def authenticated_request(
    httpx_request_type: Callable[..., httpx.Response],
    path: str,
    inp: Any | None = None,  # TODO type hint a JSON serializable DataclassInstance
    *,
    server_url: str = THE_SERVER_URL,
) -> AuthenticatedOutput:
    inp_auth = AuthenticatedInput(
        inp=inp,
        auth_key=AuthKey(_token),
    )

    resp = httpx_request_type(
        f"http://{server_url}/{path}",
        json=asdict(inp_auth),
    )

    return AuthenticatedOutput(
        **resp.json(),
    )
