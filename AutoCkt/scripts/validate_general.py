"""
Use this script to train an AutoCkt agent that knows how to optimize
a specific circuit within some constraints.
"""


if __name__ != "__main__":
    raise Exception("This is a SCRIPT and should be run as __main__!")


# Local Imports
from validate import run  # FIXME: what/ where is this?
from autockt_shared.cktopt import CircuitOptimization, AutoCktGymEnvConfig


def main(
    circuit_optimization: CircuitOptimization,
    num_workers: int = 1,
):
    """# Entry point for a validation script, running `circuit_optimization`."""

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
        "num_workers": num_workers,
        "env_config": gym_env_config,  # a kwarg to the env constructor
        # "disable_env_checking": True,
    }

    # run validate # FIXME: what is this?
    run(config_train)


if __name__ == "__main__":
    # The circuit optimiation under test:
    from autockt_shared.opamp import circuit_optimization

    main(circuit_optimization=circuit_optimization)
