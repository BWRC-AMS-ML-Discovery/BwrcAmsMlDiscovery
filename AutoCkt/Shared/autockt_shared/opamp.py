# Std-Lib Imports
from dataclasses import dataclass

# Workspace Imports
from discovery_shared import Rpc

# Local Imports
from .opamp_output import OpAmpOutput
from .rewards import settaluri_reward
from .cktopt import (
    AutoCktCircuitOptimization,
    AutoCktSpec,
    AutoCktSpecs,
    AutoCktParam,
    AutoCktParams,
    Number,
)


@dataclass
class OpAmpInput:
    """
    Input type for AutoCkt library, a state of result
    """

    mp1: int  # number of units of specific pmos transistor
    mn1: int  # number of units of specific nmos transistor
    mp3: int  # number of units of specific pmos transistor
    mn3: int  # number of units of specific nmos transistor
    mn4: int  # number of units of specific nmos transistor
    mn5: int  # number of units of specific nmos transistor
    cc: float  # Or maybe `str`, or the Hdl21/ VLSIR `Prefixed` fixed-point type


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


circuit_optimization = AutoCktCircuitOptimization(
    params=AutoCktParams(
        [
            AutoCktParam("mp1", (1, 100), step=1, init=34),
            AutoCktParam("mn1", (1, 100), step=1, init=34),
            AutoCktParam("mp3", (1, 100), step=1, init=34),
            AutoCktParam("mn3", (1, 100), step=1, init=34),
            AutoCktParam("mn4", (1, 100), step=1, init=34),
            AutoCktParam("mn5", (1, 100), step=1, init=15),
            AutoCktParam("cc", (0.1e-12, 10.0e-12), step=0.1e-12, init=2.1e-12),
        ]
    ),
    specs=AutoCktSpecs(  # FIXME Numbers right?
        [
            AutoCktSpec("gain", (200, 400), normalize=350),
            AutoCktSpec("ugbw", (1.0e6, 2.5e7), normalize=9.5e5),
            AutoCktSpec("phm", (60, 60.0000001), normalize=60),
            AutoCktSpec("ibias", (0.0001, 0.01), normalize=0.001),
        ]
    ),
    input_type=OpAmpInput,
    output_type=OpAmpOutput,
    simulation=auto_ckt_sim,
    reward=settaluri_reward,
)
