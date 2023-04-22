"""
# Authenticated Inputs
TODO Figure out a better way to do this
"""


# Local Imports
from discovery.shared.dataclasses import dataclass
from discovery.shared.auth import AuthKey


@dataclass
class WhoAmIInputAuth:
    inp: None
    auth_key: AuthKey
