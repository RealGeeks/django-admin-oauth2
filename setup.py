from setuptools import setup
from os.path import dirname, join

try:
    with open(join(dirname(__file__), 'README.md')) as f:
        README = f.read()
except IOError:
    README = '<no description>'

install_requires = ['oauthlib','requests_oauthlib']

try:
    import importlib
except ImportError:
    install_requires.append('importlib')


setup(
    name='django-admin-oauth2',
    version='0.2.6',
    description='A django app that replaces the django admin authentication mechanism by deferring to an oauth2 provider',
    long_description=README,
    url='https://github.com/RealGeeks/django-admin-oauth2',
    author='Real Geeks LLC',
    author_email='andrew@realgeeks.com',
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
    ],
    license='MIT',
    install_requires=install_requires,
    packages=['oauthadmin'],
)
