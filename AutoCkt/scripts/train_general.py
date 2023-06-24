from autockt import AutoCktTrainer

from shared.autockt_gym_env_config import (
    AutoCktCircuitOptimization,
    AutoCktGymEnvConfig,
    AutoCktParams,
    AutoCktParam,
    AutoCktSpecs,
    AutoCktSpec,
)


def main():
    circuit_optimization = AutoCktCircuitOptimization(
        params=AutoCktParams(
            [
                AutoCktParam("mp1", (1, 100), 1),
                AutoCktParam("mn1", (1, 100), 1),
                AutoCktParam("mp3", (1, 100), 1),
                AutoCktParam("mn3", (1, 100), 1),
                AutoCktParam("mn4", (1, 100), 1),
                AutoCktParam("mn5", (1, 100), 1),
                AutoCktParam("cc", (0.1e-12, 10.0e-12), 0.1e-12),
            ]
        ),
        specs=AutoCktSpecs(  # FIXME Numbers ain't right
            [
                AutoCktSpec("gain", 200, 400, 350),
                AutoCktSpec("ibias", 1.0e6, 2.5e7, 1.0e7),
                AutoCktSpec("phm", 60, 60.0000001, 60),
                AutoCktSpec("ugbw", 0.0001, 0.01, 950000.0),
            ]
        ),
    )

    gym_env_config = AutoCktGymEnvConfig(
        circuit_optimization=circuit_optimization,
    )

    trainer = AutoCktTrainer()

    agent = trainer.train(gym_env_config)

    agent.save()


if __name__ == "__main__":
    main()
