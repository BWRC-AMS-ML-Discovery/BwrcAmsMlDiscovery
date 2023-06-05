# Std-Lib Imports
from typing import Callable, Type, Dict

# Local Imports
from .dataclasses import dataclass

_rpcs: Dict[str, "Rpc"] = dict()


@dataclass
class Rpc:
    """
    # Remote Procedure Call
    Shared server-client code
    """

    name: str  # RPC name. Serves as the endpoint name.
    func: Callable  # Function to be called
    input_type: Type  # Input type
    output_type: Type  # Output type

    def __post_init_post_parse__(self):
        """# Register the RPC"""
        if self.name in _rpcs:
            raise ValueError(f"RPC {self.name} already exists")
        _rpcs[self.name] = self
