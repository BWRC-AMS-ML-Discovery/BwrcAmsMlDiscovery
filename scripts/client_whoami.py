"""
# Example authentication script
"""


from discovery.client import (
    alive,
    version,
)


from discovery.client.user import whoami


# No authentication needed
print(alive())
print(version())


# Authentication needed
print(whoami())
