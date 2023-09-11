"""
Use this script to train an AutoCkt agent that knows how to optimize
a specific circuit within some constraints.
"""


if __name__ != "__main__":
    raise Exception("This is a SCRIPT and should be run as __main__!")


# Local Imports
from validate import run

from autockt.trainer import (
    autockt_train,
)
from autockt.autockt_gym_env_config import (
    CircuitOptimization,
    AutoCktGymEnvConfig,
    ParamSpecs,
    ParamSpec,
    MetricSpecs,
    MetricSpec,
)
from example_client import (
    AutoCktInput,
    AutoCktOutput,
    auto_ckt_sim,
)
from eval_engines.rewards import (
    settaluri_reward,
)


def main():
    circuit_optimization = CircuitOptimization(
        params=ParamSpecs(
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
        specs=MetricSpecs(  # FIXME Numbers right?
            [
                MetricSpec("gain", (200, 400), normalize=350),
                MetricSpec("ugbw", (1.0e6, 2.5e7), normalize=9.5e5),
                MetricSpec("phm", (60, 60.0000001), normalize=60),
                MetricSpec("ibias", (0.0001, 0.01), normalize=0.001),
            ]
        ),
        input_type=AutoCktInput,
        output_type=AutoCktOutput,
        simulation=auto_ckt_sim,
        reward=settaluri_reward,
    )

    gym_env_config = AutoCktGymEnvConfig(
        circuit_optimization=circuit_optimization,
        actions_per_param=[-1, 0, 2],
    )

    config_train = {
        # "sample_batch_size": 200,
        "train_batch_size": 1200,
        # "sgd_minibatch_size": 1200,
        # "num_sgd_iter": 3,
        # "lr":1e-3,
        # "vf_loss_coeff": 0.5,
        "horizon": 30,
        "num_gpus": 0,
        "model": {
            "fcnet_hiddens": [64, 64],
        },
        "num_workers": 1,
        "env_config": gym_env_config,  # a kwarg to the env constructor
        # "disable_env_checking": True,
    }

    # run validate
    run(config_train)


if __name__ == "__main__":
    main()
