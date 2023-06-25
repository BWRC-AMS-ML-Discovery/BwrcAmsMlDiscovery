# PyPI imports
from ray import tune

# Local imports
from autockt.autockt_gym import AutoCktGym
from autockt.autockt_gym_env_config import AutoCktGymEnvConfig


class AutoCktTrainer:
    """
    The reason that this exists is because the interaction between ray and gym
    is unclear at the moment. Let's use Keerthana's code for now, until we
    figure out how to properly use ray and gym.
    """

    def train(gym_env_config: AutoCktGymEnvConfig):
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
            "num_workers": 1,
            "env_config": {  # a kwarg to the env constructor
                "generalize": True,
                "run_valid": False,
            },
            # "disable_env_checking": True,
        }

        config_experiment = {
            "env": AutoCktGym,
            "config": config_train,
            "run": "PPO",
            "checkpoint_freq": 1,
        }

        # Ray training starts
        ray.init()

        # Runs training and saves the result in ~/ray_results/train_ngspice_45nm
        # If checkpoint fails for any reason, training can be restored
        if not args.checkpoint_dir:
            tune.run_experiments(
                {
                    "train_45nm_ngspice": {
                        **config_experiment,
                        "stop": {"episode_reward_mean": -0.02},
                    }
                }
            )
        else:
            print("RESTORING NOW!!!!!!")
            tune.run_experiments(
                {
                    "restore_ppo": {
                        **config_experiment,
                        "restore": args.checkpoint_dir,
                    }
                }
            )
