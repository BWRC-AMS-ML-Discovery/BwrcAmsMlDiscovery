"""
# Git Version Info
## On the current in-memory repository
"""

# Std-Lib Imports
from copy import copy
from typing import List

# PyPi Imports
import git

# Local Imports
from .dataclasses import dataclass


@dataclass
class GitInfo:
    """# Git info for a repository"""

    sha: str  # The SHA of the commit
    tags: List[str]  # List of tags on the commit
    is_dirty: bool = False  # Whether the repo is dirty

    @staticmethod
    def get() -> "GitInfo":
        return copy(gi)


"""
# Non-docstring comment:
# 
# Note the GitPython library includes some admonitions to *not* use it in a long-running process, 
# (kinda like our web server!). This is largely about resource management and clean-up. 
# We only monitor one repo - the one containing this file. 
# So, load it up at import time, and then just copy the `GitInfo` object for the rest of the process.
"""

repo = git.Repo()
gi = GitInfo(
    sha=repo.head.object.hexsha,
    tags=[tag.name for tag in repo.tags if tag.commit == repo.head.commit],
    is_dirty=repo.is_dirty(),
)

__all__ = ["GitInfo"]
