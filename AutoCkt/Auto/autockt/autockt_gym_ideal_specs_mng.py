# Stdlib imports
from typing import Callable, Generic, TypeVar
from dataclasses import asdict
import random
import numpy as np
import pickle
from collections import OrderedDict


# PyPI imports
from pydantic.dataclasses import dataclass

# local imports
from autockt_shared.cktopt import (
    AutoCktSpec,
    AutoCktSpecs,
    AutoCktParam,
    AutoCktParams,
    Number,
)


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

    ideal_specs: list[dict[str, Number]]

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

        self.global_norm = {}
        for spec in init_spec:
            self.global_norm[spec.name] = spec.normalize

        self.num_specs = 350

        self.ideal_specs = []
        for i in range(self.num_specs):
            self.ideal_specs.append(self.gen_spec())

        zeros = np.zeros(len(self.spec_id))
        self.cur_spec = dict(zip(self.spec_id, zeros))

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
        idx = random.randint(0, self.num_specs - 1)
        self.ideal_spec = self.ideal_specs[idx]

        self.ideal_norm = self.normalize(self.ideal_spec)

        cur_norm = self.normalize(self.cur_spec)

        return [cur_norm, self.ideal_norm]

    def update(self, simulated: dict[str, Number]) -> dict[str, Number]:
        """
        simulates on the given param values and returns a spec dict
        """

        self.cur_spec = simulated

    def normalize(self, specs: dict[str, Number]) -> dict[str, Number]:
        """
        given a dict of specs, calculate and return normalized spec value
        """
        relative = {}

        for spec in self.init_spec:
            to_normalize = float(specs[spec.name])
            rel = (to_normalize - spec.normalize) / (to_normalize + spec.normalize)
            relative[spec.name] = rel

        return relative

    def gen_spec(self):
        """
        using the given range from init_spec, randomly generate one set of specs which fits this range
        """
        spec_values = []
        for spec in self.init_spec:
            range = spec.range
            # print(spec)
            if isinstance(range.min, int):
                val = random.randint(int(range.min), int(range.max))
            else:
                val = random.uniform(float(range.min), float(range.max))
            spec_values.append(val)

        cur_spec = dict(zip(self.spec_id, spec_values))

        return cur_spec

    def get_global_norm(self):
        return self.global_norm

    def get_specs(self):
        return self.ideal_specs
