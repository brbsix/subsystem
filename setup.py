# -*- coding: utf-8 -*-

from setuptools import find_packages, setup
from subsystem.subsystem import __description__, __program__, __version__


def read(filename):
    with open(filename) as f:
        return f.read()


setup(
    name=__program__,
    version=__version__,
    description=__description__,
    author='Brian Beffa',
    author_email='brbsix@gmail.com',
    long_description=read('README.rst'),
    url='https://github.com/brbsix/subsystem',
    license='GPLv3',
    keywords=['advertising', 'download', 'periscope', 'rename', 'srt',
              'ss', 'subscope', 'subtitle', 'thunar', 'yad'],
    packages=find_packages(),
    install_requires=['subnuker'],
    entry_points={
        'console_scripts': ['subsystem=subsystem.subsystem:main'],
    },
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: POSIX',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3 :: Only',
        'Topic :: Multimedia :: Video',
        'Topic :: Utilities',
    ],
)
