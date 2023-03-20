import firebase_admin
from firebase_admin import credentials
from firebase_admin import auth  # Todo


cred = credentials.Certificate("./env/firebase_admin_sdk.json")
default_app = firebase_admin.initialize_app()
