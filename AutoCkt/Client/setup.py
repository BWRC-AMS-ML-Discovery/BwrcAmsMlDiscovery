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
    name="autockt_client",
    version="0.0.1",
    description="BWRC AMS ML Discovery AutoCkt - Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="FIXME",
    author="The Regents of the University of California",
    author_email="FIXME",
    packages=find_packages(),
    python_requires=">=3.7, <4",  ## FIXME: require 3.7, maybe more, after dependencies upgrades
    install_requires=[  ##
        # Local "workspace" dependencies
        "autockt_shared",
        "discovery_client",
    ],
    extras_require={"dev": ["cktgym_discovery_dev"]},
)
