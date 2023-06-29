import json
import datetime
import os


class Results:
    def __init__(self, simulation_id, objective_function_value, parameters):

        self.id = simulation_id
        self.value = objective_function_value
        self.parameters = parameters

    def set_value(self, value):
        self.value = value

    def set_parameters(self, parameters):
        self.parameters = parameters

    def get_id(self):
        return self.id

    def get_value(self):
        return self.value

    def get_parameters(self):
        return self.parameters

    def dump(self):
        timestamp = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        file_name = "results/" + str(self.id) + "_" + timestamp + ".json"
        data = self.parameters
        data["id"] = self.id
        data["value"] = self.value

        if not os.path.exists("results"):
            os.makedirs("results")

        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)

    def __str__(self):
        white = "\033[97m"
        green = ": \033[92m"
        string = (
            "Simulation ID: "
            + str(self.id)
            + "\nObjective function value: "
            + str(self.value)
            + "\nOptimal parameters:\n\n"
        )

        for key in self.parameters.keys():
            string += (
                white
                + str(key.ljust(10))
                + green
                + str(self.parameters.get(key))
                + "\n"
            )

        return string + white
