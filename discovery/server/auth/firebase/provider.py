# Firebase Imports
from firebase_admin import auth


# Local Imports
from ..user import User
from discovery.shared.auth import AuthKey


def verify_auth_key(auth_key: AuthKey) -> User:
    user = auth.verify_id_token(auth_key.token)

    return User(
        username=user["name"],
        email=user["email"],
    )
