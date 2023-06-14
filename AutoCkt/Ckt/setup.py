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
    name="eval_engines",
    version="0.0.1",
    description="BWRC AMS ML Discovery AutoCkt - Circuits",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="FIXME",
    author="The Regents of the University of California",
    author_email="FIXME",
    packages=find_packages(),
    python_requires=">=3.10", ## FIXME: require 3.7, maybe more, after dependencies upgrades
    install_requires=[  ##
        ## FIXME: can we ease up on the version requirements?
        "numpy==1.21.5",
        "scipy==1.10.1",
        "pyyaml==5.1.2",
        # "autockt_shared",  # Local "workspace" dependency
    ],
    # extras_require={
    #     "dev": [
    #         "pytest==7.1",
    #         "coverage",
    #         "pytest-cov",
    #         "pre-commit==2.20",
    #         "black==22.6",
    #         "twine",
    #     ]
    # },
)
