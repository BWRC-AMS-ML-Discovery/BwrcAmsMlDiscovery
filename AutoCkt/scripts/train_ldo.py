from example_shared import (
    LDOInput,
    LDOOutput,
    ldo_sim,
)
from AutoCkt.Auto.autockt.autockt_gym_env_config import (
    CircuitOptimization,
    ParamSpec,
    ParamSpecs,
    MetricSpec,
    MetricSpecs,
)
from AutoCkt.Ckt.eval_engines.rewards import ldo_reward


circuit_optimization = CircuitOptimization(
    params=ParamSpecs(
        # TODO Change these
        # TODO Action space for length of MOS (14nm, 100nm, 200nm)
        [
            ParamSpec("w1", (1, 100), step=1, init=10),
            ParamSpec("w2", (1, 100), step=1, init=10),
            ParamSpec("w3", (1, 100), step=1, init=10),
            ParamSpec("w4", (1, 100), step=1, init=10),
            ParamSpec("w5", (1, 100), step=1, init=10),
            ParamSpec("w6", (1, 100), step=1, init=10),
            ParamSpec("w7r", (1, 100), step=1, init=10),
            ParamSpec("w8", (1, 100), step=1, init=10),
            ParamSpec("w9", (1, 100), step=1, init=10),
            ParamSpec("w10", (1, 100), step=1, init=10),
            ParamSpec("wpass", (1, 100), step=1, init=10),
            ParamSpec("w1", (1, 100), step=1, init=10),
            ParamSpec("w1", (1, 100), step=1, init=10),
            ParamSpec("w1", (1, 100), step=1, init=10),
            ParamSpec("w1", (1, 100), step=1, init=10),
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
            MetricSpec("gain", (200, 400), normalize=350),
            MetricSpec("ugbw", (1.0e6, 2.5e7), normalize=9.5e5),
            MetricSpec("phm", (60, 60.0000001), normalize=60),
            MetricSpec("ibias", (0.0001, 0.01), normalize=0.001),
        ]
    ),
    input_type=LDOInput,
    output_type=LDOOutput,
    simulation=ldo_sim,
    reward=ldo_reward,
)
