#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = [
    'astropy',
    'scipy',
    'pyspectral'
    # TODO: put package requirements here
]

setup_requirements = [
    'pytest-runner',
    # TODO(michaelaye): put setup requirements (distutils extensions, etc.) here
]

test_requirements = [
    'pytest',
    'nbval'
    # TODO: put package test requirements here
]

setup(
    name='pytelescope',
    version='0.1.0',
    description="Package to support design and operation of space mission telescopes",
    long_description=readme + '\n\n' + history,
    author="K.-Michael Aye",
    author_email='kmichael.aye@gmail.com',
    url='https://github.com/michaelaye/pytelescope',
    packages=find_packages(include=['pytelescope']),
    include_package_data=True,
    install_requires=requirements,
    license="ISC license",
    zip_safe=False,
    keywords='pytelescope',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    test_suite='tests',
    tests_require=test_requirements,
    setup_requires=setup_requirements,
)
