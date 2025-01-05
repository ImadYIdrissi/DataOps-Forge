"""Installation util for engine package."""

import os
from setuptools import setup, find_packages

base_dir = os.path.abspath(os.path.dirname(__file__))


def parse_requirements(file) -> list:
    """Read requirements.txt.

    Args:
        file (str): Path of the file to parse.
    Returns:
        list: Parsed requirements.
    """
    print(f"Looking for requirements at: {os.path.join(base_dir, 'requirements.txt')}")

    with open(file, "r") as f:
        return [line.strip() for line in f if line and not line.startswith("#")]


setup(
    name="engine",
    version="0.1.0",
    packages=find_packages(),
    install_requires=parse_requirements("requirements.txt"),
)
