"""
# Dataclass Wrapper 
"""

# Std-Lib Imports
from functools import update_wrapper

# PyPi Imports
import pydantic


def dataclass(*args, **kwargs):
    """# The dataclasses workaround from
    https://github.com/tiangolo/fastapi/issues/265#issuecomment-557849193"""

    class ORMConfig:
        orm_mode = True
        arbitrary_types_allowed = True

    return pydantic.dataclasses.dataclass(config=ORMConfig)(*args, **kwargs)


update_wrapper(wrapper=dataclass, wrapped=pydantic.dataclasses.dataclass)
