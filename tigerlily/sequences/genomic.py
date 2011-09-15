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

class NucleicSequence(PolymerSequence):
    """Container for nucleic (chromosomal DNA) sequences.
    
    In general this is not an 'input' or 'output' format, but rather an
    internal format that constrains the sequence to a certain set of
    allowed characters in the sequence.

    Those characters are captured by the regular expression
        [atgcATGCN]+
    If a sequence is converted to a NucleicSequence and doesn't fit that
    regular expression, ValueError will be raised.

    NucleicSequence objects do not have a valid write() method, nor do
    they have a valid format() method. (Instead they will raise
    NotImplementedError.)

    >>> from . import raw
    >>> seqdata = 'CTAGCATACTCACAGT'
    >>> seq = raw.RawSequence(seqdata)
    >>> nucleic = seq.convert(NucleicSequence)
    >>> nucleic.sequence
    'CTAGCATACTCACAGT'

    An example showing that NucleicSequence objects can be instantiated
    directly.

    >>> seq2 = NucleicSequence(seqdata)
    >>> seq2.sequence == nucleic.sequence
    True
    
    An example where the constraint fails:
    
    >>> seq = raw.RawSequence('CAGTTACTm')
    >>> nucleic = seq.convert(NucleicSequence)
    Traceback (most recent call last):
        ...
    ValueError: Invalid nucleic sequence format
    """

    
    def __init__(self,sequence,identifier=None):
        if not re.match(r'[atgcATGCN]+$',sequence):
            raise ValueError('Invalid nucleic sequence format')

        self._sequence = sequence
        self._identifier = identifier

    @property
    def sequence(self):
        return self._sequence

    @property
    def identifier(self):
        """The identifier for this read.

        If the identifier was unspecified, a placeholder will be used that
        includes a hash value checksum of the sequence.

        >>> seq = NucleicSequence('GGGACTG')
        >>> seq.identifier
        'UnknownSeq_7276410743868358753'
        >>> seq = NucleicSequence('AGGCTA')
        >>> seq.identifier
        'UnknownSeq_-8092672563224726703'
        >>> seq = NucleicSequence('AGGCTA',identifier='chr1')
        >>> seq.identifier
        'chr1'
        """
        # TODO - don't use hash(), use something smarter.
        if self._identifier is None:
            return 'UnknownSeq_{}'.format(hash(self._sequence))
        return self._identifier

    def reverse(self):
        """Return a new sequence that is the reverse of this sequence.
        
        >>> seq1 = NucleicSequence('AATGCC')
        >>> rseq1 = seq1.reverse()
        >>> rseq1.sequence
        'CCGTAA'
        >>> seq2 = rseq1.reverse()
        >>> seq2.sequence == seq1.sequence
        True

        """
        return NucleicSequence(self._sequence[::-1],identifier=self._identifier)

    def complement(self):
        """Return the purine<->pyrimidine complement of the sequence
        as a new sequence.

        >>> seq1 = NucleicSequence('AATGCC')
        >>> cseq1 = seq1.complement()
        >>> cseq1.sequence
        'TTACGG'
        >>> seq2 = cseq1.complement()
        >>> seq2.sequence == seq1.sequence
        True
        """
        return NucleicSequence(self._sequence.translate(COMPLEMENT_TRANS),  
                               identifier=self._identifier)

    def reverse_complement(self):
        """Return the reverse complement of the sequence as a new sequence.

        Has the same result as sequence.reverse().complement(), but slightly
        more efficient.

        >>> seq1 = NucleicSequence('AATGCC')
        >>> rcseq1 = seq1.reverse_complement()
        >>> rcseq1.sequence
        'GGCATT'
        >>> seq2 = rcseq1.reverse_complement()
        >>> seq2.sequence == seq1.sequence
        True
        >>> rcseq1.sequence == seq1.reverse().complement().sequence
        True
        """
        return NucleicSequence(reverse_complement(self.sequence),
                               identifier=self._identifier)


class AminoSequence(PolymerSequence):
    """PolymerSequence for aminoacid sequences (e.g. protein sequences).

    Each member of the sequence must be one of ABCDEFGHIKLMNOPQRSTUVWYZX*-
    """
    
    def __init__(self,sequence,identifier=None):
        """Create a new AminoSequence, and validates the sequence.

        If the sequence is not composed of characters that are in
        ABCDEFGHIKLMNOPQRSTUVWYZX*- then ValueError will be raised.
        
        >>> seq = AminoSequence('ADKKYMZZB*EE')
        >>> seq2 = AminoSequence('ADKKYMZZB*EE',identifier='seq2')
        >>> seq3 = AminoSequence('ADKKYMZZB*EEJ')
        Traceback (most recent call last):
            ...
        ValueError: invalid character in AminoSequence
        """
        if not re.match(r'[ABCDEFGHIKLMNOPQRSTUVWYZX*\-]+$',sequence):
            raise ValueError('invalid character in AminoSequence')

        self._sequence = sequence
        self._identifier = identifier

    @property
    def sequence(self):
        return self._sequence

    @property
    def identifier(self):
        """Returns the identifier, if any.

        If the identifier has not been explicitly set, the default identifier
        will be used instead.
        """
        if self._identifier is None:
            return super().identifier
        return self._identifier
        
def reverse_complement(sequence):
    """Compute the reverse complement of the input string.

    Input is assumed to be a string that could be the sequence of a
    NucleicSequence. 

    >>> reverse_complement('ACGGTC')
    'GACCGT'
    >>> reverse_complement('GACCGT')
    'ACGGTC'
    """
    return sequence[::-1].translate(COMPLEMENT_TRANS)

def createNucleicSequenceGroup(*sequences):
    r"""Convert any group of sequences in to a nucleic MixedSequence group.

    >>> from tigerlily.sequences.raw import Raw
    >>> sequences = Raw(data='AGTACGTATTTCAT\nTTCATACGACTAC\n')
    >>> len(sequences)
    2
    >>> nucleic = createNucleicSequenceGroup(*[s for s in sequences])
    >>> len(nucleic)
    2
    >>> for seq in nucleic:
    ...     isinstance(seq,NucleicSequence)
    ...
    True
    True

    """

    new_group = MixedSequenceGroup()
    
    for sequence in sequences:
        new_group.add(sequence.convert(NucleicSequence))

    return new_group

