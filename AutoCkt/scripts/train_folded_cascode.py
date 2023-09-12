from example_shared import (
    FoldedCascodeInput,
    FoldedCascodeOutput,
    folded_cascode_sim,
)
from AutoCkt.Auto.autockt.autockt_gym_env_config import (
    AutoCktCircuitOptimization,
    AutoCktParam,
    AutoCktParams,
    AutoCktSpec,
    AutoCktSpecs,
)
from AutoCkt.Ckt.eval_engines.rewards import folded_cascode_reward


circuit_optimization = AutoCktCircuitOptimization(
    params=AutoCktParams(
        # TODO Change these
        [
            AutoCktParam("w1_2", (2, 24), step=2, init=10),
            AutoCktParam("w5_6", (2, 24), step=2, init=10),
            AutoCktParam("w7_8", (2, 24), step=2, init=10),
            AutoCktParam("w9_10", (2, 24), step=2, init=10),
            AutoCktParam("w11_12", (2, 24), step=2, init=10),
            AutoCktParam("w13_14", (2, 24), step=2, init=10),
            AutoCktParam("w15_16", (2, 24), step=2, init=10),
            AutoCktParam("cl", (8e-15, 30e-15), step=2e-15, init=10e-15),
            AutoCktParam("cc", (0.1e-12, 10.0e-12), step=0.1e-12, init=2.1e-12),
            AutoCktParam("rc", (0.1e-12, 10.0e-12), step=0.1e-12, init=2.1e-12),
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
    input_type=FoldedCascodeInput,
    output_type=FoldedCascodeOutput,
    simulation=folded_cascode_sim,
    reward=folded_cascode_reward,
)
