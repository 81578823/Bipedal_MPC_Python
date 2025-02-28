from setuptools import find_packages
from setuptools import setup

setup(
    name='trans',
    version='0.0.0',
    packages=find_packages(
        include=('trans', 'trans.*')),
)
