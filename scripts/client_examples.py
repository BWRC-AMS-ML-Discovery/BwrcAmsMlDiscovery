"""
# Example Discovery Client Script 
"""

from discovery import Example, SecretSpiceSimulationInput, OpAmpParams
from discovery.client import (
    alive,
    version,
    example,
    secret_spice_sim,
    simulate_that_opamp,
    elaborate_that_opamp_here_and_simulate_on_the_server,
)

# Call the server's root endpoint.
# Gets a general health-indication of whether we can contact the server.
print(alive())

# Get the server's version
print(version())

# Call the server's example RPC endpoint, and print what comes back
print(example(Example(txt="Hello World!", num=3)))

# Now invoke a super-secret SPICE simulation
print(secret_spice_sim(SecretSpiceSimulationInput(w=1000, l=150, v=1000)))

simulate_that_opamp(OpAmpParams())

elaborate_that_opamp_here_and_simulate_on_the_server(OpAmpParams())
