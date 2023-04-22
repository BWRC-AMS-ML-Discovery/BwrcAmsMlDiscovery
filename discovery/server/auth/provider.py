# Local Imports
from discovery.shared.auth import AuthKey
from .user import User


# Current implementation uses Firebase
from . import firebase


def verify_auth_key(auth_key: AuthKey) -> User:
    return firebase.verify_auth_key(auth_key)
