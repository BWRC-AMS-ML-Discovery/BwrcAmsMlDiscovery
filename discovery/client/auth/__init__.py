# Std-Lib Imports
from dataclasses import asdict
from typing import Callable


# PyPI Imports
import httpx


# Local Imports
from . import _path_to_types_maps
from discovery.client import env, THE_SERVER_URL
from discovery.shared.auth import AuthKey


_token = env.get("DISCOVERY_AUTH_TOKEN", None)


def authenticated_request(
    httpx_request_type: Callable[..., httpx.Response],
    path: str,
    inp=None,
    *,
    server_url: str = THE_SERVER_URL,
):
    inp_auth = _path_to_types_maps.inp_auth_types[path](
        inp=inp,
        auth_key=AuthKey(_token),
    )

    resp = httpx_request_type(
        f"http://{server_url}/{path}",
        json=asdict(inp_auth),
    )

    return _path_to_types_maps.out_types[path](
        **resp.json(),
    )
