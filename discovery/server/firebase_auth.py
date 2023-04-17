import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def init_firebase_admin():
    cred = credentials.Certificate("./env/firebase_admin_sdk.json")
    firebase_admin.initialize_app(cred)
