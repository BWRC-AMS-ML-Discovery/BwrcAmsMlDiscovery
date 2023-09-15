from autockt_shared import (
    LDOInput,
    LDOOutput,
    ldo_sim,
)
from autockt_shared.cktopt import (
    AutoCktCircuitOptimization,
    AutoCktParam,
    AutoCktParams,
    AutoCktSpec,
    AutoCktSpecs,
)
from autockt_shared.rewards import ldo_reward


circuit_optimization = AutoCktCircuitOptimization(
    params=AutoCktParams(
        # TODO Change these
        # TODO Action space for length of MOS (14nm, 100nm, 200nm)
        [
            AutoCktParam("w1", (1, 40), step=1, init=10),
            AutoCktParam("w2", (1, 40), step=1, init=10),
            AutoCktParam("w3", (1, 40), step=1, init=10),
            AutoCktParam("w4", (1, 40), step=1, init=10),
            AutoCktParam("w5", (1, 40), step=1, init=10),
            AutoCktParam("w6", (1, 40), step=1, init=10),
            AutoCktParam("w7r", (1, 40), step=1, init=10),
            AutoCktParam("w8", (1, 40), step=1, init=10),
            AutoCktParam("w9", (1, 40), step=1, init=10),
            AutoCktParam("w10", (1, 40), step=1, init=10),
            AutoCktParam("wpass", (1, 40), step=1, init=10),
            AutoCktParam("w1", (1, 40), step=1, init=10),
            AutoCktParam("w1", (1, 40), step=1, init=10),
            AutoCktParam("w1", (1, 40), step=1, init=10),
            AutoCktParam("w1", (1, 40), step=1, init=10),
            AutoCktParam("mn1", (1, 40), step=1, init=34),
            AutoCktParam("mp3", (1, 40), step=1, init=34),
            AutoCktParam("mn3", (1, 40), step=1, init=34),
            AutoCktParam("mn4", (1, 40), step=1, init=34),
            AutoCktParam("mn5", (1, 40), step=1, init=15),
            AutoCktParam("cc", (0.1e-12, 10.0e-12), step=0.1e-12, init=2.1e-12),
        ]
    ),
    specs=AutoCktSpecs(
        # TODO Change these
        [
            AutoCktSpec("gain", (1, 2), normalize=1.5),
            AutoCktSpec("ugbw", (1.0e6, 2.5e7), normalize=9.5e5),
            AutoCktSpec("phm", (60, 60.0000001), normalize=60),
            AutoCktSpec("ibias", (0.0001, 0.01), normalize=0.001),
        ]
    ),
    input_type=LDOInput,
    output_type=LDOOutput,
    simulation=ldo_sim,
    reward=ldo_reward,
)
