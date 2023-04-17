import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


def init_firebase_admin():
    cred = credentials.Certificate("./env/firebase_admin_sdk.json")
    firebase_admin.initialize_app(cred)


def check_token(inp, time_days_constraint):
    from datetime import datetime, timedelta
    db = firestore.client()
    
    # access database, if input user exist, return stored info as a dict from the database
    user_doc = db.collection('users').document(inp.api_key).get()
    if user_doc:
        user_info = user_doc.to_dict()

    # user info exist, if current real time - registered time is within 1 day, then just return stored user doc, else proceed to generate new one
    if user_info:
        user_exp = datetime.strptime(user_info['exp'], '%a, %d %b %Y %H:%M:%S GMT')
        current_time = datetime.utcnow()
        if current_time - user_exp <= timedelta(days=time_days_constraint):
            return user_doc
    return None