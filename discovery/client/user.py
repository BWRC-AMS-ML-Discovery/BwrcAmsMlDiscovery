# Std-Lib Imports
from dataclasses import asdict


# PyPI Imports
import httpx


# Local Imports
from . import THE_SERVER_URL
from .auth import authenticated_request
from ..shared.user import WhoAmIOutput


def whoami() -> WhoAmIOutput:
    """Pass in an ID token"""
    return authenticated_request(
        httpx.post,
        THE_SERVER_URL,
        "whoami",
    )
