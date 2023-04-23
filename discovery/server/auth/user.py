from dataclasses import dataclass
import datetime

@dataclass
class User:
    user: str
    email: str
    exp: datetime
