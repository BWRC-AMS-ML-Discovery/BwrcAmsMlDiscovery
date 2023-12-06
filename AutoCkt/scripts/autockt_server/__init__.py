"""
# AutoCkt Server
"""

# Workspace Imports
import discovery_server as ds
from discovery_server import Config
from autockt_shared import (
    # These are not used here, but "re-exported"
    FlipFlopInput,
    FlipFlopOutput,
    FoldedCascodeInput,
    LDOInput,
    LDOOutput,
    LatchInput,
    LatchOutput,
    TwoStageOpAmpNgmInput,
    # Used here:
    OpAmpInput,
    OpAmpOutput,
    latch_sim,
    flip_flop_sim,
    folded_cascode_sim,
    ldo_sim,
    two_stage_op_amp_ngm_sim,
    auto_ckt_sim,
    auto_ckt_sim_hdl21,
)

# Local implementations
from . import opamps, Latch, FF, LDO

#
# Primary Action:
# Affix implementations to RPCs
#

## OpAmps
auto_ckt_sim_hdl21.impl(opamps.TwoStageOpAmp.opamp_inner)
folded_cascode_sim.impl(opamps.FoldedCascode.endpoint)
two_stage_op_amp_ngm_sim.impl(opamps.TwoStageOpAmp_ngm.two_stage_op_amp_ngm_sim)

## Others
latch_sim.impl(Latch.latch_sim)
flip_flop_sim.impl(FF.flip_flop_sim)
ldo_sim.impl(LDO.ldo_sim)


def start_server(cfg: Config):
    """Retrieve values from .env and then configure and start the server"""
    # FIXME NOTE: you're not retrieving anything from any .env here chief!

    ds.configure(cfg)
    ds.start_server()


"""
FIXME: 
Get rid of this whole "original AutoCkt" / netlist-templating setup. 
Or at least rename it to reflect what it is. 
"""


@auto_ckt_sim.impl
def auto_ckt_sim(inp: OpAmpInput) -> OpAmpOutput:
    """
    AutoCkt Simulation
    """
    from .auto_ckt_sim_lib import (
        create_design,
        simulate,
        translate_result,
    )

    # print(f"input {inp}")
    tmpdir, design_folder, fpath = create_design(inp)

    # print(f"design created {design_folder}")
    # TODO Error return?
    info = simulate(fpath)

    # print(f"simualted {info}")

    specs = translate_result(tmpdir, design_folder)
    # print(f"to specs {specs}")
    return specs
