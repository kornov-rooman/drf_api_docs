#!/usr/bin/python
import os

from distutils.core import setup

from drf_api_docs import __version__ as VERSION

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setup(
    name='drf_api_docs',
    version=VERSION,
    description='An API documentation generator for Django REST Framework',
    author='Kornov Rooman',
    author_email='kornov.rooman@gmail.com',
    url='https://github.com/kornov-rooman/drf_api_docs',
    download_url='https://github.com/kornov-rooman/drf_api_docs/archive/master.zip',
    packages=['drf_api_docs'],
    classifiers=[],
    requires=['django', 'coreapi', 'djagnorestframework'],
    install_requires=[
        'django>=1.10',
        'coreapi>=2.1.1',
        'djangorestframework>=3.5.3'
    ],
    license='MIT',
    keywords=['djangorestframework', 'rest_framework', 'drf', 'django', 'documentation'],
)
