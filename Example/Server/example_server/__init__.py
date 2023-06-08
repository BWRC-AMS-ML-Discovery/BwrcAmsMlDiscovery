"""
# Example Server
"""


# Workspace Imports
from example_shared import (
    example,
    Example,
)


@example.impl
def example_func(example: Example) -> Example:
    """# Example RPC"""

    return Example(txt=example.txt * example.num, num=1)


