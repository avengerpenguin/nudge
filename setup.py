#!/usr/bin/env python

from setuptools import setup

setup(
    name="nudge",
    version="0.0.0",
    author='The Launch Ninja',
    author_email='ross@thelaunch.ninja',
    packages=['nudge'],
    description='nudge MVP',
    install_requires=['django', 'django-zappa', 'clize'],
)
