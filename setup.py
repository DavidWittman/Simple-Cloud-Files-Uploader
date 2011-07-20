#!/usr/bin/env python

from setuptools import setup

reqs = [ 'python-cloudfiles' ]

setup(  name = 'cfupload',
        description = 'A very simple Rackspace Cloud Files uploader',
        version = '0.1',
        author = 'David Wittman',
        author_email = 'david@wittman.com',
        license = 'BSD',
        install_requires = reqs,
        scripts = ['cfupload.py']
    )
