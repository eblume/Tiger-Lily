# genomic.py - Support for genomic (chromosomal DNA) sequences
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

import re
import string

from tigerlily.sequences.sequence import PolymerSequence
from tigerlily.sequences.mixed import MixedSequenceGroup


COMPLEMENT_TRANS = str.maketrans('atgcATGC','tacgTACG')

class GenomicSequence(PolymerSequence):
    """Container for Genomic (chromosomal DNA) sequences.
    
    In general this is not an 'input' or 'output' format, but rather an
    internal format that constrains the sequence to a certain set of
    allowed characters in the sequence.

    Those characters are captured by the regular expression
        [atgcATGCN]+
    If a sequence is converted to a GenomicSequence and doesn't fit that
    regular expression, ValueError will be raised.

    GenomicSequence objects do not have a valid write() method, nor do
    they have a valid format() method. (Instead they will raise
    NotImplementedError.)

    >>> from . import raw
    >>> seq = raw.RawSequence('CTAGCATACTCACAGT')
    >>> genomic = seq.convert(GenomicSequence)
    >>> genomic.sequence
    'CTAGCATACTCACAGT'
    
    An example where the constraint fails:
    
    >>> seq = raw.RawSequence('LAVVUGHTLK')
    >>> genomic = seq.convert(GenomicSequence)
    Traceback (most recent call last):
        ...
    ValueError: Invalid genomic sequence format: LAVVUGHTLK

    """

    
    def __init__(self,sequence,identifier=None):
        if not re.match(r'[atgcATGCN]+',sequence):
            raise ValueError('Invalid genomic sequence format: {}'.format(
                sequence,
            ))

        self._sequence = sequence
        self._identifier = identifier

    @property
    def sequence(self):
        return self._sequence

    @property
    def identifier(self):
        if self._identifier is None:
            return 'UnknownSeq_{chcksum}'.format(hash(self._sequence))
        return self._identifier

    def _format(self):
        raise NotImplementedError('Attempt to format a genomic sequence. '
                                  'Try casting to another sequence type first.')
    def write(self,file):
        raise NotImplementedError('Attempt to write a genomic sequence. '
                                  'Try casting to another sequence type first.')

    def reverse(self):
        """Return a new sequence that is the reverse of this sequence.
        
        >>> seq1 = GenomicSequence('AATGCC')
        >>> rseq1 = seq1.reverse()
        >>> rseq1.sequence
        'CCGTAA'
        >>> seq2 = rseq1.reverse()
        >>> seq2.sequence == seq1.sequence
        True

        """
        return GenomicSequence(self._sequence[::-1],identifier=self._identifier)

    def complement(self):
        """Return the purine<->pyrimidine complement of the sequence
        as a new sequence.

        >>> seq1 = GenomicSequence('AATGCC')
        >>> cseq1 = seq1.complement()
        >>> cseq1.sequence
        'TTACGG'
        >>> seq2 = cseq1.complement()
        >>> seq2.sequence == seq1.sequence
        True
        """
        return GenomicSequence(self._sequence.translate(COMPLEMENT_TRANS),  
                               identifier=self._identifier)

    def reverse_complement(self):
        """Return the reverse complement of the sequence as a new sequence.

        Has the same result as sequence.reverse().complement(), but slightly
        more efficient.

        >>> seq1 = GenomicSequence('AATGCC')
        >>> rcseq1 = seq1.reverse_complement()
        >>> rcseq1.sequence
        'GGCATT'
        >>> seq2 = rcseq1.reverse_complement()
        >>> seq2.sequence == seq1.sequence
        True
        >>> rcseq1.sequence == seq1.reverse().complement().sequence
        True
        """
        return GenomicSequence(rev_comp(self.sequence),
                               identifier=self._identifier)
        
def rev_comp(sequence):
    """Compute the reverse complement of the input string.

    Input is assumed to be a string that could be the sequence of a
    GenomicSequence. 

    >>> rev_comp('ACGGTC')
    'GACCGT'
    >>> rev_comp('GACCGT')
    'ACGGTC'
    """
    return sequence[::-1].translate(COMPLEMENT_TRANS)

def createGenomicSequenceGroup(*sequences):
    r"""Convert any group of sequences in to a genomic MixedSequence group.

    >>> from tigerlily.sequences.rar import Raw
    >>> sequences = Raw(data='AGTACGTATTTCAT\nTTCATACGACTAC\n')
    >>> len(sequences)
    2
    >>> genomic = createGenomicSequenceGroup([s for s in sequences])
    >>> len(genomic)
    2
    >>> for seq in genomic:
    ...     isinstance(seq,GenomicSequence)
    ...
    True
    True

    """

    new_group = MixedSequenceGroup()
    
    for sequence in sequences:
        new_group.add(sequence.convert(GenomicSequence))

    return new_group
    

