import os
from setuptools import setup

with open(os.path.join(os.path.dirname(__file__), 'README.rst')) as readme:
    README = readme.read()


setup(
    name='movielist',
    version='1.0.0',
    packages=['movielist'],
    description='Find nice moives from douban',
    long_description=README,
    author='Arwen Chen',
    author_email='ywchen92@gmail.com',
    install_requires=['wxPython-Phoenix', 'beautifulsoup4'],
    classifiers=[
        'Programming Language :: Python',
        # Replace these appropriately if you are stuck on Python 2.
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
    ],
)
