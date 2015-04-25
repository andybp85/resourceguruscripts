try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'ResourceGuru Python for scripts',
    'author': 'Andrew Stanish for YouShallThrive, Inc. based on original by Owen Barton',
    'url': 'https://github.com/andybp85/resourceguruscrips',
    'version': '0.1',
    'install_requires': [],
    'requires': ['requests_oauth2'],
    'packages': ['resourceguruscrips'],
    'scripts': [],
    'name': 'resourceguru'
}

setup(**config)
