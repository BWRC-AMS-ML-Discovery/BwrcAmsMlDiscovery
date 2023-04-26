"""
# RPC 

Generate client-server pairs via an `@rpc` decorator applied to a "core" server-side "action function". 
Example: 

```python
@rpc
def my_server_side_stuff(inp: Input) -> Output: 
    # Do the actual stuff you want the server to do
    something = do_sims_and_stuff(inp)
    return Output(**something)
```

Generates: 

* The endpoint `my_server_side_stuff`
  * Using `Input` as its argument-type and `Output` as its return-type
* The server-side wrapper 
* The client-side wrapper 

"""

# Std-Lib Imports
import inspect, functools
from dataclasses import is_dataclass, asdict
from typing import Callable, Type, Dict, Tuple

# Local Imports
from .dataclasses import dataclass


@dataclass
class Rpc:
    """
    # Remote Procedure Call
    Shared server-client code
    """

    name: str  # RPC name. Serves as the endpoint name.
    func: Callable  # Core Inner Function
    input_type: Type  # Input type
    return_type: Type  # Return type

    def __call__(self, *args, **kwargs) -> "self.return_type":
        """# Call our RPC function
        Dispatches to the inner callable.
        This would only be invoked if directly importing from the shared version, but should remain handy.
        Our return-type annotation here is pseudo-code, but you get the point."""
        return self.f(*args, **kwargs)


# All the "registered" RPC functions
rpcs: Dict[str, Rpc] = dict()


def rpc(f: Callable) -> Rpc:
    """# RPC Decorator
    Wrap function `f` in an `Rpc` which can be interpreted by both client-side and server-side code."""

    # Assert that our argument is a callable
    if not callable(f):
        raise RuntimeError(f"Invalid `@generator` application to non-callable {f}")

    # Check that it has a unique name, so as to not overwrite another entry point
    if f.__name__ in rpcs:
        raise ValueError(f"RPC {f.__name__} already exists")

    # Grab, parse, and validate its call-signature
    sig = inspect.signature(f)

    args = list(sig.parameters.values())
    if len(args) != 1:
        raise RuntimeError(f"RPC {f.__name__} must take a single argument")

    # Extract the parameters-argument type
    input_type = args[0].annotation
    if not is_dataclass(input_type):
        msg = f"RPC {f.__name__} argument must be a `dataclass`, not {input_type}"
        raise RuntimeError(msg)

    # Validate the return type is `Module`
    return_type = sig.return_annotation
    if not is_dataclass(return_type):
        msg = f"RPC {f.__name__} argument must be a `dataclass`, not {return_type}"
        raise RuntimeError(msg)

    # Create, store, and return the `Rpc` object
    rpc = Rpc(name=f.__name__, func=f, input_type=input_type, return_type=return_type)
    rpcs[f.__name__] = rpc
    return rpc


#
# Now, each of `client` and `server` can do something like:
#


def _do_this_in_client():
    # Import the list of RPCs
    from ..shared.rpc import rpcs

    def create_client_rpc(rpc: Rpc):
        """# Create the client function for `rpc`."""
        ## import httpx # This stuff, and the server URL, will be in the client module

        # The functools "function wrapper" will apply the docstring etc from `rpc.func`
        @functools.wraps(rpc.func)
        def client_wrapper(inp: rpc.input_type) -> rpc.return_type:
            url = f"http://{THE_SERVER_URL}/{rpc.name}"
            resp = httpx.post(url, json=asdict(inp))
            return rpc.return_type(**resp.json())

        return client_wrapper

    # Create one of those for each RPC
    for rpc in rpcs.values():
        create_client_rpc(rpc)


def _do_this_in_server():
    # And do something similar on the server
    for rpc in rpcs.values():
        create_server_rpc(rpc)


@dataclass
class ExampleMlInputs:
    """
    # Example ML Optimizer Inputs
    Now you can have inputs to your ML thing like so:
    """

    input_range: Tuple[int, int]
    initial_value_of_something: float

    # The point here: the objective function can be an `Rpc`
    the_objective_function: Rpc
