#!/usr/bin/env python

from setuptools import setup, find_packages

setup(
    name='webscraperapp',
    version='1.0.2',
    packages=find_packages(),
    entry_points={
        'scrapy': ['settings = webscraperapp.settings']
    },
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
)
