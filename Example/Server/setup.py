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
    name="example_server",
    version="0.0.1",
    description="Example Discovery Server",
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
        "discovery_server==0.0.1",
        "scipy",
        "example_shared==0.0.1",
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
