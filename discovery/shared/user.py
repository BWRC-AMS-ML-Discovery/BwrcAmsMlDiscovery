"""
User
"""


# Local Imports
from .dataclasses import dataclass


@dataclass
class WhoAmIOutput:
    valid: bool
    username: str
    email: str
