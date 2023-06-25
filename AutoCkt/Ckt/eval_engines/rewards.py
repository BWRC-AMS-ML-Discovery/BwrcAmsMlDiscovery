from example_client import AutoCktOutput
from shared.typing import Number


def settaluri_reward(curr_specs: AutoCktOutput, ideal_specs: dict[str, Number]):
    """
    Reward: doesn't penalize for overshooting spec, is negative
    """

    def calc_relative_spec(spec: float, ideal_spec: float):
        ideal_spec = float(ideal_spec)  # Not sure if this is necessary
        relative_spec = (spec - ideal_spec) / (ideal_spec + spec)
        return relative_spec

    # FIXME
    raise NotImplementedError
