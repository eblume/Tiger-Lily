#!/usr/bin/env python3
# mixed.py
# Support for sequence groups of mixed type.
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

from .sequence import PolymerSequenceGroup


class MixedSequenceGroup(PolymerSequenceGroup):
    r"""PolymerSequenceGroup that allows sequences of any type.
    
    What this gains in flexibility, it loses in representation. This
    subclass of PolymerSequenceGroup does not have a .write() method, since
    there probably isn't a good way to represent the sequences it contains.

    We also gain an add() method, which allows additional sequences to be
    added to the sequence group after initialization - perhaps the key
    benefit of a MixedSequenceGroup.

    >>> from .sequence import FASTASequence
    >>> from .raw import RawSequence, Raw
    >>> seq1 = FASTASequence(sequence='aCGTAtagcATCA',identifier='seq1')
    >>> seq2 = RawSequence(sequence='GGCATACGGCAatacgaCATN')
    >>> sequences = Raw(data='GGCATACT\nGAGcgaACT\n')
    >>> genomic = MixedSequenceGroup(sequences)
    >>> len(genomic)
    2
    >>> genomic.add(seq1)
    >>> genomic.add(seq2)
    >>> len(genomic)
    4
    >>> genomic = MixedSequenceGroup()
    >>> len(genomic)
    0
    >>> genomic.add(seq1)
    >>> len(genomic)
    1

    """

    def __init__(self,sequence_group=None):
        self._sequences = []
        if sequence_group:
            for sequence in sequence_group:
                self.add(sequence)

    def __iter__(self):
        for sequence in self._sequences:
            yield sequence

    def __len__(self):
        return len(self._sequences)

    def add(self,sequence):
        self._sequences.append(sequence)

    # Yes, that was a WHOLE lotta documentation for a very very thin class.
    # But doesn't it make you just feel warm inside?


