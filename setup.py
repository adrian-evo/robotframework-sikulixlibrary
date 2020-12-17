# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages  # type: ignore
import sys

# get __version__ number
exec(compile(open('SikuliXLibrary/version.py', "rb").read(), 'SikuliXLibrary/version.py', 'exec'))

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

install_requires = open(os.path.join("SikuliXLibrary", "requirements.txt")).readlines()

setup_kwargs = {
    "name": "robotframework-sikulixlibrary",
    "version": __version__,
    "description": "Robot Framework SiluliX library powered by SikuliX Java library and JPype Python module.",
    "long_description": long_description,
    "long_description_content_type": "text/markdown",
    "author": "Adrian V.",
    "author_email": "avaidos@gmail.com",
    "maintainer": None,
    "maintainer_email": None,
    "url": "https://github.com/adrian-evo/robotframework-sikulixlibrary",
    "packages": find_packages(exclude=["test"]),
    "include_package_data" : True,
    "install_requires": install_requires,
    "python_requires": ">=3.7,<4.0",
    "classifiers": [
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Topic :: Software Development :: Testing",
        "Framework :: Robot Framework",
        "Framework :: Robot Framework :: Library",
    ],
}

setup(**setup_kwargs)
