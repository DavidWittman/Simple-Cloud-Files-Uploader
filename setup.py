#!/usr/bin/env python

from setuptools import setup

VERSION = "0.3"
REQS = ['python-cloudfiles']

setup(
    name = 'cfupload',
    description = 'A very simple Rackspace Cloud Files uploader',
    version = VERSION,
    author = 'David Wittman',
    author_email = 'david@wittman.com',
    license = 'BSD',
    install_requires = REQS,
    scripts = ['cfupload.py']
)
