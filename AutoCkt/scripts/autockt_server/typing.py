from dataclasses import asdict

import hdl21 as h


def dataclass_to_hdl21_paramclass(dataclass: type) -> h.Type:
    """Convert a dataclass to an hdl21 Paramclass"""

    attributes = {
        field_name: h.Param(
            dtype=field.type,
            desc=field.default.description,
            default=field.default.default,
        )
        for field_name, field in dataclass.__dataclass_fields__.items()
    }

    return h.paramclass(
        type(
            dataclass.__name__,
            (),
            attributes,
        )
    )


hdl21_paramclass = {}


def Hdl21Paramclass(dataclass: type) -> type:
    """Convert a dataclass to an hdl21 Paramclass and register it"""

    if dataclass not in hdl21_paramclass:
        hdl21_paramclass[dataclass] = dataclass_to_hdl21_paramclass(dataclass)

    return hdl21_paramclass[dataclass]


def _like_hdl21_paramclass(dataclass: type) -> type:
    """Convert a dataclass to an hdl21 Paramclass and register it"""

    hdl21_paramclass[dataclass] = dataclass_to_hdl21_paramclass(dataclass)

    return dataclass


def as_hdl21_paramclass(data):
    """
    Convert a dataclass to a Hdl21 parameter class
    """
    return Hdl21Paramclass(type(data))(
        **asdict(data),
    )
