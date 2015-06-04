try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'name'         : 'resourceguruscripts',
    'packages'     : ['resourceguruscripts'],
    'version'      : '0.8.4',
    'description'  : 'ResourceGuru Python for Scripts',
    'author'       : 'Andrew Stanish for YouShallThrive, Inc. based on original by Owen Barton',
    'author_email' : 'andy@youshallthrive.com',
    'url'          : 'https://github.com/andybp85/resourceguruscripts',
    'download_url' : 'https://github.com/andybp85/resourceguruscripts/tarball/0.8.4',
    'keywords'     : ['resourceguru'],
    'classifiers'  : [],
    'requires'     : ['requests_oauthlib']
    }

setup(**config)
