import os
from pathlib import Path
from copy import deepcopy
import hdl21 as h
import hdl21.sim as hs
import vlsirtools.spice as vsp
from hdl21.external_module import SpiceType
from hdl21.prefix import µ, NANO

from ..opamps.TwoStageOpAmp import OpAmp


def test_nothing():
    # seriously what are we doin here.
    ...
