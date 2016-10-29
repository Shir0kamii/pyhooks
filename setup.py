"""
Pyhooks
"""

import os
import subprocess
import sys
from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


def get_version():
    if not os.path.isdir(".git"):
        sys.stderr.write("This does not appear to be a Git repository.")
        return ""
    return subprocess.check_output(["git", "describe", "--tags", "--always"],
                                   universal_newlines=True)[:-1]

setup(
    name="pyhooks",
    version=get_version(),
    author="Shir0kamii",
    author_email="shir0kamii@gmail.com",
    description="appnexus-client is a python wrapper for the Appnexus API",
    long_description=read("README.rst"),
    url="https://github.com/Shir0kamii/pyhooks",
    download_url="https://github.com/Shir0kamii/pyhooks/tags",
    platforms="any",
    packages=find_packages(),
    classifiers=[
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Topic :: Software Development :: Libraries :: Python Modules"
    ]
)
