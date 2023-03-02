"""
# Discovery 
Shared server-client code
"""

# Std-Lib Imports
import functools
from typing import Optional, List, Any
from dataclasses import asdict

# PyPi Imports
import pydantic


def dataclass(*args, **kwargs):
    """# The dataclasses workaround from
    https://github.com/tiangolo/fastapi/issues/265#issuecomment-557849193"""

    class ORMConfig:
        orm_mode = True
        arbitrary_types_allowed = True

    return pydantic.dataclasses.dataclass(config=ORMConfig)(*args, **kwargs)


functools.update_wrapper(wrapper=dataclass, wrapped=pydantic.dataclasses.dataclass)


@dataclass
class Example:
    """# Example of a dataclass that can be used as a POST body"""

    txt: str
    num: int


__all__ = ["Example"]
