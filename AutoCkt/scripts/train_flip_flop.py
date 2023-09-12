from example_shared import (
    FlipFlopInput,
    FlipFlopOutput,
    flip_flop_sim,
)
from AutoCkt.Auto.autockt.autockt_gym_env_config import (
    CircuitOptimization,
    ParamSpec,
    ParamSpecs,
    MetricSpec,
    MetricSpecs,
)
from AutoCkt.Ckt.eval_engines.rewards import flip_flop_reward


circuit_optimization = CircuitOptimization(
    params=ParamSpecs(
        # TODO Change these
        [
            ParamSpec("mp1", (1, 100), step=1, init=34),
            ParamSpec("mn1", (1, 100), step=1, init=34),
            ParamSpec("mp3", (1, 100), step=1, init=34),
            ParamSpec("mn3", (1, 100), step=1, init=34),
            ParamSpec("mn4", (1, 100), step=1, init=34),
            ParamSpec("mn5", (1, 100), step=1, init=15),
            ParamSpec("cc", (0.1e-12, 10.0e-12), step=0.1e-12, init=2.1e-12),
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
    input_type=FlipFlopInput,
    output_type=FlipFlopOutput,
    simulation=flip_flop_sim,
    reward=flip_flop_reward,
)
