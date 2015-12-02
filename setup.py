#!/usr/bin/env python

from setuptools import setup, find_packages

__version__ = "1.1"

setup(
    name="influxdbnagiosplugin",
    version=__version__,
    description="InfluxDB Nagios Plugin",
    author="Location Labs",
    author_email="info@locationlabs.com",
    url="http://locationlabs.com",
    packages=find_packages(exclude=["*.tests"]),
    setup_requires=[
        "nose>=1.3.7"
    ],
    install_requires=[
        "influxdb>=2.10.0",
        "nagiosplugin>=1.2.3",
    ],
    tests_require=[
        "PyHamcrest>=1.8.5",
        "mock>=1.0.1",
        "coverage>=4.0.1",
    ],
    test_suite="influxdbnagiosplugin.tests",
    entry_points={
        "console_scripts": [
            "check-measurement = influxdbnagiosplugin.main:main",
        ]
    }
)
