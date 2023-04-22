# Firebase Imports
from firebase_admin import auth


# Local Imports
from ..provider import User
from discovery.shared.auth import AuthKey


def verify_auth_key(auth_key: AuthKey) -> User:
    user = auth.verify_id_token(auth_key.token)

    # TODO
    return User(user)
