"""
# Authentication
"""


from typing import Any, Union


# Local Imports
from ..dataclasses import dataclass


@dataclass
class AuthKey:
    token: str


@dataclass
class AuthenticatedInput:
    inp: Union[Any, None]  # TODO type hint a JSON serializable DataclassInstance
    auth_key: AuthKey


@dataclass
class AuthError:
    err: str


@dataclass
class AuthenticatedOutput:
    out: Union[Any, None]  # TODO type hint a JSON serializable DataclassInstance
    auth_err: Union[AuthError, None]
