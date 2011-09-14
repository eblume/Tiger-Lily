# fixedtree.py - Fixed-width substring tree index for genomic sequences.
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

from tigerlily.index.index import GroupIndex

class FixedTree(GroupIndex):
    """GroupIndex wrapper which implements a Fixed-Width Substring Tree.
    
    The resulting tree supports alignments of a fixed width only. It supports
    memory and time efficient lookups including mismatches. It does not support
    gaps, indels, arbitrary width lookups, etc.

    As an example, the following block of code will create a MixedSequenceGroup
    that we can index.

    >>> from tigerlily.sequences import GenomicSequence
    >>> from tigerlily.sequences import createGenomicSequenceGroup
    >>> s1 = GenomicSequence('ACGTACTTAGCATCATACGTCAGTACGCAGTCAGTCAGTCAT')
    >>> s2 = GenomicSequence('CGAGCGACGCAGTACGTACTGGCAGACGTGTATACCTGC')
    >>> group = createGenomicSequenceGroup(s1,s2)

    And now we create that index for alignments of width 5.

    >>> index = FixedTree(group,5)

    This index will be used in later examples.

    """

    def __init__(self, sequence_group, width, reverse=False):
        """Creates a FixedTree from the given sequence_group and fixed width.

        sequence_group may be any subclass of
        tigerlily.sequences.PolymerSequenceGroup, although it will most usually
        be a MixedSequenceGroup composed of GenomicSequence objects that
        correspond to reference chromosomes. 

        width is an integer that must be greater than 0, although for reasonable
        performance it should also be greater than about 20. After this index
        is created, only reads that are exactly as long as width may be aligned

        If reverse is set to True, then each input sequence's reverse
        complement is also processed. Alignments on these strands are reported
        with the same position and chromosome name, but with 'strand' as False.
        Note that the reported position of a reverse strand alignment will be
        the same position as the given sequence's reverse complement's position.

        See the documentation for the parent class for an example.
        """
        pass

    def __contains__(self, sequence):
        """Return true if, given the arguments, the sequence is in the index.

        As with alignments(), sequence must be a string. Raises ValueError if
        the length of the sequence does not match the index width.

        The alignment is performed as if alignments() was called with all
        optional arguments left at their default.

        >>> 'TACGT' in index
        True
        >>> 'ACGTA' in index # reverse compliment of the above
        True
        >>> 'GGGGG' in index
        False
        >>> 'TACTTAGCA' in index
        Traceback (most recent call last):
            ...
        ValueError: aligned read is not the right width for this index

        """
        return len(self.alignments(sequence)) > 0

    def alignments(self, sequence, mismatches=0,
            maximum_alignments=None,
            best_alignments=False,
        ):
        """Returns a list of all alignments produced by the given input.

        Retrurns a list of tuples, each tuple containing three values. They are:
            0: str - 'chromosome name'
            1: int - 'position'
            2: boolean - 'strand' (True means 'reported strand', False means
                                   'opposing strand'. Opposing strand matches
                                   do not alter the original position.)

        Each reported alignment will have a computed 'Hamming Distance' (see
        http://en.wikipedia.org/wiki/Hamming_distance ) of no greater than the
        mismatches argument. If left at 0, no actual edit distance calculations
        are performed.

        If maximum_alignments is an integer greater than 0, then only that many
        alignments will be found - after that many are found, the search ends.

        If best_alignments is False, then every possible alignment will be found
        even if maximum_alignments is set. Then, alignments are reported in
        increasing order of their edit distance from the search sequence. In
        general, this function will slow down the search considerably,
        particularly if maximum_alignments is set (since the primary benefit of
        maximim_alignments will be negated.)

        This will raise ValueError if the given sequence does not match the
        pre-specified width of the index.

        >>> seq = GenomicSequence('GGAATTCC',identifier='foo')
        >>> seqgroup = createGenomicSequenceGroup(seq)
        >>> index = FixedTree(seqgroup,2)
        >>> index.alignments('GG')
        [('foo',0,True)]
        
        Note that for the next example with mismatches, the order of the result
        is unspecified, so we will just wrap it with len() to avoid testing
        errors. You don't need to wrap the result in len() in your own code.

        >>> len(index.alignments('GG',mismatches=1))
        2

        For the next example we enable best_alignments, so the order is 
        gaurunteed.        

        >>> index.alignmnets('GG',mismatches=1,best_alignmnets=True)
        [('foo', 0, True), ('foo', 1, True)]
        >>> index.alignments('GA',mismatches=1,best_alignments=True)
        [('foo', 1, True), ('foo', 0, True), ('foo', 2, True)]

        """
        pass
