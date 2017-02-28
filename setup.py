#!/usr/bin/env python

from setuptools import setup
import io

import StationTester

def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)

long_description = read(
    'algorithm/README.MODISL1DB',
    'algorithm/VERSION_HISTORY',
    'VERSIONLOG'
)
_version = read('algorithm/docs/VERSION')

setup(name='modisl1db',
    version=_version,
    description='MODIS Level-1 Direct Broadcast software package capable of '
        'processing Aqua and Terra Level 0 data to Level 1A and Level 1B.',
    long_description=long_description,
    url='http://oceancolor.gsfc.nasa.gov/seadas/modisl1db/',

    tests_require=['nose', 'StationTester'],
    install_requires=[
    ],
    dependency_links = [
        'https://github.com/USF-IMARS/StationTester/tarball/master#egg=StationTester-0.0.1'
    ]
    #packages=['myBoilerplatePackageName']
)
