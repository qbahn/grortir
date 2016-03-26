#!/usr/bin/env python

"""Setup script for Grortir."""

import setuptools

from grortir import __project__, __version__

try:
    README = open("README.rst").read()
    CHANGES = open("CHANGES.rst").read()
except IOError:
    DESCRIPTION = "<placeholder>"
else:
    DESCRIPTION = README + '\n' + CHANGES

setuptools.setup(
    name=__project__,
    version=__version__,

    description="""Application for supporting
                 optimization of production process.""",
    url='https://github.com/qbahn/grortir',
    author='Wojtek Pietrucha',
    author_email='wojtekpietrucha@gmail.com',

    packages=setuptools.find_packages(),

    entry_points={'console_scripts': []},

    long_description=(DESCRIPTION),
    license='MIT',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],

    install_requires=open("requirements.txt").readlines(),
)
