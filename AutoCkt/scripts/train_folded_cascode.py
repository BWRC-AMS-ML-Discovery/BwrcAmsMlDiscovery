from example_shared import (
    FoldedCascodeInput,
    FoldedCascodeOutput,
    folded_cascode_sim,
)
from AutoCkt.Auto.autockt.autockt_gym_env_config import (
    CircuitOptimization,
    ParamSpec,
    ParamSpecs,
    MetricSpec,
    MetricSpecs,
)
from AutoCkt.Ckt.eval_engines.rewards import folded_cascode_reward


circuit_optimization = CircuitOptimization(
    params=ParamSpecs(
        # TODO Change these
        [
            ParamSpec("w1_2", (2, 24), step=2, init=10),
            ParamSpec("w5_6", (2, 24), step=2, init=10),
            ParamSpec("w7_8", (2, 24), step=2, init=10),
            ParamSpec("w9_10", (2, 24), step=2, init=10),
            ParamSpec("w11_12", (2, 24), step=2, init=10),
            ParamSpec("w13_14", (2, 24), step=2, init=10),
            ParamSpec("w15_16", (2, 24), step=2, init=10),
            ParamSpec("cl", (8e-15, 30e-15), step=2e-15, init=10e-15),
            ParamSpec("cc", (0.1e-12, 10.0e-12), step=0.1e-12, init=2.1e-12),
            ParamSpec("rc", (0.1e-12, 10.0e-12), step=0.1e-12, init=2.1e-12),
        ]
    ),
    specs=MetricSpecs(
        # TODO Change these
        [
            MetricSpec("gain", (200, 400), normalize=350),
            MetricSpec("ugbw", (1.0e6, 2.5e7), normalize=9.5e5),
            MetricSpec("phm", (60, 60.0000001), normalize=60),
            MetricSpec("ibias", (0.0001, 0.01), normalize=0.001),
        ]
    ),
    input_type=FoldedCascodeInput,
    output_type=FoldedCascodeOutput,
    simulation=folded_cascode_sim,
    reward=folded_cascode_reward,
)
