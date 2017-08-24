"""
flask_private_area
------------------

flask_private_area uses Flask-AutoIndex with a simple authentication, via
a sqlite database.

The initial goal was to keep an persistent authentication when an authenticated
user still navigates in a private area.
A very short expiration time cookie is used and set each time the user goes on
a page in the private area.

"""

from setuptools import setup
from flask_private_area import __version__

setup(
    name='flask_private_area',
    version = __version__,
    license = 'BSD',
    author = 'Benoît Pineau',
    author_email = 'beny@sickless.net',
    url = 'https://github.com/sickless/flask_private_area',
    description = 'flask_autoindex with simple authentication',
    long_description = __doc__,
    platforms = 'any',
    packages=['flask_private_area'],
    include_package_data=True,
    install_requires=[
        'flask_autoindex==0.6',
    ],
)
