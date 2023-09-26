"""
# Example Discovery App
Shared server-client code
"""

import hdl21 as h
import hdl21.sim as hs
from hdl21.primitives import MosParams

from pydantic import Field, validator


# Workspace Imports
from discovery_shared.dataclasses import dataclass
from discovery_shared.rpc import Rpc
from example_shared.hdl21_paramclass import hdl21_paramclass, like_hdl21_paramclass


# Import the inverter schematic
from .inverter import inverter


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


@like_hdl21_paramclass
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


@h.generator
def RingOsc(params: hdl21_paramclass[RingOscInput]) -> h.Module:
    """A three-stage ring oscillator"""

    mos = MosParams()

    @h.module
    class RingOsc:
        VDD, VSS = h.Inputs(2)
        a = h.Outputs(params.num_inverters)

        for i in range(params.num_inverters):
            ia = inverter(mos)(inp=a[i], out=a[i + 1], VDD=VDD, VSS=VSS)

    return RingOsc


def RingOscSim(params: hdl21_paramclass[RingOscInput]) -> hs.Sim:
    @hs.sim
    class RingOscSim:
        """
        TODO
        """

        instance = RingOsc(params)

    return RingOscSim


@ring_osc.impl
def ring_osc(params: RingOscInput) -> RingOscOutput:
    """# Ring Oscillator"""

    sim = RingOscSim(params)
    result = sim.run(1e-9)

    return RingOscOutput(
        frequency=1 / result.ia.tpd,
    )


# * We can also implement "@like_autockt_paramspec" and "@like_autockt_targetspec"
