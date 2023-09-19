from autockt_shared import OpAmpInput, OpAmpOutput
from autockt_shared import auto_ckt_sim  ##FIXME


def ordered_dict_to_input(param_val):
    return OpAmpInput(
        mp1=param_val["mp1"],
        mn1=param_val["mn1"],
        mp3=param_val["mp3"],
        mn3=param_val["mn3"],
        mn4=param_val["mn4"],
        mn5=param_val["mn5"],
        cc=param_val["cc"],
    )


def output_to_dict(out: OpAmpOutput) -> dict:
    return {
        "ugbw": out.ugbw,
        "gain": out.gain,
        "phm": out.phm,
        "ibias": out.ibias,
    }


def create_design_and_simulate(param_val) -> dict:
    inp: OpAmpInput = ordered_dict_to_input(param_val)
    out: OpAmpOutput = auto_ckt_sim(inp)
    result: dict = output_to_dict(out)
    return result
