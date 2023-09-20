from autockt_shared import (
    auto_ckt_sim_hdl21,
    OpAmpInput,
)

inp = OpAmpInput(3, 3, 3, 3, 3, 3, 1e-12)
out = auto_ckt_sim_hdl21(inp)
print(out)
