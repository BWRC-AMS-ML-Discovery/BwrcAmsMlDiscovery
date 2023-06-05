# PyPI Imports
import httpx


# Local Imports
from .auth import authenticated_request
from ..shared.user import WhoAmIOutput


def whoami() -> WhoAmIOutput:
    """Pass in an ID token"""
    return authenticated_request(
        httpx.post,
        "/whoami",
    )
