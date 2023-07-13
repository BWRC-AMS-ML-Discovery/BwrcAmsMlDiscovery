from dataclasses import dataclass
from datetime import datetime


@dataclass
class User:
    name: str
    email: str
    exp: datetime
