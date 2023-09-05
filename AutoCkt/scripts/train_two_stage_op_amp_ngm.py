from example_shared import (
    TwoStageOpAmpNgmInput,
    TwoStageOpAmpNgmOutput,
    two_stage_op_amp_ngm_sim,
)
from AutoCkt.Auto.autockt.autockt_gym_env_config import (
    AutoCktCircuitOptimization,
    AutoCktParam,
    AutoCktParams,
    AutoCktSpec,
    AutoCktSpecs,
)
from AutoCkt.Ckt.eval_engines.rewards import two_stage_op_amp_ngm_reward


circuit_optimization = AutoCktCircuitOptimization(
    params=AutoCktParams(
        # TODO Double Check these
        [
            AutoCktParam("wtail1", (4, 20), step=2, init=10),
            AutoCktParam("wtail2", (4, 20), step=2, init=10),
            AutoCktParam("wcm", (4, 20), step=2, init=10),
            AutoCktParam("win", (4, 20), step=2, init=10),
            AutoCktParam("wref", (4, 20), step=2, init=10),
            AutoCktParam("wd1", (4, 20), step=2, init=10),
            AutoCktParam("wd", (4, 20), step=2, init=10),
            AutoCktParam("wn_gm", (4, 20), step=2, init=10),
            AutoCktParam("wtail", (4, 20), step=2, init=10),
            AutoCktParam("wtailr", (4, 20), step=2, init=10),
            AutoCktParam("Cc", (10e-15, 150e-15), step=5e-15, init=10e-15),
            AutoCktParam("Rf", (0.1e3, 6e3), step=0.1e3, init=1e3),
        ]
    ),
    specs=AutoCktSpecs(
        # TODO Double Check these
        [
            AutoCktSpec("gain", (1, 40), normalize=10),
            AutoCktSpec("ugbw", (1.0e6, 2.5e7), normalize=9.5e5),
            AutoCktSpec("phm", (60, 75), normalize=60),
            AutoCktSpec("ibias", (0.0001, 0.01), normalize=0.001),
        ]
    ),
    input_type=TwoStageOpAmpNgmInput,
    output_type=TwoStageOpAmpNgmOutput,
    simulation=two_stage_op_amp_ngm_sim,
    reward=two_stage_op_amp_ngm_reward,
)
