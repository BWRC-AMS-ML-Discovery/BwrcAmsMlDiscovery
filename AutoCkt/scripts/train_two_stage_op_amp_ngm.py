from example_shared import (
    TwoStageOpAmpNgmInput,
    TwoStageOpAmpNgmOutput,
    two_stage_op_amp_ngm_sim,
)
from AutoCkt.Auto.autockt.autockt_gym_env_config import (
    CircuitOptimization,
    ParamSpec,
    ParamSpecs,
    MetricSpec,
    MetricSpecs,
)
from AutoCkt.Ckt.eval_engines.rewards import two_stage_op_amp_ngm_reward


circuit_optimization = CircuitOptimization(
    params=ParamSpecs(
        # TODO Change these
        [
            ParamSpec("wtail1", (4, 20), step=2, init=10),
            ParamSpec("wtail2", (4, 20), step=2, init=10),
            ParamSpec("wcm", (4, 20), step=2, init=10),
            ParamSpec("win", (4, 20), step=2, init=10),
            ParamSpec("wref", (4, 20), step=2, init=10),
            ParamSpec("wd1", (4, 20), step=2, init=10),
            ParamSpec("wd", (4, 20), step=2, init=10),
            ParamSpec("wn_gm", (4, 20), step=2, init=10),
            ParamSpec("wtail", (4, 20), step=2, init=10),
            ParamSpec("wtailr", (4, 20), step=2, init=10),
            ParamSpec("Cc", (10e-15, 150e-15), step=5e-15, init=10e-15),
            ParamSpec("Rf", (0.1e3, 6e3), step=0.1e3, init=1e3),
        ]
    ),
    specs=MetricSpecs(
        # TODO Change these
        [
            MetricSpec("gain", (1, 40), normalize=10),
            MetricSpec("ugbw", (1.0e6, 2.5e7), normalize=9.5e5),
            MetricSpec("phm", (60, 75), normalize=60),
            MetricSpec("ibias", (0.0001, 0.01), normalize=0.001),
        ]
    ),
    input_type=TwoStageOpAmpNgmInput,
    output_type=TwoStageOpAmpNgmOutput,
    simulation=two_stage_op_amp_ngm_sim,
    reward=two_stage_op_amp_ngm_reward,
)
