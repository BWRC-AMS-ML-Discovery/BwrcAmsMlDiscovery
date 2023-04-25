import yaml


class Parameters:
    keys = ["generator_type", "circuit_type", "step_size"]

    def __init__(self, config_file_address):
        """
        Instantiate a Parameters object.

        :param config_file_address: the config file address
        :type config_file_address: str
        """

        with open(config_file_address, "r") as config_file:
            config = yaml.safe_load(config_file)

        self.parameters = config

    def get_parameter(self, parameter):
        return self.parameters.get(parameter)

    def get_hyperparameter(self, hyperparameter):
        return self.parameters.get("hyperparameters").get(hyperparameter)

    def set_parameter(self, parameter, value):
        self.parameters[parameter] = value

    def set_hyperparameter(self, hyperparameter, value):
        self.parameters.get("hyperparameters")[hyperparameter] = value

    def __str__(self):
        white = "\033[97m"
        green = ": \033[92m"
        string = (
            "Simulation ID #" + str(self.get_parameter("id")) + "\n\nParameters\n\n"
        )

        for key in Parameters.keys:
            string += (
                white + str(key.ljust(18)) + green + str(self.get_parameter(key)) + "\n"
            )

        string += "\033[97m\nHyperparameters\n\n"

        for hkey in self.get_parameter("hyperparameters").keys():
            string += (
                white
                + str(hkey.ljust(18))
                + green
                + str(self.get_hyperparameter(hkey))
                + "\n"
            )

        return string + white
