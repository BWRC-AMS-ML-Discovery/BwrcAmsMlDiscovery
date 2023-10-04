# Std-Lib Imports
from dataclasses import dataclass

# Workspace Imports
from discovery_shared import Rpc
from pydantic import Field

# Local Imports
from .opamp_output import OpAmpOutput
from .rewards import settaluri_reward
from .cktopt import (
    CircuitOptimization,
    MetricSpec,
    MetricSpecs,
    ParamSpec,
    ParamSpecs,
)


from dataclasses import asdict


def as_hdl21_paramclass(data):
    """
    Convert a dataclass to a Hdl21 parameter class
    """
    return hdl21_paramclass[type(data)](
        **asdict(data),
    )


def as_param_specs(dataclass_type):
    """
    Convert a dataclass to a ParamSpecs
    """
    return ParamSpecs(
        [
            ParamSpec(
                name=field.name,
                range=(field.default.ge, field.default.le),
                step=field.default.extra["step"],
                init=field.default.default,
            )
            for field in dataclass_type.__dataclass_fields__.values()
        ]
    )


def as_target_specs(dataclass_type):
    """
    Convert a dataclass to a MetricSpecs
    """
    return MetricSpecs(
        [
            MetricSpec(
                name=field.name,
                range=(field.default.ge, field.default.le),
                normalize=field.default.extra["normalize"],
            )
            for field in dataclass_type.__dataclass_fields__.values()
        ]
    )


@dataclass
class OpAmpInput:
    """
    Input type for AutoCkt library, a state of result
    """

    mp1: int = Field(
        description="number of units of specific pmos transistor",
        default=34,
        ge=1,
        le=100,
        step=1,
    )
    mn1: int = Field(
        description="number of units of specific nmos transistor",
        default=34,
        ge=1,
        le=100,
        step=1,
    )
    mp3: int = Field(
        description="number of units of specific pmos transistor",
        default=34,
        ge=1,
        le=100,
        step=1,
    )
    mn3: int = Field(
        description="number of units of specific nmos transistor",
        default=34,
        ge=1,
        le=100,
        step=1,
    )
    mn4: int = Field(
        description="number of units of specific nmos transistor",
        default=34,
        ge=1,
        le=100,
        step=1,
    )
    mn5: int = Field(
        description="number of units of specific nmos transistor",
        default=15,
        ge=1,
        le=100,
        step=1,
    )
    cc: float = Field(
        description="capacitance of specific capacitor",
        default=2.1e-12,
        ge=0.1e-12,
        le=10.0e-12,
        step=0.1e-12,
    )  # Or maybe `str`, or the Hdl21/ VLSIR `Prefixed` fixed-point type


@dataclass
class OpAmpOutput:
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
    specs=as_target_specs(OpAmpOutput),
    input_type=OpAmpInput,
    output_type=OpAmpOutput,
    simulation=auto_ckt_sim,
    reward=settaluri_reward,
)
