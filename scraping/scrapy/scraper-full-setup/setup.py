#!/usr/bin/env python
# ==============================================================================

from setuptools import setup, find_packages

setup(
    name='webscraperapp',
    packages=find_packages(),
    entry_points={
        'scrapy': ['settings = webscraperapp.settings']
    },
)
