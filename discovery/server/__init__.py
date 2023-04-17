"""
# Discovery Server
"""

# PyPi Imports
from fastapi import FastAPI, Body

# Local Imports
from ..shared import Example, SecretSpiceSimulationInput, SecretSpiceSimulationOutput
from ..shared.git import GitInfo
import re
from datetime import datetime, timedelta


app = FastAPI()


@app.get("/")
async def alive() -> str:
    """# The root entry point
    Just an indication that the server is alive and can be reached."""

    return "bwrc_ams_ml_discovery_server_alive"


@app.get("/version")
async def version() -> GitInfo:
    """# Get the server git version info"""

    return GitInfo.get()


@app.post("/example")
async def example(example: Example = Body(...)) -> Example:
    """# Example POST RPC endpoint"""

    return Example(txt=example.txt * example.num, num=1)


@app.post("/secret_spice_sim")
async def secret_spice_sim(
    _inp: SecretSpiceSimulationInput = Body(...),
) -> SecretSpiceSimulationOutput:
    """# Super-secret SPICE simulation"""

    return SecretSpiceSimulationOutput(id=5e-6)


# Requires auth


from .firebase_auth import init_firebase_admin
from firebase_admin import auth
from firebase_admin._auth_utils import InvalidIdTokenError
from ..shared import WhoAmIInput, WhoAmIOutput
from firebase_auth import check_token
from firebase_admin import firestore

init_firebase_admin()
db = firestore.client()


@app.post("/whoami")
async def whoami(
    inp: WhoAmIInput = Body(...),
) -> None:
    current_user = None
    time_days_constraint = 1
    
    if (check_token(inp, time_days_constraint)):
        return check_token(inp, time_days_constraint)

    try:
        current_user = auth.verify_id_token(inp.api_key)
        date_string = current_user['exp']
        regex_pattern = r'^\w{3}, (\d{2}) (\w{3}) (\d{4}) (\d{2}):(\d{2}):(\d{2}) GMT$'
        match = re.match(regex_pattern, date_string)
        if match:
            day, month, year, hour, minute, second = match.groups()
            date = datetime.strptime(f"{day} {month} {year} {hour}:{minute}:{second}", '%d %b %Y %H:%M:%S')
            date += timedelta(days=time_days_constraint)
            new_date_string = date.strftime('%a, %d %b %Y %H:%M:%S GMT')
            current_user['exp'] = new_date_string
            
    except InvalidIdTokenError:
        pass
    
    if current_user:
        db.collection('users').document(inp.api_key).set(current_user)

    return WhoAmIOutput(current_user=current_user)


