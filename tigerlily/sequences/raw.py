# raw.py - Support for 'raw' (one-line-per-sequence) sequence format.
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

"""Support for sequences that don't fit any other format, or have none."""

from tigerlily.sequences import sequence

class RawSequence(sequence.FormattedSequence):
    """Container for a 'raw' sequence. This is just a bare sequence without
    any other syntactic or semantic requirement or information. That makes this
    class useful for handling sequences that don't fit in any other class.

    >>> seq = RawSequence(sequence='ATCGCGAGTCAGTCAGCATGACTACGCACAGTAC')
    
    One possible use of this container is to create Raw sequences that know
    their identifier. Raw sequences that are given an identifier don't forget
    it and will happily send it when being converted to and from different
    formats. They just don't ever use them in output.

    >>> seq = RawSequence(sequence='LALL',identifier='seq1')
    
    An example converting from Raw to FASTA and back, to prove it works:

    >>> import tigerlily.sequences as sequence
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
    

def parseRaw(file=None,data=None):
    r"""Parse the given file or data to yield all ``RawSequence`` objects

    Either *file* or *data* must be set. *data* must be a ``str`` object and
    *file* must be a file-like object opened in non-binary mode (such that it
    returns ``str`` objects when ``.read()`` is called.)

    >>> data = ("TGATCGCAGTCAG\n"
    ...         "ATATCGTA\n"
    ...         "\n"
    ...         "TTGATTAGCTAGTCGACGAT\n"
    ...         "\n"
    ...         "ACGTTGTTTTAGTCAGTC"
    ... )
    >>> seqs = [s for s in parseRaw(data=data)]
    >>> len(seqs)
    4
    >>> seqs[1].identifier
    'RawSeq_Line2'
    >>> seqs[2].identifier
    'RawSeq_Line4'

    And the equivalent using file-based objects:
    
    >>> from io import StringIO
    >>> data_f = StringIO(data)
    >>> seqs_f = [s for s in parseRaw(file=data_f)]
    >>> for s1,s2 in zip(seqs,seqs_f):
    ...     s1.sequence == s2.sequence
    ...     s1.identifier == s2.identifier
    True
    True
    True
    True
    True
    True
    True
    True

    """
    if (file and data) or (not file and not data):
        raise ValueError('Specify either file or data, and not both')

    if file:
        data = file.read()


    line_num = 0
    for line in data.split('\n'):
        line_num += 1
        seq = line.rstrip()
        if not seq:
            continue
        yield RawSequence(seq,identifier='RawSeq_Line{}'.format(line_num))

