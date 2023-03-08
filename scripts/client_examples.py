"""
# Example Discovery Client Script 
"""

from discovery import Example, SecretSpiceSimulationInput
from discovery.client import alive, version, example, secret_spice_sim

# Call the server's root endpoint.
# Gets a general health-indication of whether we can contact the server.
print(alive())

# Get the server's version
print(version())

# Call the server's example RPC endpoint, and print what comes back
print(example(Example(txt="Hello World!", num=3)))

# Now invoke a super-secret SPICE simulation
print(secret_spice_sim(SecretSpiceSimulationInput(w=1000, l=150, v=1000)))
