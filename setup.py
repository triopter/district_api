#!/usr/bin/env python

import os
import sys
import district_api

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requires = ["requests >= 2.0.0"]

setup(
    name='district_api',
    version = district_api.__version__,
    description='Python Client for NY Times Districts API',
    long_description=open('README.rst').read(),
    author='Noemi Millman',
    author_email='noemi@triopter.com',
    url='http://proj.example.com/',
    packages=['district_api'],
    install_requires=requires,
    license=open('LICENSE.TXT').read(),
    zip_safe=False,
    entry_points = {},
    classifiers = [
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ],
)
