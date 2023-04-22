"""
# Authentication
"""


from typing import Any


# Local Imports
from ..dataclasses import dataclass


@dataclass
class AuthKey:
    token: str


@dataclass
class AuthenticatedInput:
    inp: Any | None  # TODO type hint a JSON serializable DataclassInstance
    auth_key: AuthKey


@dataclass
class AuthError:
    err: str
