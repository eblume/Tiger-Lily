# archive_test.py - unit tests for archive.py
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

"""This module provides unit tests for the ``tigerlily.utility.archive``
module.

As with all unit test modules, the tests it contains can be executed in many
ways, but most easily by going to the project root dir and executing
``python3 setup.py nosetests``.
"""

import unittest
import os

import tigerlily.utility.archive as ar


class ConsoleDownloaderTests(unittest.TestCase):
    """Test harness for ``tigerlily.utility.download.ConsoleDownloader`` class.
    """

    def setUp(self):
        """Create the testing environment"""
        self.test_dir = os.path.join(os.dirname(__file__),'test_archives')

    
        
        
