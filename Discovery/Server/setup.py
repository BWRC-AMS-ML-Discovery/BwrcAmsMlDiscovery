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
    name="cktgym_discovery_server",
    version="0.0.4",
    description="BWRC AMS ML Discovery Server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BWRC-AMS-ML-Discovery",
    author="The Regents of the University of California",
    author_email="haohanw@eecs.berkeley.edu",
    packages=find_packages(),
    python_requires=">=3.7, <3.11",
    install_requires=[
        "python-dotenv~=1.0",
        "fastapi~=0.99.1",
        "GitPython>=3.1.31",
        "uvicorn>=0.20.0",
        "firebase_admin>=6.0.1",
        "cktgym_discovery_shared",
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
