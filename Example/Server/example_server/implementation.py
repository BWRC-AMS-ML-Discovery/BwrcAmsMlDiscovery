# Workspace Imports
from example_shared import (
    example,
    Example,
    secret_spice,
    SecretSpiceSimulationInput,
    SecretSpiceSimulationOutput,
    simulate_that_opamp,
    OpAmpParams,
    VlsirProtoBufKind,
    VlsirProtoBufBinary,
    inverter_beta_ratio,
    InverterBetaRatioInput,
    InverterBetaRatioOutput,
    AutoCktInput,
    AutoCktOutput,
)

from example_shared.rpc_declaration import auto_ckt_sim

from .auto_ckt_sim_lib import (
    create_design,
    simulate,
    translate_result,
)
from example_shared.rpc_declaration import auto_ckt_sim


@auto_ckt_sim.impl
async def auto_ckt_sim_implementation(inp: AutoCktInput) -> AutoCktOutput:
    """
    AutoCkt Simulation
    """
    design_folder, fpath = create_design(inp)

    # Error return?
    info = simulate(fpath)

    specs = translate_result(design_folder)

    return specs