# FastAPI Imports
from fastapi import Body


# Local Imports
from . import app
from ..shared.user import WhoAmIOutput
from ..shared.auth import AuthError, AuthenticatedInput, AuthenticatedOutput

from .auth.provider import verify_auth_key


@app.post("/whoami")
async def whoami(
    inp: AuthenticatedInput = Body(...),
) -> AuthenticatedOutput:
    try:
        user = verify_auth_key(inp.auth_key)
    except Exception as e:
        return AuthenticatedOutput(
            out=None,
            auth_err=AuthError(err=str(e)),
        )

    return AuthenticatedOutput(
        out=WhoAmIOutput(
            username=user.username,
            email=user.email,
        ),
        auth_err=None,
    )
