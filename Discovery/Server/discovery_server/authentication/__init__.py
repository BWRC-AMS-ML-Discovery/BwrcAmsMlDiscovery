from firebase_admin import auth

from .user import User


def verify_credentials(credentials) -> User:
    username = credentials.username
    token = credentials.password

    current_user = auth.verify_id_token(token)

    user = User(
        name=username,
        email=current_user["email"],
        exp=current_user["exp"],
    )
    return user
