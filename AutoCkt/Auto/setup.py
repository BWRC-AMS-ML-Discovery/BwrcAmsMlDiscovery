"""
# Setup Script

Derived from the setuptools sample project at
https://github.com/pypa/sampleproject/blob/main/setup.py

"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()
readme = here / "readme.md"
long_description = "" if not readme.exists() else readme.read_text(encoding="utf-8")


setup(
    name="autockt",
    version="0.0.1",
    description="BWRC AMS ML Discovery AutoCkt - ML",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="FIXME",
    author="The Regents of the University of California",
    author_email="FIXME",
    packages=find_packages(),
    python_requires=">=3.7, <4",  ## FIXME: require 3.7, maybe more, after dependencies upgrades
    install_requires=[  ##
        ## FIXME: can we ease up on the version requirements?
        ## Maybe, but it's nice for intra-workspace consistency.
        "numpy==1.21.5",
        "scipy==1.10.1",
        "gym==0.23.1",  # Core ML dependency: OpenAI Gym
        "ray[rllib,tune]==2.0.0",  # Ray for RL, parallelization, training
        "tensorflow==2.8.0",  # "ray" needs these
        "protobuf==3.19.1",  # "ray" needs these
        "pyyaml==5.1.2",
        "pydantic==1.10.11",
        "autockt_shared",  # Local "workspace" dependency
        "example_shared",  # Local "workspace" dependency
        "example_client",  # Local "workspace" dependency
    ],
    extras_require={
        "dev": [
            "ipython==6.5.0",
            # "pytest==7.1",
            # "coverage",
            # "pytest-cov",
            # "pre-commit==2.20",
            # "black==22.6",
            # "twine",
        ]
    },
)
