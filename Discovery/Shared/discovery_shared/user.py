"""
User
"""


# Local Imports
from .dataclasses import dataclass


@dataclass
class WhoAmIOutput:
    username: str
    email: str
