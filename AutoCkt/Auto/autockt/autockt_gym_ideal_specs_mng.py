# Stdlib imports
from typing import Callable, Generic, TypeVar
from dataclasses import asdict
import random
import numpy as np

# PyPI imports
from pydantic.dataclasses import dataclass

# local imports
from .autockt_gym_env_config import (
    AutoCktSpec,
    AutoCktSpecs,
    AutoCktParam,
    AutoCktParams,
    Number,
)


# FIXME This lib was an adapter to use auto_ckt_sim for Keerthana's code
# We should use the auto_ckt_sim directly, since if you look into this lib,
# it's not generalizable
from .envs.create_design_and_simulate_lib import create_design_and_simulate


@dataclass
class SpecManager:
    """
    handles state management and generation of specs in RL model
    """

    # the inital specs used to create the spec manager
    init_spec: AutoCktSpecs

    # what spec is initially generated to
    ideal_spec: list[Number]
    # the current spec value
    cur_spec: list[Number]
    # ideal norm is calculate from ideal_spec and normalized values
    ideal_norm: list[Number]

    def __init__(self, init_spec):
        """
        generates initial variable
        """
        self.init_spec = init_spec

        self.ideal_spec = self.gen_spec()
        self.ideal_norm = self.normalize(self.ideal_spec)

        self.cur_spec = np.zeros(len(self.init_spec))

    def step(self):
        """
        Takes a dict of param values and updates the current spec values

        returns the current spec, ideal_spec, the norm of the current spec, and the norm of the ideal spec
        returns the current and ideal spec so that reward can be calculated
        """
        cur_norm = self.normalize(self.cur_spec)

        return [self.cur_spec, self.ideal_spec, cur_norm, self.ideal_norm]

    def reset(self):
        """
        Takes a dict of param values to reset the current spec value to
        generates a new set of ideal specs

        returns the normalied values of the current spec and the ideal spec
        """
        self.ideal_spec = self.gen_spec()
        self.ideal_norm = self.normalize(self.ideal_spec)

        cur_norm = self.normalize(self.cur_spec)

        return [cur_norm, self.ideal_norm]

    def update(self, simulated: dict[str, Number]) -> list[Number]:
        """
        simulates on the given param values and returns a spec dict
        """
        # print(f"{simulated}")
        self.cur_spec = list(simulated.values())

    def normalize(self, specs: dict[str, Number]) -> list[Number]:
        """
        given a dict of specs, calculate and return normalized spec value
        """
        relative = []

        for i in range(len(self.init_spec)):
            to_normalize = specs[i]
            spec = self.init_spec[i]
            rel = (to_normalize - spec.normalize) / (to_normalize + spec.normalize)
            relative.append(rel)

        # print(f"{relative}")
        # spec_norm = dict(zip(self.spec_id, relative))
        return relative

    def gen_spec(self):
        """
        using the given range from init_spec, randomly generate one set of specs which fits this range
        """
        spec_values = []
        for spec in self.init_spec:
            range = spec.range
            if isinstance(range.min, int):
                val = random.randint(int(range.min), int(range.max))
            else:
                val = random.uniform(float(range.min), float(range.max))
            spec_values.append(val)

        return spec_values
