try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'ResourceGuru Python',
    'author': 'Owen Barton',
    'url': 'https://github.com/grugnog/resourceguru',
    'version': '0.1',
    'install_requires': [],
    'requires': ['requests_oauth2'],
    'packages': ['resourceguru'],
    'scripts': [],
    'name': 'resourceguru'
}

setup(**config)
