#!/usr/bin/env python3
# raw.py
# Support for 'raw' (one-line-per-sequence) sequence format.
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

from . import sequence

class RawSequence(sequence.PolymerSequence):
    """Container for a 'raw' sequence.

    Since raw reads are essentially just a sequence, this is a fairly useless
    class. It is more or less just a holder for the Raw sequence group object.

    >>> seq = RawSequence(sequence='ATCGCGAGTCAGTCAGCATGACTACGCACAGTAC')
    
    One possible use of this container is to create Raw sequences that know
    their identifier. Raw sequences that are given an identifier don't forget
    it and will happily send it when being converted to and from different
    formats. They just don't ever use them in output.

    >>> seq = RawSequence(sequence='LALL',identifier='seq1')
    
    An example converting from Raw to FASTA and back, to prove it works:

    >>> from . import sequence
    >>> fasta = seq.convert(sequence.FASTASequence)
    >>> seq2 = fasta.convert(RawSequence)
    >>> seq.sequence == fasta.sequence == seq2.sequence == 'LALL'
    True
    >>> seq.identifier == fasta.identifier == seq2.identifier == 'seq1'
    True

    """

    def __init__(self,sequence,identifier=None):
        self._sequence = sequence
        self._identifier = identifier
    
    @property
    def sequence(self):
        return self._sequence

    @property
    def identifier(self):
        # Maybe there is an identifier even though this is Raw?
        if self._identifier is not None:
            return self._identifier
        # Nothing worked, use the default.
        return super().identifier

    def _format(self):
        return "{}\n".format(self._sequence)

    def write(self,file):
        file.write(self._format())
    

class Raw(sequence.PolymerSequenceGroup):
    """Container for a set of raw (unformatted) sequences, one per line.

    Use this object to parse data that stores sequences one per line without
    any additional formatting or information beyond the read and a newline
    character for each read (except possibly the last one).

    Additionally, blank lines are skipped without an error (even if they 
    contain white space characters).

    >>> data = r'''
    ... CGTATACGCTCAGTC
    ... CGGGGCATCAGACTA
    ... CACGTACGACTACGTACGACTGACTGACTGCATCACATG
    ... 
    ... LAGVVGALVUIALKT
    ... '''
    >>> sequences = Raw(data=data)
    >>> len(sequences)
    4

    """
    
    def __init__(self,file=None,data=None):
        if file and data:
            raise ValueError('Only specify file or data, not both')

        if not file and not data:
            raise ValueError('You must specify file or data, but not both.')

        if file:
            data = file.read()

        self._load(data)


    def __iter__(self):
        for seq in self._sequences:
            yield seq

    def __len__(self):
        return len(self._sequences)

    def write(self,file):
        for seq in self:
            seq.write(file)

    def _load(self,data):
        self._sequences = []
        # TODO - use line numbers for identifiers? Probably yes but I'm
        #        leaving it out now for expediency
        for line in data.split('\n'):
            line = line.rstrip()
            if not line:
                continue

            self._sequences.append(RawSequence(sequence=line))


