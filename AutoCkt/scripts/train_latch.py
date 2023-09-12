from example_shared import (
    LatchInput,
    LatchOutput,
    latch_sim,
)
from AutoCkt.Auto.autockt.autockt_gym_env_config import (
    CircuitOptimization,
    ParamSpec,
    ParamSpecs,
    MetricSpec,
    MetricSpecs,
)
from AutoCkt.Ckt.eval_engines.rewards import latch_reward


circuit_optimization = CircuitOptimization(
    params=ParamSpecs(
        [
            ParamSpec("w1", (1, 100), step=1, init=10),
            ParamSpec("w2", (1, 100), step=1, init=20),
            ParamSpec("w3", (1, 100), step=1, init=10),
            ParamSpec("w4", (1, 100), step=1, init=20),
            ParamSpec("w5", (1, 100), step=1, init=10),
            ParamSpec("w6", (1, 100), step=1, init=20),
            ParamSpec("w7", (1, 100), step=1, init=20),
            ParamSpec("w8", (1, 100), step=1, init=20),
            ParamSpec("w9", (1, 100), step=1, init=10),
            ParamSpec("w10", (1, 100), step=1, init=10),
        ]
    ),
    specs=MetricSpecs(
        # TODO Change these
        [
            MetricSpec("delay", (0, 10e-9), normalize=1e-9),
            MetricSpec("setup_time", (0, 10e-9), normalize=1e-9),
            MetricSpec("hold_time", (0, 10e-9), normalize=1e-9),
            MetricSpec("ibias", (0, 1), normalize=1e-3),
        ]
    ),
    input_type=LatchInput,
    output_type=LatchOutput,
    simulation=latch_sim,
    reward=latch_reward,
)
