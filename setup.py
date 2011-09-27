# setup.py -  Install script for distutils
# Authors:
#   * Erich Blume <blume.erich@gmail.com>
#
# Copyright 2011 Erich Blume <blume.erich@gmail.com>
#
#   This file is part of Tiger Lily.
#
#   Tiger Lily is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   Tiger Lily is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with Tiger Lily.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys
import glob

# distribute stuff
from distribute_setup import use_setuptools
use_setuptools()
from setuptools import setup, find_packages


# Finally, Tiger Lily stuff
sys.path.insert(0,'.')
from tigerlily import VERSION_INFO


# The following is taken from python.org:
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = 'TigerLily',
    version = VERSION_INFO[1],
    packages = find_packages(),
    scripts = glob.glob(os.path.join(os.path.dirname(__file__),'scripts/*')),
    
    # Non-python files that are equired by the install
    package_data = {
        'tigerlily' : ['grc/test_assemblies/*',],
        # 'package_name' : ['*.txt','*.dat'],
    },

    # Required packages for installation
    install_requires = [
        'docutils>=0.3', # for reStructuredText processing
    ],

    setup_requires = [
        'nose>=1.0',
    ],

    author = 'Erich Blume',
    author_email = 'blume.erich@gmail.com',
    description = ('Bioinformatics tools for Python 3'),
    license = 'GPLv3',
    keywords = 'python3 bioinformatics bio sequencing',
    url = 'https://github.com/eblume/Tiger-Lily',
    download_url='https://github.com/eblume/Tiger-Lily/tarball/master',
    long_description = read('README.rst'),

    test_suite = 'tests',
)
