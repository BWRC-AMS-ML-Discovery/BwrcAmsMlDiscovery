""" 
# Parameters
"""

from typing import Optional
import hdl21 as h


@h.paramclass
class TbParams:
    """# Testbench Parameters"""

    # Required
    dut = h.Param(dtype=h.Instantiable, desc="Design Under Test")
    VDD = h.Param(dtype=h.Scalar, desc="VDD voltage")
    ibias = h.Param(dtype=h.Scalar, desc="ibias current")
    # Optional
    cl = h.Param(dtype=Optional[h.Scalar], desc="Load Cap", default=None)
    vicm = h.Param(dtype=Optional[h.Scalar], desc="Input common-mode", default=None)
