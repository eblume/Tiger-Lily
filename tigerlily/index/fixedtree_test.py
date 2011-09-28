# fixed_test.py - unit tests for fixedtree.py
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

"""This module provides unit tests for the ``tigerlily.index.fixedtree``
module.

As with all unit test modules, the tests it contains can be executed in many
ways, but most easily by going to the project root dir and executing
``python3 setup.py nosetests``.
"""

import unittest
import tempfile
import os
import shutil

from tigerlily.sequences import createNucleicSequenceGroup, NucleicSequence
import tigerlily.index.fixedtree as ft

class FixedTreeTests(unittest.TestCase):
    """Test harness for ``tigerlily.index.fixedtree.FixedTree`` class.
    """

    def setUp(self):
        """Create the testing environment"""
        self.test_dir = tempfile.mkdtemp()
        self.orig_dir = os.getcwd()
        os.chdir(self.test_dir)

        self.seq_grp = createNucleicSequenceGroup(
            NucleicSequence('TGTACGTACTTACGCATTCAGGCAGTCA',identifier='seq1'),
            NucleicSequence('GGACTTTACTGACACGTTACTGGG',identifier='seq2'),
        )
    
        # Comment '^' shows an alignment for 'TTTTT' with 1 mismatch
        self.extra_seq = NucleicSequence('GGAACGTACTTATCGTCTGTCAGTACTTATTTAT'  
           #                                                        ^^ ^^    
            'TGGTCAGTTGAGGTTATACGTTATTTATTATTTTTATTATGTCAGGTCATTGGGCGATGTCAG'  
           #                     ^^ ^^  ^^^^^^^                              
            'GGTCGGTACGTTTTATCTGGTGGGCAGCTGCTGATATTATATATAGCGTACGCATAGCGCGCG'   
           #          ^^^                                                    
            'GGGGCGGAGCGGACGACTCATATTATCTACACACTACGCATGAGCTATGACCACATGGACTCA',  
           #                                                                 
           # In other words, 'TTTTT' aligns 18 times with 1 mismatch
            identifier='seq3',
        )

        self.index_width = 5

    def tearDown(self):
        """Remove the testing environment"""
        os.chdir(self.orig_dir)
        shutil.rmtree(self.test_dir)

    def test_create_index(self):
        """fixedtree.py: Test tree creation from NucleicSequence group"""
        index = ft.FixedTree(self.seq_grp,self.index_width)
        self._search_index_subtest(index)
    
    def test_store_index(self):
        "fixedtree.py: Test writing FixedTree to disk"
        pass

    def _search_index_subtest(self, index):
        "subtest to test the given tree index"
    
        self.assertFalse('GGGGG' in index)
        index.add_sequence(self.extra_seq,False)
        self.assertTrue('GGGGG' in index)

        alignments = index.alignments('TTTTT')
        self.assertEqual(len(alignments),1)

        alignments = index.alignments('TTTTT',mismatches=1)
        self.assertEqual(len(alignments),18)
        self.assertTrue(('seq3', 108, True) in alignments)
        self.assertTrue(('seq3', 27, True) in alignments)
        self.assertTrue(('seq3', 64, True) in alignments)

        self.assertFalse('CCCCC' in index)
        index.add_sequence(self.extra_seq,True)
        self.assertTrue('CCCCC' in index)
        


        

