# FastAPI Imports
from fastapi import Body


# Local Imports
from . import app
from Discovery.Shared.discovery_shared.user import WhoAmIOutput
from Discovery.Server.discovery_server.auth import authenticated_service
from Discovery.Server.discovery_server.auth.user import User


@authenticated_service(app.post, "/whoami")
def whoami(inp: None, user: User) -> WhoAmIOutput:
    return WhoAmIOutput(
        username=user.name,
        email=user.email,
    )
