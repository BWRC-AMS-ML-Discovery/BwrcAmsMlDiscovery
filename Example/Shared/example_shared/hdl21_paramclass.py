import hdl21 as h


hdl21_paramclass = {}


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


def like_hdl21_paramclass(dataclass: type) -> type:
    """Convert a dataclass to an hdl21 Paramclass and register it"""

    hdl21_paramclass[dataclass] = dataclass_to_hdl21_paramclass(dataclass)

    return dataclass
