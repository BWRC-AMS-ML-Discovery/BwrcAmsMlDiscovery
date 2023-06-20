from example_client import (
    test_auto_ckt,
    example_client_start
)


def main():
    example_client_start()
    
    reinforcement_learning_env = {"steps": 5, "update": None}

    for reinforcement_learning_step in range(
        reinforcement_learning_env["steps"],
    ):
        result = test_auto_ckt()

        print(f"{result=}")

        reinforcement_learning_env["update"] = result


if __name__ == "__main__":
    main()
