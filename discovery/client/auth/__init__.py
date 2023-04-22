# Std-Lib Imports
from dataclasses import asdict


# PyPI Imports


# Local Imports
from . import env
from discovery.shared.auth import AuthKey


_token = env.get("DISCOVERY_AUTH_TOKEN", None)


def authenticated_request(
    httpx_request_type,
    server_url: str,
    path: str,
    inp,
    inp_auth_type,
    out_type,
):
    """
    TODO Redundant information in parameters
    """
    inp_auth = inp_auth_type(inp=inp, auth_key=AuthKey(_token))
    resp = httpx_request_type(f"http://{server_url}/{path}", json=asdict(inp_auth))
    return out_type(**resp.json())
