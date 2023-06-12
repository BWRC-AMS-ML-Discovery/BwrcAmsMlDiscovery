# FastAPI Imports
from fastapi import Body


# Local Imports
from . import app
from discovery_shared.user import WhoAmIOutput
from discovery_server.auth import authenticated_service
from discovery_server.auth.user import User


@authenticated_service(app.post, "/whoami")
def whoami(inp: None, user: User) -> WhoAmIOutput:
    return WhoAmIOutput(
        username=user.name,
        email=user.email,
    )
