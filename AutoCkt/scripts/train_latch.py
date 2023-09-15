from autockt_shared import (
    LatchInput,
    LatchOutput,
    latch_sim,
)
from autockt_shared.cktopt import (
    AutoCktCircuitOptimization,
    AutoCktParam,
    AutoCktParams,
    AutoCktSpec,
    AutoCktSpecs,
)
from autockt_shared.rewards import latch_reward


circuit_optimization = AutoCktCircuitOptimization(
    params=AutoCktParams(
        [
            AutoCktParam("w1", (1, 100), step=1, init=10),
            AutoCktParam("w2", (1, 100), step=1, init=20),
            AutoCktParam("w3", (1, 100), step=1, init=10),
            AutoCktParam("w4", (1, 100), step=1, init=20),
            AutoCktParam("w5", (1, 100), step=1, init=10),
            AutoCktParam("w6", (1, 100), step=1, init=20),
            AutoCktParam("w7", (1, 100), step=1, init=20),
            AutoCktParam("w8", (1, 100), step=1, init=20),
            AutoCktParam("w9", (1, 100), step=1, init=10),
            AutoCktParam("w10", (1, 100), step=1, init=10),
        ]
    ),
    specs=AutoCktSpecs(
        # TODO Change these
        [
            AutoCktSpec("delay", (0, 10e-9), normalize=1e-9),
            AutoCktSpec("setup_time", (0, 10e-9), normalize=1e-9),
            AutoCktSpec("hold_time", (0, 10e-9), normalize=1e-9),
            AutoCktSpec("ibias", (0, 1), normalize=1e-3),
        ]
    ),
    input_type=LatchInput,
    output_type=LatchOutput,
    simulation=latch_sim,
    reward=latch_reward,
)
