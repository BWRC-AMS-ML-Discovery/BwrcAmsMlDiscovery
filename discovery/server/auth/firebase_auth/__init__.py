import firebase_admin
from firebase_admin import credentials


_cred = credentials.Certificate("./env/firebase_admin_sdk.json")
firebase_admin.initialize_app(_cred)
