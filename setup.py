import os
from setuptools import setup

BASE_PATH = os.path.abspath(os.path.dirname(__file__))
README = open(os.path.join(BASE_PATH, 'README.rst')).read()

__version__ = '0.0.6'
__author__ = 'Masashi Shibata <contact@c-bata.link>'
__author_email__ = 'contact@c-bata.link'
__license__ = 'MIT License'
__classifiers__ = (
    'Development Status :: 2 - Pre-Alpha',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Topic :: Internet :: WWW/HTTP :: WSGI',
    'Topic :: Internet :: WWW/HTTP :: WSGI :: Middleware',
    'Programming Language :: Python',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
)


setup(
    name='wsgi-static-middleware',
    version=__version__,
    author=__author__,
    author_email=__author_email__,
    url='https://github.com/c-bata/wsgi-static-middleware',
    description='WSGI Middleware for serving static files',
    long_description=README,
    classifiers=__classifiers__,
    py_modules=['wsgi_static_middleware'],
    keywords='wsgi middleware staticfile',
    license=__license__,
    include_package_data=True,
    test_suite='tests',
)
