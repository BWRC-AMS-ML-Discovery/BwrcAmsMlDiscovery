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
    name="cktgym_discovery_dev",
    version="0.0.4",
    description="BWRC AMS ML Discovery - Dev Packages",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BWRC-AMS-ML-Discovery",
    author="The Regents of the University of California",
    author_email="haohanw@eecs.berkeley.edu",
    packages=find_packages(),
    python_requires=">=3.7, <3.11",
    install_requires=[
        "ipython==6.5.0",
        "pytest==7.1",
        "coverage",
        "pytest-cov",
        "pre-commit==2.20",
        "black==22.6",
        "twine",
    ],
)
