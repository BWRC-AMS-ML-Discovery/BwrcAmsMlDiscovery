import os

import firebase_admin
from firebase_admin import auth, credentials

from .user import User


# Get current file directory
DIR_PATH = os.path.dirname(os.path.realpath(__file__))


def start_firebase_auth():
    _cred = credentials.Certificate(DIR_PATH + "/firebase_admin_sdk.json")
    firebase_admin.initialize_app(_cred)


def verify_credentials(credentials) -> User:
    username = credentials.username
    token = credentials.password

    # current_user = auth.verify_id_token(token)
    current_user = auth.verify_session_cookie(token)

    user = User(
        name=username,
        email=current_user["email"],
        exp=current_user["exp"],
    )
    print(current_user["exp"])
    return user
