# FastAPI Imports
from fastapi import Body


# Local Imports
from . import app
from ..shared.user import WhoAmIOutput
from ..server.auth import authenticated_service
from ..server.auth.user import User


@authenticated_service(app.post, "/whoami")
def whoami(inp: None, user: User) -> WhoAmIOutput:
    return WhoAmIOutput(
        username=user.username,
        email=user.email,
    )
