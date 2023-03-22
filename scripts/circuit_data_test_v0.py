"""
# Circuit data test v0
"""

from discovery import *
from discovery.client import *

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def cprint(message, test):
    message = str(message)
    if test in message:
        print(bcolors.OKGREEN + message + bcolors.ENDC)
    else:
        print(bcolors.FAIL + message + bcolors.ENDC)

# Call the server's root endpoint.
# Gets a general health-indication of whether we can contact the server.
rootpoint_status = alive()
cprint(rootpoint_status, "alive")

# Call the server's example RPC endpoint, and print what comes back
print(example(Example(txt="Hello World!", num=3)))

# Now invoke a super-secret SPICE simulation
print(secret_spice_sim(SecretSpiceSimulationInput(w=1000, l=150, v=1000)))

# New test
new_module = create_module(TestModuleInput(new_name="test1", new_i=1, new_o=2, new_s=3))
print(new_module.tostring())