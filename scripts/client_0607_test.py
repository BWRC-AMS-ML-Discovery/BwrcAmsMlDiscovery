from example_client import test_auto_ckt


def main():
    reinforcement_learning_env = {"steps": 5, "update": None}

    for reinforcement_learning_step in range(
        reinforcement_learning_env["steps"],
    ):
        result = test_auto_ckt()

        print(f"{result=}")

        reinforcement_learning_env["update"] = result


if __name__ == "__main__":
    main()
