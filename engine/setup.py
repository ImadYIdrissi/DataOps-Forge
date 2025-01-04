from setuptools import setup, find_packages


# Read requirements.txt
def parse_requirements(file):
    with open(file, "r") as f:
        return [line.strip() for line in f if line and not line.startswith("#")]


setup(
    name="engine",
    version="0.1.0",
    packages=find_packages(),
    install_requires=parse_requirements("../requirements.txt"),  # Adjust relative path as needed
)
