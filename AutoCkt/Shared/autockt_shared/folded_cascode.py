# Std-Lib Imports
from pydantic.dataclasses import dataclass, Field

# Workspace Imports
from discovery_shared import Rpc

# Local Imports
from .opamp_output import OpAmpOutput
from .rewards import settaluri_reward
from .typing import as_param_specs
from .cktopt import CircuitOptimization, MetricSpec, MetricSpecs


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
class FoldedCascodeInput:
    """# Folded Cascode Input
    Generator parameters and optimization ranges for the `Fcasc` generator."""

    # Unit device sizes
    nbias: int = intparam("Bias Nmos Unit Width", 2)
    pbias: int = intparam("Bias Pmos Unit Width", 4)
    ncasc: int = intparam("Cascode Nmos Unit Width", 2)
    pcasc: int = intparam("Cascode Pmos Unit Width", 4)
    ninp: int = intparam("Input Nmos Unit Width", 2)
    pinp: int = intparam("Input Pmos Unit Width", 4)

    # Current Mirror Ratios
    alpha: int = intparam("Alpha (Pmos Input) Current Ratio", 2)
    beta: int = intparam("Beta (Nmos Input) Current Ratio", 2)
    gamma: int = intparam("Gamma (Output Cascode) Current Ratio", 2)

    # Other
    vcb: int = Field(
        description="Cascode Bias Voltage (mV)",
        default=200,
        ge=50,
        le=350,
        step=10,
    )
    cc: int = Field(
        description="Load/ Compensation Cap Value (fF)",
        default=1000,
        ge=10,
        le=10_000,
        step=10,
    )


folded_cascode_sim = Rpc(
    name="folded_cascode_sim",
    input_type=FoldedCascodeInput,
    return_type=OpAmpOutput,
    docstring="FoldedCascode simulation",
)


circuit_optimization = CircuitOptimization(
    params=as_param_specs(FoldedCascodeInput),
    specs=MetricSpecs(
        [
            MetricSpec("gain", (200, 400), normalize=350),
            MetricSpec("ugbw", (1.0e6, 2.5e7), normalize=9.5e5),
            MetricSpec("phm", (60, 60.0000001), normalize=60),
            MetricSpec("ibias", (0.0001, 0.01), normalize=0.001),
        ]
    ),
    input_type=FoldedCascodeInput,
    output_type=OpAmpOutput,
    simulation=folded_cascode_sim,
    reward=settaluri_reward,
)
