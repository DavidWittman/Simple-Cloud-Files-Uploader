#!/usr/bin/env python

from setuptools import setup

VERSION = '0.4'
REQS = ['python-cloudfiles']

setup(
    name = 'cfupload',
    url = 'https://github.com/DavidWittman/Simple-Cloud-Files-Uploader',
    description = 'A very simple Rackspace Cloud Files uploader',
    version = VERSION,
    author = 'David Wittman',
    author_email = 'david@wittman.com',
    license = 'BSD',
    install_requires = REQS,
    scripts = [ 'src/cfupload' ],
    classifiers = [
        'Environment :: Console',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP',
        'Topic :: Utilities',
        'License :: OSI Approved :: BSD License'
    ]
)
