# FastAPI Imports
from fastapi import Body


# Local Imports
from . import app
from ..shared.user import WhoAmIOutput
from ..shared.auth import AuthError, AuthenticatedInput

from .auth.provider import verify_auth_key


@app.post("/whoami")
async def whoami(
    inp: AuthenticatedInput = Body(...),
) -> WhoAmIOutput | AuthError:
    try:
        user = verify_auth_key(inp.auth_key)
    except Exception as e:
        return AuthError(err=str(e))

    return WhoAmIOutput(
        username=user.username,
        email=user.email,
    )
