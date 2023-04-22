"""
# Authentication
"""


# Local Imports
from .dataclasses import dataclass


@dataclass
class AuthKey:
    token: str
