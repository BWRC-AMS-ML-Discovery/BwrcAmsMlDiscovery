# Local Imports
from jwt import InvalidTokenError
from discovery.shared.auth import AuthKey
from auth import User


# Current implementation uses Firebase
from server import auth
from auth import check_token
import re
from datetime import datetime, timedelta
from auth import firestore
db = firestore.client()



def verify_auth_key(auth_key: AuthKey) -> User:
    current_user = None
    time_days_constraint = 1
    
    if (check_token(auth_key, time_days_constraint)):
        return check_token(auth_key, time_days_constraint)

    try:
        current_user = auth.verify_id_token(auth_key.api_key)
        date_string = current_user['exp']
        regex_pattern = r'^\w{3}, (\d{2}) (\w{3}) (\d{4}) (\d{2}):(\d{2}):(\d{2}) GMT$'
        match = re.match(regex_pattern, date_string)
        if match:
            day, month, year, hour, minute, second = match.groups()
            date = datetime.strptime(f"{day} {month} {year} {hour}:{minute}:{second}", '%d %b %Y %H:%M:%S')
            date += timedelta(days=time_days_constraint)
            new_date_string = date.strftime('%a, %d %b %Y %H:%M:%S GMT')
            current_user['exp'] = new_date_string
            
    except InvalidTokenError:
        pass
    
    if current_user:
        ret = db.collection('users').document(auth_key.api_key).set(current_user)

    return ret

