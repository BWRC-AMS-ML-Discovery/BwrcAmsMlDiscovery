# Local Imports
from jwt import InvalidTokenError
from discovery.shared.auth import AuthKey
from ..user import User


# Current implementation uses Firebase
from firebase_admin import auth
from . import check_token
import re
from datetime import datetime, timedelta
from firebase_admin import firestore
db = firestore.client()



def verify_auth_key(auth_key: AuthKey) -> User:
    current_user = None
    time_days_constraint = 1
    
    if (check_token(auth_key, time_days_constraint)):
        return check_token(auth_key, time_days_constraint)

    try:
        current_user = auth.verify_id_token(auth_key.token)
        date_string = current_user['exp']
        regex_pattern = r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}"
        match = re.match(regex_pattern, date_string)
        if match:
            date = datetime.fromisoformat(date_string)
            date += timedelta(days=time_days_constraint)
            new_date_string = date.strftime('%a, %d %b %Y %H:%M:%S')
            current_user['exp'] = new_date_string
            ret = User(current_user['user'], current_user['email'], current_user['exp'])
            
    except InvalidTokenError:
        pass
    
    if current_user:
        db.collection('users').document(auth_key.token).set(current_user)

    return ret

