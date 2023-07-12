from example_client import (
    auto_ckt_sim_hdl21,
    AutoCktInput,
    AutoCktOutput,
)

inp = AutoCktInput(3, 3, 3, 3, 3, 3, 1e-12)
out = auto_ckt_sim_hdl21(inp)
print(out)
