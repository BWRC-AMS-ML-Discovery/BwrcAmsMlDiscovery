# Std-Lib Imports
from dataclasses import asdict

# PyPi Imports
from dotenv import dotenv_values

# Workspace Imports
from example_shared import (
    example,
    Example,
)

# Importing the client library will create client stubs for all defined RPCs, including all those functions above.
import discovery_client as _


"""
Now we can just call the RPCs as though they were implemented locally.
"""

def do_example_stuff():
    """# Call a few example RPCs"""
    example_resp = example(Example(txt="Hello", num=3))
    print(example_resp)

   