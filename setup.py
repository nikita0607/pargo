from setuptools import setup, find_packages
from os.path import join, dirname

import os


print(os.listdir())

setup(
    name='pargo',
    version='1.3.0',
    url='https://github.com/nikita0607/pargo',
    license='MIT',

    author="nikita0607",
    author_email="ecfed205@gmail.com",

    packages=find_packages(),
    long_description=open(join(dirname(__file__), 'README.md')).read(),

    install_requires=[]
)
