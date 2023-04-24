from dataclasses import dataclass
import datetime


@dataclass
class User:
    name: str
    email: str
    exp: datetime
