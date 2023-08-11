from example_shared import (
    LatchInput,
    LatchOutput,
    latch_sim,
)
from AutoCkt.Auto.autockt.autockt_gym_env_config import (
    AutoCktCircuitOptimization,
    AutoCktParam,
    AutoCktParams,
    AutoCktSpec,
    AutoCktSpecs,
)
from AutoCkt.Ckt.eval_engines.rewards import latch_reward


circuit_optimization = AutoCktCircuitOptimization(
    params=AutoCktParams(
        # TODO Change these
        [
            AutoCktParam("mp1", (1, 100), step=1, init=34),
            AutoCktParam("mn1", (1, 100), step=1, init=34),
            AutoCktParam("mp3", (1, 100), step=1, init=34),
            AutoCktParam("mn3", (1, 100), step=1, init=34),
            AutoCktParam("mn4", (1, 100), step=1, init=34),
            AutoCktParam("mn5", (1, 100), step=1, init=15),
            AutoCktParam("cc", (0.1e-12, 10.0e-12), step=0.1e-12, init=2.1e-12),
        ]
    ),
    specs=AutoCktSpecs(
        # TODO Change these
        [
            AutoCktSpec("gain", (200, 400), normalize=350),
            AutoCktSpec("ugbw", (1.0e6, 2.5e7), normalize=9.5e5),
            AutoCktSpec("phm", (60, 60.0000001), normalize=60),
            AutoCktSpec("ibias", (0.0001, 0.01), normalize=0.001),
        ]
    ),
    input_type=LatchInput,
    output_type=LatchOutput,
    simulation=latch_sim,
    reward=latch_reward,
)
