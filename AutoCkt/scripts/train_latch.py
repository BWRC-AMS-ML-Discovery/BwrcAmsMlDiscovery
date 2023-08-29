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
            AutoCktSpec("delay", (200, 400), normalize=350),
            AutoCktSpec("setup_time", (1.0e6, 2.5e7), normalize=9.5e5),
            AutoCktSpec("hold_time", (60, 60.0000001), normalize=60),
            AutoCktSpec("ibias", (0.0001, 0.01), normalize=0.001),
        ]
    ),
    input_type=LatchInput,
    output_type=LatchOutput,
    simulation=latch_sim,
    reward=latch_reward,
)
