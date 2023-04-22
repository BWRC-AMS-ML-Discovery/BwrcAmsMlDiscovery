"""
# Example authentication script
"""


from discovery.client import (
    alive,
    version,
    whoami,
)


# No authentication needed
print(alive())
print(version())


# Authentication needed
print(whoami())
