# Local Imports
from discovery_shared.auth import AuthKey
from .user import User


# Current implementation uses Firebase
from .firebase import provider


def verify_auth_key(auth_key: AuthKey) -> User:
    return User(
        name="FIXME",
        email="FIXME",
        exp=None,
    )

    # FIXME Fix this Firebase
    return provider.verify_auth_key(auth_key)
