from os import path


from .parameters import Parameters


def test():
    # Get the path to this file
    file_path = path.dirname(path.abspath(__file__))
    # Get the path to the yaml file
    yaml_path = path.join(file_path, "parameters_test.yaml")

    test_parameters_object = Parameters(yaml_path)

    print(test_parameters_object)

    test_parameters_object.set_parameter("generator_type", "BAG")
    print(
        "New generator type:",
        test_parameters_object.get_parameter("generator_type"),
    )

    test_parameters_object.set_hyperparameter("discount_factor", 0.25)
    print(
        "New discount factor:",
        test_parameters_object.get_hyperparameter("discount_factor"),
    )

    print(test_parameters_object)
