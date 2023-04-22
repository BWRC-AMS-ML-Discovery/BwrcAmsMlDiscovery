# FastAPI Imports
from fastapi import Body


# Local Imports
from . import app
from ..shared.auth import WhoAmIOutput
from .auth.inputs import WhoAmIInputAuth


@app.post("/whoami")
async def whoami(
    _inp: WhoAmIInputAuth = Body(...),
) -> None:
    return WhoAmIOutput(current_user="me")
