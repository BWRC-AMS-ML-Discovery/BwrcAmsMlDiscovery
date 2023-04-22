from dataclasses import dataclass


# Local Imports
from discovery.shared.auth import AuthKey
from . import firebase


@dataclass
class User:
    username: str


def verify_auth_key(auth_key: AuthKey) -> User:
    return firebase.verify_auth_key(auth_key)
