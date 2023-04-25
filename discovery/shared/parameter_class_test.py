from Parameters.parameters import Parameters

test_parameters_object = Parameters("test.yaml")

print(test_parameters_object)

test_parameters_object.set_parameter("generator_type", "BAG")
print("New generator type:", test_parameters_object.get_parameter("generator_type"))

test_parameters_object.set_hyperparameter("discount_factor", 0.25)
print("New discount factor:", test_parameters_object.get_hyperparameter("discount_factor"))

print(test_parameters_object)
