# Stdlib imports
from typing import Callable, Generic, TypeVar
from dataclasses import asdict
import random
import numpy as np

# PyPI imports
from pydantic.dataclasses import dataclass

# local imports
from autockt_gym_env_config import (
    AutoCktSpec,
    AutoCktSpecs,
    AutoCktParam,
    AutoCktParams,
    Number,
)
from envs.create_design_and_simulate_lib import create_design_and_simulate


#
@dataclass
class SpecManager:
    # the inital specs used to create the spec manager
    init_spec: AutoCktSpecs

    # list if ids the spec has
    spec_id: list(str)
    # what spec is initially generated to
    ideal_spec: dict[str:Number]
    # the current spec value
    cur_spec: dict[str:Number]
    # ideal norm is calculate from ideal_spec and normalized values
    ideal_norm: dict[str:Number]

    def __init__(self, init_spec):
        self.init_spec = init_spec

        self.spec_id = [spec.str for spec in init_spec]
        self.ideal_spec = self.gen_spec()
        self.ideal_norm = self.normalize(self.ideal_spec)
        self.cur_spec = np.zeroes(len(self.spec_id))

    def step(self, params):
        self.cur_spec = self.update(params)
        cur_norm = self.normalize(self.cur_spec)

        return [self.cur_spec, cur_norm, self.ideal_norm]

    def reset(self, params: dict[str:Number]):
        self.ideal_spec = self.gen_spec()
        self.ideal_norm = self.normalize(self.ideal_spec)

        self.cur_spec = self.update(params)
        cur_norm = self.normalize(self.cur_spec)

        return [cur_norm, self.ideal_norm]

    def update(self, params: dict[str:Number]):
        simulated = create_design_and_simulate(params)
        return simulated

    def normalize(self, spec):
        to_normalize = spec.values()
        normalize = [spec.normalize for spec in self.init_spec]

        relative = (to_normalize - normalize) / (to_normalize + normalize)

        spec_norm = dict(zip(self.spec_id, relative))
        return spec_norm

    def gen_spec(self):
        """
        using the given range, randomly generate one set of specs which fits this range
        """
        spec_values = []
        for spec in self.init_spec:
            range = spec.range
            if isinstance(range.min, int):
                val = random.randint(int(range.min), int(range.max))
            else:
                val = random.uniform(float(range.min), float(range.max))
            spec_values.append(val)

        cur_spec = dict(zip(self.spec_id, spec_values))
        return cur_spec
