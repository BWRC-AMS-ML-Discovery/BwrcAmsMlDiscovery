# Std-Lib Imports
from dataclasses import asdict
from typing import Callable, Any, Union


# PyPI Imports
import httpx


# Local Imports
from .. import env, THE_SERVER_URL
from .errors import DiscoveryAuthError
from discovery_shared.auth import AuthKey, AuthenticatedInput, AuthenticatedOutput
from discovery_shared.types import convert_out_json_to_type, path_to_out_types


_token = env.get("DISCOVERY_AUTH_TOKEN", None)


def authenticated_request(
    httpx_request_type: Callable[..., httpx.Response],
    path: str,
    # TODO type hint a JSON serializable DataclassInstance
    inp: Union[Any, None] = None,
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

    out = convert_out_json_to_type(
        path_to_out_types[path],
        out_or_auth_err.out,
    )

    return out
