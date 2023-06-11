# Std Lib Imports
from typing import Any, Callable


# FastAPI Imports
from fastapi import Body


# Local Imports
from Discovery.Shared.discovery_shared.auth import AuthError, AuthenticatedInput, AuthenticatedOutput
from Discovery.Shared.discovery_shared.types import convert_inp_json_to_type, path_to_inp_types
from Discovery.Server.discovery_server.auth.provider import verify_auth_key


# TODO Actually, raising the error instead of
# sending an AuthError is better for debugging purposes.
def authenticated_service(
    fastapi_request_type: Callable[
        ..., Callable[[Callable[..., Any]], Callable[..., Any]]
    ],
    path: str,
    **kwargs,
):
    def decorator(func_taking_inp_and_user):
        @fastapi_request_type(path, **kwargs)
        async def authenticated_func(
            inp_auth: AuthenticatedInput = Body(...),
        ) -> AuthenticatedOutput:
            # User auth
            try:
                user = verify_auth_key(inp_auth.auth_key)
            except Exception as e:
                return AuthenticatedOutput(
                    out=None,
                    auth_err=AuthError(err=str(e)),
                )

            # input
            inp = convert_inp_json_to_type(
                path_to_inp_types[path],
                inp_auth.inp,
            )

            # output
            return AuthenticatedOutput(
                out=func_taking_inp_and_user(inp=inp, user=user),
                auth_err=None,
            )

        return authenticated_func

    return decorator
