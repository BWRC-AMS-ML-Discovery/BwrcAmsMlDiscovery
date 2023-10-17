# PyPI imports
from ray import tune

# Local imports
from autockt.autockt_gym import AutoCktGym
from autockt_shared.cktopt import AutoCktGymEnvConfig


def autockt_train(
    experiment_name: str,
    gym_env_config: AutoCktGymEnvConfig,
    num_workers: int,
):
    """
    The reason that this exists is because the interaction between ray and gym
    is unclear at the moment. Let's use Keerthana's code for now, until we
    figure out how to properly use ray and gym.
    """

    # configures training of the agent with associated hyperparameters
    # See Ray documentation for details on each parameter
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

    config_experiment = {
        "env": AutoCktGym,
        "config": config_train,
        "run": "PPO",
        "checkpoint_freq": 1,
        "stop": {"episodes_total": 1},  # FIXME Sometimes we will never reach this
    }

    tune.run_experiments(
        {experiment_name: config_experiment},
    )
