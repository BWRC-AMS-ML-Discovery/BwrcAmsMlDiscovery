# Std-Lib Imports
from dataclasses import asdict
from typing import Callable


# PyPI Imports
import httpx


# Local Imports
from . import _maps
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
    inp_auth = {
        "inp": asdict(inp) if inp else None,
        "auth_key": asdict(AuthKey(_token)),
    }

    resp = httpx_request_type(
        f"http://{server_url}/{path}",
        json=inp_auth,
    )

    return _maps.path_to_out_types[path](
        **resp.json(),
    )
