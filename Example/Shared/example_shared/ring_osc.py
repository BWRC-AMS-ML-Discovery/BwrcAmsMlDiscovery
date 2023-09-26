"""
# Ring Oscillator

Using the inverter delay element defined in `inverter.sch.svg`.
"""

import hdl21 as h
import hdl21.sim as hs
from hdl21.primitives import MosParams
import hdl21schematicimporter as _

# Import the inverter schematic
from .inverter import inverter

# Just in case you don't believe this:
assert isinstance(inverter, h.Generator)
