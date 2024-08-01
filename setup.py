from setuptools import setup, find_packages
import os

# Read the contents of your README file
from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

# Get version
version = {}
with open(os.path.join("repopack", "version.py")) as fp:
    exec(fp.read(), version)

setup(
    name="repopack",
    version=version['__version__'],
    author="Abin Thomas",
    author_email="abinthomasonline@gmail.com",
    description="A tool to pack repository contents into a single file for AI analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/abinthomasonline/repopack-py",
    packages=find_packages(),
    install_requires=[
        "chardet",
        "pathspec",
        "colorama",
        # Add any other dependencies your project needs
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "repopack=repopack.cli:run_cli",
        ],
    },
)