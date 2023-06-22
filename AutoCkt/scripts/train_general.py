from autockt import AutoCktTrainer
from eval_engines import ExampleOpAmpEvalEngine


def main():
    # Create the evaluation engine
    eval_engine = ExampleOpAmpEvalEngine()

    # Create the trainer
    trainer = AutoCktTrainer(eval_engine)

    # Train the model
    agent = trainer.train()

    # Save the model
    agent.save()


if __name__ == "__main__":
    main()
