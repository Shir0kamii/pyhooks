"""
Pyhooks
"""

import os
from setuptools import find_packages, setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name="pyhooks",
    version="1.0.1",
    author="Shir0kamii",
    author_email="shir0kamii@gmail.com",
    description="Python hooks for methods",
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
