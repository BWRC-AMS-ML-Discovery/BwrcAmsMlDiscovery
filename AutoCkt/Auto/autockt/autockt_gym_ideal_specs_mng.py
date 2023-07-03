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

    # list if ids the spec has
    spec_id: list[str]
    # what spec is initially generated to
    ideal_spec: dict[str, Number]
    # the current spec value
    cur_spec: dict[str, Number]
    # ideal norm is calculate from ideal_spec and normalized values
    ideal_norm: dict[str, Number]

    def __init__(self, init_spec):
        """
        generates initial variable
        """
        self.init_spec = init_spec

        self.spec_id = [spec.name for spec in init_spec]
        self.ideal_spec = self.gen_spec()
        self.ideal_norm = self.normalize(self.ideal_spec)

        zeros = np.zeros(len(self.spec_id))
        self.cur_spec = dict(zip(self.spec_id, zeros))

        print(f"spec id: {self.spec_id}")
        print(f"ideal spec: {self.ideal_spec}")
        print(f"ideal norm: {self.ideal_norm}")
        print(f"cur spec: {self.cur_spec}")

    def step(self, params: dict[str, Number]):
        """
        Takes a dict of param values and updates the current spec values

        returns the current spec, ideal_spec, the norm of the current spec, and the norm of the ideal spec
        returns the current and ideal spec so that reward can be calculated
        """
        self.cur_spec = self.update(params)
        cur_norm = self.normalize(self.cur_spec)

        return [self.cur_spec, self.ideal_spec, cur_norm, self.ideal_norm]

    def reset(self, params: dict[str, Number]):
        """
        Takes a dict of param values to reset the current spec value to
        generates a new set of ideal specs

        returns the normalied values of the current spec and the ideal spec
        """
        self.ideal_spec = self.gen_spec()
        self.ideal_norm = self.normalize(self.ideal_spec)

        self.cur_spec = self.update(params)
        cur_norm = self.normalize(self.cur_spec)

        return [cur_norm, self.ideal_norm]

    def update(self, params: dict[str, Number]) -> dict[str, Number]:
        """
        simulates on the given param values and returns a spec dict
        """
        simulated = create_design_and_simulate(params)
        return simulated

    def normalize(self, specs: dict[str, Number]) -> dict[str, Number]:
        """
        given a dict of specs, calculate and return normalized spec value
        """
        relative = []

        for spec in self.init_spec:
            to_normalize = specs[spec.name]
            rel = (to_normalize - spec.normalize) / (to_normalize + spec.normalize)
            relative.append(rel)

        spec_norm = dict(zip(self.spec_id, relative))
        return spec_norm

    def gen_spec(self):
        """
        using the given range from init_spec, randomly generate one set of specs which fits this range
        """
        spec_values = []
        for spec in self.init_spec:
            range = spec.range
            print(spec)
            print(type(range.min))
            if isinstance(range.min, int):
                val = random.randint(int(range.min), int(range.max))
            else:
                val = random.uniform(float(range.min), float(range.max))
            spec_values.append(val)

        cur_spec = dict(zip(self.spec_id, spec_values))
        return cur_spec


# for testing
# specs = AutoCktSpecs(  # FIXME Numbers right?
#     [
#         AutoCktSpec("gain", (200, 400), normalize=350),
#         AutoCktSpec("ugbw", (1.0e6, 2.5e7), normalize=9.5e5),
#         AutoCktSpec("phm", (60, 60.0000001), normalize=60),
#         AutoCktSpec("ibias", (0.0001, 0.01), normalize=0.001),
#     ]
# )
# sm = SpecManager(specs)

# param_vals = {'mp1':34, 'mn1':34, 'mp3':34, 'mn3':34, 'mn4':34, 'mn5':15, 'cc':2.1e-12}
# norm, ideal_norm = sm.step(param_vals)
# print(f"val norm: {norm}")
# print(f"ideal norm: {ideal_norm}")
