# FastAPI Imports
from fastapi import Body


# Local Imports
from . import app
from ..shared.user import WhoAmIOutput
from ..shared.auth.inputs import WhoAmIInputAuth
from .auth.provider import verify_auth_key


@app.post("/whoami")
async def whoami(
    inp: WhoAmIInputAuth = Body(...),
) -> None:
    user = verify_auth_key(inp.auth_key)

    return WhoAmIOutput(username=user.username)
