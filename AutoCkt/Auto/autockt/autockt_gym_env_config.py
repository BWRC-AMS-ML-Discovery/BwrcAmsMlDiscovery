# Stdlib imports
import dataclasses
from dataclasses import asdict
from typing import Callable, List, Optional

# PyPI imports
from pydantic.dataclasses import dataclass

# Local imports
from shared.typing import Number
from discovery_shared.rpc import Rpc


@dataclass
class Range:
    min: Number
    max: Number


@dataclass
class ParamSpec:
    name: str  # Parameter name
    range: Range  # Min and max
    step: Number  # Allowed step size
    init: Number  # Initial / default value
    desc: str  # Description


@dataclass
class ParamSpecs:
    something: list[ParamSpec]
    # FIXME: make the value types here!


@dataclass
class MetricSpec:
    name: str
    range: Range
    normalize: Number


@dataclass
class MetricSpecs:
    something: list[MetricSpec]
    # FIXME: make the value types here!


@dataclass
class CircuitOptimization:
    params: ParamSpecs
    metrics: MetricSpecs

    reward: Callable[
        ["Self.OutputType", dict[str, Number]],  # TODO Typing
        # TODO The input to reward can be expanded to (s_t, a_t, s_{t+1}),
        # as defined in OpenAI's Spinning Up intro to RL:
        # https://spinningup.openai.com/en/latest/spinningup/rl_intro.html#reward-and-return
        float,
    ]

    # rpc function which simulates
    simulation: Rpc

    input_type: Optional[type] = None
    output_type: Optional[type] = None

    def __post_init_post_parse__(self):
        if self.input_type is None:
            self.input_type = something("ParamValues", self.params)
        if self.output_type is None:
            raise TabError(f"FIXME: YOU GUYS MAKE THIS FOR METRICS")


@dataclass
class AutoCktGymEnvConfig:
    circuit_optimization: CircuitOptimization
    actions_per_param: list[
        int  # TODO Here, int is number of steps. Can be more general.
    ]

    def __iter__(self):
        """
        FIXME Needs to be iterable, required by ray
        """
        yield from asdict(self).items()


def something(name: str, params: List[ParamSpec]) -> type:
    """Create the parameter value-type from a list of `ParamSpec`s

    From something like

    ```python
    [
        ParamSpec("mp1", (1, 100), step=1, init=34, desc="MP1 Multiplier"),
        ParamSpec("mn1", (1, 100), step=1, init=34, desc="MN1 Multiplier"),
        ParamSpec("cc", (0.1e-12, 10.0e-12), step=0.1e-12, init=2.1e-12, desc="Compensation Capacitance"),
    ]
    ```

    Produce something like

    ```python
    @dataclass
    class ParamValues:
        mp1: Number = field(default=34)
        mn1: Number = field(default=34)
        cc: Number = field(default=2.1e-12)
    ```
    """

    cls = type(name, (), {})

    for param in params:
        # What to do with range and step? Meh we'll see
        field = dataclasses.field(default=param.init)
        setattr(cls, param.name, field)

    # FIXME: also make the hdl21.paramclass edition, something like
    """
    ```python
    @h.paramclass 
    class Hdl21Params:
        mp1 = h.Param(dtype=Number, desc="MP1 Multiplier", "default=34)
        mn1 = h.Param(dtype=Number, desc="MN1 Multiplier", "default=34)
        cc = h.Param(dtype=Number, desc="Compensation Capacitance", "default=2.1e-12)

    hp = Hdl21Params(**asdict(ParamValues()))
    ```
    """
    return cls
