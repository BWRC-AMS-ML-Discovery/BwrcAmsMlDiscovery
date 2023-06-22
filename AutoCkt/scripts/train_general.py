from autockt import AutoCktTrainer, derive_action_space

# eval_engines will be renamed to something like
from eval_engines import (
    ExampleOpAmpParams,
    ExampleOpAmpSpecs,
    # ExampleOpAmpActionSpace, # Suppose we want to derive this
    ExampleOpAmpObservationSpace,
    ExampleOpAmpReward,
)


def main():
    # Create the trainer
    trainer = AutoCktTrainer()

    # Train the model
    agent = trainer.train(
        params=ExampleOpAmpParams,
        specs=ExampleOpAmpSpecs,
        action_space=derive_action_space(ExampleOpAmpParams),  # Derive the action space
        observation_space=ExampleOpAmpObservationSpace,
        reward=ExampleOpAmpReward,
    )

    # Save the model
    agent.save()


if __name__ == "__main__":
    main()
