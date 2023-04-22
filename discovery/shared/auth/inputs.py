"""
# Authenticated Inputs
TODO Create an InputAuth type for every input type is tedious.
"""


# Local Imports
from discovery.shared.dataclasses import dataclass
from discovery.shared.auth import AuthKey


@dataclass
class WhoAmIInputAuth:
    inp: None
    auth_key: AuthKey
