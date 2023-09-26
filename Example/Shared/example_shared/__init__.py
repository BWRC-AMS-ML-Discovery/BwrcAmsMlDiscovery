"""
# Example Discovery App
Shared server-client code
"""

import hdl21 as h

from pydantic import Field, validator


# Workspace Imports
from discovery_shared.dataclasses import dataclass
from discovery_shared.rpc import Rpc


@dataclass
class Example:
    """# Example of a dataclass that can be used as a POST body"""

    txt: str
    num: int


example = Rpc(
    name="example",
    input_type=Example,
    return_type=Example,
    docstring="Example RPC",
)


@dataclass
class RingOscInput:
    num_inverters: int = Field(
        description="Number of inverters in the ring oscillator",
        default=3,
        ge=1,
        le=9,
        step=2,
    )

    @validator("num_inverters")
    def num_inverters_must_be_odd(cls, v):
        assert v % 2 == 1
        return v


@dataclass
class RingOscOutput:
    frequency: float = Field(
        description="Frequency of the ring oscillator (MHz)",
        ge=0,
        le=100,
        step=0.1,
        normalize=50,
    )

    assert frequency.extra["normalize"] >= frequency.ge
    assert frequency.extra["normalize"] <= frequency.le


ring_osc = Rpc(
    name="ring_osc",
    input_type=RingOscInput,
    return_type=RingOscOutput,
    docstring="Ring Oscillator RPC",
)


def dataclass_to_hdl21_paramclass(dataclass: type) -> h.Type:
    """Convert a dataclass to an hdl21 Paramclass"""

    class Params:
        pass

    # Add all the fields from the dataclass
    for field in dataclass.__dataclass_fields__.values():
        param = h.Param(
            dtype=field.type,
            desc=field.metadata.get("description", ""),
            default=field.default,
            # ge=field.metadata.get("ge", None),
            # le=field.metadata.get("le", None),
            # step=field.metadata.get("step", None),
            # normalize=field.metadata.get("normalize", None),
        )

        setattr(Params, field.name, param)

    return h.paramclass(Params)
