#!/usr/bin/env python3
# genomic.py
# Support gor genomic (chromosomal DNA) sequences
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

from .sequence import PolymerSequence
from .mixed import MixedSequenceGroup

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
        return self._identifier

    def _format(self):
        raise NotImplementedError('Attempt to format a genomic sequence. '
                                  'Try casting to another sequence type first.')
    def write(self,file):
        raise NotImplementedError('Attempt to write a genomic sequence. '
                                  'Try casting to another sequence type first.')
        

def createGenomicSequenceGroup(sequence_group):
    r"""Convert any PolymerSequenceGroup descendent in to a genomic version.

    This helper function will take any instance of a descendent of
    PolymerSequenceGroup and convert it in to an instance of
    MixedSequenceGroup in which every internal sequence is a GenomicSequence.

    This allows for the creation of a group of GenomicSequence objects.

    >>> from . import raw
    >>> sequences = raw.Raw(data='AGTACGTATTTCAT\nTTCATACGACTAC\n')
    >>> len(sequences)
    2
    >>> genomic = createGenomicSequenceGroup(sequences)
    >>> len(genomic)
    2
    >>> for seq in genomic:
    ...     isinstance(seq,GenomicSequence)
    ...
    True
    True

    """

    new_group = MixedSequenceGroup()
    
    for sequence in sequence_group:
        new_group.add(sequence.convert(GenomicSequence))

    return new_group
    

