from dataclasses import asdict

from autockt_shared.cktopt import (
    MetricSpec,
    MetricSpecs,
    ParamSpec,
    ParamSpecs,
)


def as_param_specs(dataclass_type):
    """
    Convert a dataclass to a ParamSpecs
    """
    return ParamSpecs(
        [
            ParamSpec(
                name=field.name,
                range=(field.default.ge, field.default.le),
                step=field.default.extra["step"],
                init=field.default.default,
            )
            for field in dataclass_type.__dataclass_fields__.values()
        ]
    )


def as_target_specs(dataclass_type):
    """
    Convert a dataclass to a MetricSpecs
    """
    return MetricSpecs(
        [
            MetricSpec(
                name=field.name,
                range=(field.default.ge, field.default.le),
                normalize=field.default.extra["normalize"],
            )
            for field in dataclass_type.__dataclass_fields__.values()
        ]
    )
