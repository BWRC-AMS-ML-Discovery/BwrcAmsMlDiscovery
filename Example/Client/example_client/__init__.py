# Std-Lib Imports
from dataclasses import asdict

# PyPi Imports
from dotenv import dotenv_values

# Workspace Imports
from example_shared import (
    example,
    Example,
)

from discovery_shared.rpc import Rpc

# Importing the client library will create client stubs for all defined RPCs, including all those functions above.
# import discovery_client as _


"""
Now we can just call the RPCs as though they were implemented locally.
"""

def do_example_stuff():
    """# Call a few example RPCs"""
    example_resp = example(Example(txt="Hello", num=3))
    return example_resp

def do_example_stuff_func(func):
    """# Call a few example RPCs"""
    test_rpc = Rpc(
        name="example",
        input_type=Example,
        return_type=Example,
        docstring="Example RPC",
        func = func
    )
    example_resp = test_rpc(Example(txt="Hello", num=1))
    return example_resp

   

   