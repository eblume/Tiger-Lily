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
import glob

from setuptools import setup, find_packages

# The following is taken from python.org:
# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
    name = 'tigerliy',
    version = '0.1-dev',
    packages = find_packages(),
    scripts = glob.glob(os.path.join(os.path.dirname(__file__),'scripts/*')),
    
    # Required packages
    install_requires = [],
    
    # Non-python files that are required by the install
    package_data = {
        # 'package_name' : ['*.txt','*.dat'],
    },

    author = 'Erich Blume',
    author_email = 'blume.erich@gmail.com',
    description = ('Biological science tools for Python 3, with an emphasis '
                  'on speed for high throughput sequencing.'),
    license = 'GPLv3',
    keywords = 'python3 bioinformatics bio sequencing',
    url = None,
    long_description = read('README'),
)
