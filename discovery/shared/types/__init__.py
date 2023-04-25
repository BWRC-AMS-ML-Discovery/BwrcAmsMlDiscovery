from .. import user, mock


path_to_inp_types = {
    "/whoami": None,
    "/mock/inverter_beta_ratio": mock.MockInverterBetaRatioInput,
}

path_to_out_types = {
    "/whoami": user.WhoAmIOutput,
    "/mock/inverter_beta_ratio": mock.MockInverterBetaRatioOutput,
}


# input
def convert_inp_json_to_type(type, inp):
    if type is None:
        return None

    if isinstance(inp, dict):
        return type(**inp)

    # Currently unsupported
    raise NotImplementedError


# output
def convert_out_json_to_type(type, out):
    if type is None:
        return None

    if isinstance(out, dict):
        return type(**out)

    # Currently unsupported
    raise NotImplementedError
