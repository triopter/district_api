#!/usr/bin/env python

import os
import sys
import my_package 

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

requires = ["requests >= 1.0.0"]

setup(
    name='districts',
    version = districts.__version__,
    description='Python Client for NY Times Districts API',
    long_description=open('README.rst').read(),
    author='Noemi Millman',
    author_email='noemi@triopter.com',
    url='http://proj.example.com/',
    packages=['districts'],
    install_requires=requires,
    license=open('LICENSE').read(),
    zip_safe=False,
    entry_points = {},
    classifiers = [
        'License :: OSI Approved :: GNU Lesser General Public License v2 or later (LGPLv2+)',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ],
)
