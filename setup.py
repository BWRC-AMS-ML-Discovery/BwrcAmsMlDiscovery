"""
# Setup Script

Derived from the setuptools sample project at
https://github.com/pypa/sampleproject/blob/main/setup.py

"""

# Always prefer setuptools over distutils
from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "readme.md").read_text(encoding="utf-8")

setup(
    name="discovery",
    version="0.0.1",
    description="BWRC AMS ML Discovery",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="FIXME",
    author="The Regents of the University of California",
    author_email="FIXME",
    packages=find_packages(),
    python_requires=">=3.7, <4",
    install_requires=[
        "hdl21>=3.0.1",
        "python-dotenv==1.0.0",
        "fastapi>=0.92.0",
        "httpx>=0.23.3",
        "GitPython>=3.1.31",
        "uvicorn>=0.20.0",
        "firebase_admin>=6.1.0",
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
