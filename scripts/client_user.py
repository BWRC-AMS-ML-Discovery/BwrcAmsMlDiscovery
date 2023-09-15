"""
# Example authentication script
"""


from discovery.client import (
    alive,
    version,
)

from discovery.client.user import whoami
from discovery.client.mock import mock_inverter_beta_ratio

from discovery.shared.mock import MockInverterBetaRatioInput


# No authentication needed
print(alive())
print(version())


# Authentication needed
print(whoami())
