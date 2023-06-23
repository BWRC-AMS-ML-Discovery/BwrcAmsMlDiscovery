from example_shared import AutoCktInput, AutoCktOutput
from example_client import auto_ckt_sim, reward


def ordered_dict_to_input(param_val):
    return AutoCktInput(
        mp1=param_val["mp1"],
        mn1=param_val["mn1"],
        mp3=param_val["mp3"],
        mn3=param_val["mn3"],
        mn4=param_val["mn4"],
        mn5=param_val["mn5"],
        cc=param_val["cc"],
    )


def output_to_dict(out: AutoCktOutput) -> dict:
    return {
        "ugbw": out.ugbw,
        "gain": out.gain,
        "phm": out.phm,
        "ibias": out.ibias,
    }


def create_design_and_simulate(param_val) -> dict:
    inp: AutoCktInput = ordered_dict_to_input(param_val)
    out: AutoCktOutput = auto_ckt_sim(inp)
    result: dict = output_to_dict(out)
    return result

