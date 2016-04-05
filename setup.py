#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

"""
Setup del proyecto utilizando el módulo setuptools
"""

setup(
    name='EC',
    version=0.0,
    # the project
    url="https://github.com/spolex/metaheuristics",

    # Author details
    author='spolex',
    author_email='spolexdroid@gmail.com',

    # license
    license='MIT',

    # What does your project relate to?
    keywords='sample setuptools development',

    install_requires=['numpy', 'pandas', 'deap', 'scipy'],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    # extras_require={
    #     'dev': ['check-manifest'],
    #     'test': ['coverage'],

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    pakage_data=[('bip_instances', ['main/Instances/BIP/*']), ('qap_instances', ['main/Instances/QAP/*'])],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    # entry_points={
    #     'console_scripts': [
    #         'sample=sample:main',
    #     ],
    # },
)
