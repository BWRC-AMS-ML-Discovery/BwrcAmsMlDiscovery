# Std-Lib Imports
from enum import Enum
from typing import Optional, Tuple


# PyPi Imports
import hdl21 as h

# Workspace Imports
from discovery_shared.dataclasses import dataclass
from discovery_shared.rpc import Rpc
from example_shared import AutoCktInput, AutoCktOutput

auto_ckt_sim = Rpc(
    name="auto_ckt_sim",
    input_type=AutoCktInput,
    return_type=AutoCktOutput,
    docstring="AutoCkt OpAmp",
)