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
    name="cktgym_sample_client",
    version="0.0.1",
    description="Sample Discovery Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="FIXME",
    author="The Regents of the University of California",
    author_email="haohanw@eecs.berkeley.edu",
    packages=find_packages(),
    python_requires=">=3.7, <4",
    install_requires=[
        "hdl21>=4.0.0",
        "python-dotenv==1.0.0",
        "cktgym_discovery_client",
        "cktgym_sample_shared",
    ],
    extras_require={
        "dev": [
            "pytest==7.1",
            "coverage",
            "pytest-cov",
            "pre-commit==2.20",
            "black==22.6",
            "twine",
        ]
    },
)
