#!/usr/bin/env python3
"""
Setup script for PyWall.
Installs the application and dependencies.
"""

import sys
from setuptools import setup, find_packages

# Check Python version
if sys.version_info < (3, 6):
    print("PyWall requires Python 3.6 or later")
    sys.exit(1)

# Read requirements
with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

setup(
    name="PyWall",
    version="1.8",
    description="A simple firewall management tool for Windows",
    author="PyWall Team",
    packages=find_packages(),
    install_requires=requirements,
    entry_points={
        'console_scripts': [
            'pywall=main:main',
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.6",
)

