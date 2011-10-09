# genome_test.py - unit tests for genome.py
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

"""This module provides unit tests for the ``tigerlily.grc.genome``
module.

As with all unit test modules, the tests it contains can be executed in many
ways, but most easily by going to the project root dir and executing
``python3 setup.py nosetests``.
"""

import unittest
import tempfile
import os
import shutil

import tigerlily.grc.genome as gg

class GRCGenomeTester(unittest.TestCase):
    """Test harness for ``tigerlily.grc.genome.GRCGenome`` class.

    At this time, the tests specifically target downloaded genomes.
    """

    def setUp(self):
        """Create the testing environment"""
        self.test_dir = tempfile.mkdtemp()
        self.orig_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Remove the testing environment"""
        os.chdir(self.orig_dir)
        shutil.rmtree(self.test_dir)
    

   def test_NoDigest_NoRetry(self):
        """genome.py: Test local genome 'download', no digest no retry"""
        gen = gg.GRCGenome.download('test_nodigest', store=True)
        self.assertTrue(os.path.isfile('test_nodigest.assembly'))

   def test_GoodDigest_NoRetry(self):
        """genome.py: Test local genome 'download', good digest no retry"""
        gen = gg.GRCGenome.download('test_digest', store=True)
        self.assertTrue(os.path.isfile('test_digest.assembly'))

   def test_BadDigest_NoRetry(self):
        """genome.py: Test local genome 'download', bad digest no retry"""
        with self.assertRaises(EnvironmentError):
            gen = gg.GRCGenome.download('test_baddigest', store=True)
        self.assertFalse(os.path.isfile('test_baddigest.assembly'))

   def test_GoodDigest_FourRetry(self):
        """genome.py: Test local genome 'download', good digest 4 retry"""
        # Note that we wouldn't expect the retries to make a difference since
        # a local file download shouldn't ever fail digest verification, but
        # the test is still valid even if we don't EXPECT it to fail.
        gen = gg.GRCGenome.download('test_digest', store=True, retries=4)
        self.assertTrue(os.path.isfile('test_digest.assembly'))

   def test_BadDigest_FourRetry(self):
        """genome.py: Test local genome 'download', bad digest 4 retry"""
        with self.assertRaises(EnvironmentError):
            gen = gg.GRCGenome.download('test_baddigest', store=True, retries=4)
        self.assertFalse(os.path.isfile('test_baddigest.assembly'))
        
        
