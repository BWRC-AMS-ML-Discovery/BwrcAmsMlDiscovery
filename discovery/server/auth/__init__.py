# Std Lib Imports
from typing import Any, Callable


# FastAPI Imports
from fastapi import Body


# Local Imports
from discovery.shared.auth import AuthError, AuthenticatedInput, AuthenticatedOutput
from discovery.shared.path import path_to_inp_types

from discovery.server.auth.provider import verify_auth_key


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
            inp = path_to_inp_types["/mock/inverter_beta_ratio"](
                **inp_auth.inp,
            )

            # output
            return AuthenticatedOutput(
                out=func_taking_inp_and_user(inp=inp, user=user),
                auth_err=None,
            )

        return authenticated_func

    return decorator
