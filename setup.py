#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: Catofes


from setuptools import setup, find_packages


setup(
    name='ImoutoPassword',
    version='0.0.1',
    packages=find_packages(),

    include_package_data=True,

    install_requires=[
        'requests',
    ],

    entry_points={
        'console_scripts': [
            'ipw = ImoutoPassword:start'
        ],
    },

    author='Catofes',
    author_email='i@catofes.com',
    url='https://github.com/Catofes/ImoutoPassword',
    description='A tool to generate and store password.',
    keywords=['password', 'manager', 'cli'],
    zip_safe=False,
)
