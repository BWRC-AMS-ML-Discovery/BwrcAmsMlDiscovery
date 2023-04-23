# Std-Lib Imports
from dataclasses import asdict
from typing import Callable, Any


# PyPI Imports
import httpx


# Local Imports
from discovery.client import env, THE_SERVER_URL
from discovery.client.auth.errors import DiscoveryAuthError
from discovery.shared.auth import AuthKey, AuthenticatedInput, AuthenticatedOutput
from discovery.shared.path import path_to_out_types


_token = env.get("DISCOVERY_AUTH_TOKEN", None)


def authenticated_request(
    httpx_request_type: Callable[..., httpx.Response],
    path: str,
    inp: Any | None = None,  # TODO type hint a JSON serializable DataclassInstance
    *,
    server_url: str = THE_SERVER_URL,
):
    inp_auth = AuthenticatedInput(
        inp=inp,
        auth_key=AuthKey(_token),
    )

    resp = httpx_request_type(
        f"http://{server_url}{path}",
        json=asdict(inp_auth),
    )

    out_or_auth_err = AuthenticatedOutput(
        **resp.json(),
    )

    if out_or_auth_err.auth_err:
        raise DiscoveryAuthError(out_or_auth_err.auth_err.err)

    out = path_to_out_types[path](
        **out_or_auth_err.out,  # Currently, this must be a dict-like object
    )

    return out
