""" 
# Parameters
"""

from typing import Optional, List
import hdl21 as h


@h.paramclass
class TbParams:
    """# Testbench Parameters"""

    dut = h.Param(dtype=h.Instantiable, desc="Design Under Test")
    VDD = h.Param(dtype=h.Scalar, desc="VDD voltage")
    ibias = h.Param(dtype=h.Scalar, desc="ibias current")
