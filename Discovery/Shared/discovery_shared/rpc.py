"""
# RPC 

Generate client-server pairs. 
RPC definitions include: 

* A function name
* An input type
* A return type

All defined RPCs are stored in a global registry which can be accessed by name.  
The Discovery client library transforms each into a callable client-side function.  
Server-side code can decorate an implementation function with `@{rpc}.impl` to register it as the implementation of an RPC.

Example:

```python
# Example / Shared

@dataclass
class Input:
    ...

@dataclass
class Output:
    ...

my_rpc = Rpc(
    name="my_rpc",
    input_type=Input,
    return_type=Output,
    docstring="My RPC",
)
```

```python
# Example / Server

from example_shared import my_rpc, Input, Output

# Define the server-side implementation of `my_rpc`
@my_rpc.impl
def my_function(inp: Input) -> Output:
    ... # Do the actual server-side stuff
    return Output(...)
```

```python
# Example / Client

from example_shared import my_rpc, Input, Output

# "Do nothing"; just start calling `my_rpc` as if it were a client-defined function.
input = Input(...)
output = my_rpc(input) # Returns an `Output` object

```

"""

# Std-Lib Imports
import inspect
from dataclasses import is_dataclass
from typing import Callable, Type, Dict

# Local Imports
from .dataclasses import dataclass


@dataclass
class Rpc:
    """
    # Remote Procedure Call
    Shared server-client code
    """

    name: str  # RPC name. Serves as the endpoint name.
    input_type: Type  # Input type
    return_type: Type  # Return type

    docstring: str = ""  # Docstring
    # Inner Function
    # An http POST in the client, and a function call in the server
    func: Callable | None = None

    def __post_init__(self) -> "Rpc":
        # Register to dictionary
        rpcs[self.name] = self

    def __call__(self, *args, **kwargs) -> "self.return_type":
        """# Call our RPC function
        Dispatches to the inner callable.
        This would only be invoked if directly importing from the shared version, but should remain handy.
        Our return-type annotation here is pseudo-code, but you get the point."""
        return self.func(*args, **kwargs)

    def impl(self, f: Callable) -> "Rpc":
        """# Implement our RPC function
        Set the inner callable to `f`."""
        if self.func is not None:
            raise RuntimeError(f"RPC {self.name} already has a function defined")
        # FIXME: probably add checks on the signature of `f` here
        self.func = f
        return self


# All the "registered" RPC functions
rpcs: Dict[str, Rpc] = dict()


def _rpc(f: Callable) -> Rpc:
    """# RPC Decorator
    Wrap function `f` in an `Rpc` which can be interpreted by both client-side and server-side code.
    """

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
