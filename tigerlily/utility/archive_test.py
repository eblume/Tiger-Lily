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
from tigerlily.sequences import parseFASTA


class ArchiveTests(unittest.TestCase):
    """Test harness for ``tigerlily.utility.archive.Archive`` class.
    """

    def setUp(self):
        """archive.py: Create the testing environment"""
        self.test_dir = os.path.join(os.path.dirname(__file__),'test_archives')
        self.targz = os.path.join(self.test_dir, 'test_fasta_archive.tar.gz')
        self.tarbz2 = os.path.join(self.test_dir, 'test_fasta_archive.tar.bz2')
        self.tar = os.path.join(self.test_dir, 'test_fasta_archive.tar')
        self.zip = os.path.join(self.test_dir, 'test_fasta_archive.zip')

    def test_targz(self):
        "archive.py: Test .tar.gz archive support"
        arch = ar.Archive(filepath=self.targz)
        self._handle_arch(arch)

    def test_tarbz2(self):
        "archive.py: Test .tar.bz2 archive support"
        arch = ar.Archive(filepath=self.tarbz2)
        self._handle_arch(arch)

    def test_tar(self):
        "archive.py: Test .tar archive support"
        arch = ar.Archive(filepath=self.tar)
        self._handle_arch(arch)

    def test_zip(self):
        "archive.py: Test .zip archive support"
        arch = ar.Archive(filepath=self.zip)
        self._handle_arch(arch)

    def _handle_arch(self,arch):
        "handler for testing an Archive object regardless of format"
        self.assertEqual(len(arch.getnames()),4)

        fasta_files = [f for f in arch.getfasta()]
        self.assertEqual(len(fasta_files),3)

        nofasta_files = [f for f in arch.getnofasta()]
        self.assertEqual(len(nofasta_files),1)

        # Finally, just test to make sure that FASTA can handle the test files
        # This isn't really a test of this unit, but it's a logical extension
        # and it would be bad if it failed, so let's do the test.
        for fasta_fileobj in arch.getfasta():
            for fasta_seq in parseFASTA(fasta_fileobj):
                self.assertTrue(len(fasta_seq.sequence) > 0)
                self.assertTrue(fasta_seq.identifier.startswith('seq'))
    
        
        
