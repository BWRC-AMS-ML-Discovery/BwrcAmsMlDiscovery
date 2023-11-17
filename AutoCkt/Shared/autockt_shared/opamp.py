# Std-Lib Imports
from pydantic.dataclasses import dataclass, Field

# Workspace Imports
from discovery_shared import Rpc

# Local Imports
from .opamp_output import OpAmpOutput
from .rewards import settaluri_reward
from .cktopt import CircuitOptimization
from .typing import as_param_specs, as_target_specs


def intparam(desc: str, default: int = 4) -> Field:
    """# Positive integer-valued parameter"""
    return Field(
        description=desc,
        default=default,
        ge=1,
        le=100,
        step=1,
    )


@dataclass
class OpAmpInput:
    """
    Input type for AutoCkt library, a state of result
    """

    # Unit device sizes
    nbias: int = intparam("Bias Nmos Unit Width", 2)
    ninp: int = intparam("Input Nmos Unit Width", 2)
    pmoses: int = intparam("Pmos Unit Width", 2)

    # Current Mirror Ratios
    alpha: int = intparam("Alpha (Input) Current Ratio", 40)
    beta: int = intparam("Beta (Output) Current Ratio", 40)

    # Other
    cc: int = Field(
        description="Compensation Cap Value (fF)",
        default=1000,
        ge=10,
        le=10_000,
        step=10,
    )


@dataclass
class OpAmpOutputTargets(OpAmpOutput):
    """# Op-Amp Output
    Server output type reused by several op-amp flavors"""

    gain: float = Field(
        description="gain of the op-amp",
        ge=200,
        le=400,
        normalize=350,
    )
    ugbw: float = Field(
        description="unity gain bandwidth of the op-amp",
        ge=1.0e6,
        le=2.5e7,
        normalize=9.5e5,
    )
    phm: float = Field(
        description="phase margin of the op-amp",
        ge=60,
        le=60.0000001,
        normalize=60,
    )
    ibias: float = Field(
        description="bias current of the op-amp",
        ge=0.0001,
        le=0.01,
        normalize=0.001,
    )


auto_ckt_sim = Rpc(
    name="auto_ckt_sim",
    input_type=OpAmpInput,
    return_type=OpAmpOutput,
    docstring="Simulation on the Server",
)

auto_ckt_sim_hdl21 = Rpc(
    name="auto_ckt_sim_hdl21",
    input_type=OpAmpInput,
    return_type=OpAmpOutput,
    docstring="Simulation on the Server",
)


circuit_optimization = CircuitOptimization(
    params=as_param_specs(OpAmpInput),
    specs=as_target_specs(OpAmpOutputTargets),
    input_type=OpAmpInput,
    output_type=OpAmpOutput,
    simulation=auto_ckt_sim_hdl21,
    reward=settaluri_reward,
)
