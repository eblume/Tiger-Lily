# fasta.py - NCBI-compatible FASTA formatted sequences
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

"""Support for the NCBI FASTA format.

This implementation honors the NCBI FASTA requirement that sequences not
contain any comments (only a single identifier line is allowed), and that '>'
is the only valid identifier character (not ';').
"""

import re
import textwrap


from tigerlily.sequences.sequence import FormattedSequence

class FASTASequence(FormattedSequence):
    r"""Container for a single FASTA Sequence.

    To parse a list of FASTA sequences out of a FASTA-formatted file, use
    ``parseFASTA()`` from this module. To create a FASTA-formatted file
    from a list of (any type of) sequence, use ``writeFASTA()``.

    You can also instantiate ``FASTASequence``
    objects directly. There is often little
    point in doing so, but it is an option available to you. Keep in mind
    that ``FASTASequence`` objects *need* both a sequence and an identifier.

    ``FASTASequence`` sequences must use a subset of the NCBI specification.
    The sequence must only contain uppercase or lowercase variants of the
    characters in either ``FASTASequence.ALLOWED_NUCLEIC_CHARS`` or
    ``FASTASequence.ALLOWED_AMINO_CHARS``. You can override the variables or
    (preferably) subclass ``FASTASequence`` to allow different characters in
    the sequence (and you are encouraged to do so),
    but you then lose the gauruntee that the resulting
    sequence will always be NCBI-portable. Note that 'degenerate' sequences
    and some other control or meta sequences are not supported in this
    implementation even though the NCBI specification does allow them - this
    is for interoperability with other Tiger Lily sequence classes.=

    >>> seq1 = FASTASequence('TTAATTCTACTTATTTTATTA',identifier='seq1')
    >>> seq1.format()
    '>seq1\nTTAATTCTACTTATTTTATTA\n'
    
    """
    
    # The FASTA format often specified a maximum line width. This is that.
    MAX_LINE_WIDTH = 79
    ALLOWED_NUCLEIC_CHARS = 'ATGCUN'
    ALLOWED_AMINO_CHARS = 'ACDEFGHIKLMNPQRSTVWYX*'

    # Required functions

    def __init__(self,sequence,identifier):
        # Note that for FASTA, unlike other formats, an identifier is REQUIRED

        # Check the sequence to make sure it conforms to NCBI-reduced
        all_allowed = ''.join(set(
            self.ALLOWED_NUCLEIC_CHARS + self.ALLOWED_NUCLEIC_CHARS.lower() + 
            self.ALLOWED_AMINO_CHARS + self.ALLOWED_AMINO_CHARS.lower()))

        if not re.match(r'[{}]+'.format(all_allowed),sequence):
            raise ValueError('FASTA sequence contains bad chars')

        self._sequence = sequence
        self._identifier = identifier
    
    @property
    def sequence(self):
        """The sequence of this FASTASequence."""
        return self._sequence

    @property
    def identifier(self):
        """The identifier of this FASTASequence.

        Note that unlike many other ``PolynomialSequence`` descendents, this
        class *requires* a valid identifier to be given at init time.
        """
        return self._identifier

    def _format(self):
        """Internal function to get a format string from this sequence"""
        # Note that FASTA sequences are often times megabases-long. These
        # sequences will perform poorly in generating a single string.
        # Instead, you may wish to use the FASTA-specific 'write' method.
        return ">{id}\n{seq}\n".format(
            id=self.identifier,
            seq = '\n'.join(textwrap.wrap(self.sequence,
                                               width=self.MAX_LINE_WIDTH)),
        )

    def write(self,file):
        """Write this FASTA sequence to the opened file object.

        Note that this function has the same result as writing the output of
        .format(). However, this function will outperform* that approach for
        large sequences (such as reference genomes stored in FASTA format),
        because this function doesn't store the entire sequence in memory a
        second time like .format() does (for text wrapping purposes).
        
        *: OK, the performance will be mostly identical, it's just that the
           memory footprint should be much smaller.
        """
    
        seq = self.sequence
        if not seq:
            raise ValueError('Empty or invalid sequence: "{}"'.format(seq))
        
        file.write('>{}\n'.format(self.identifier))

        for i in range(0,len(seq),self.MAX_LINE_WIDTH):
            file.write('{}\n'.format(seq[i:i+self.MAX_LINE_WIDTH]))


def parseFASTA(file=None,data=None):
    r"""Parse the given file or data and return ``FASTASequence`` objects.

    This function will generate each sequence in *file* or *data*.

    You must specify either *file* or *data* and not both. *data* must be a
    sequence of type ``str`` (and not ``bytes``). *file* can be any file-like
    object opened for reading in non-binary mode (such that ``file.read()`` will
    produce ``str`` objects).

    >>> example_data = (">seq1\n"
    ... "CATTTACGGTACGTGATCTTACGATGCTAGCTTTGTACTAC\n"
    ... ">seq2\n"
    ... "TTAGGGACGTAATCGGACTCAGACGTTTTATGCGCGCGGCGCTTGGCGATATTAGGCGT\n"
    ... )
    >>> seqs = [s for s in parseFASTA(data=example_data)]
    >>> len(seqs)
    2
    >>> seqs[1].identifier
    'seq2'
    >>> seqs[0].sequence
    'CATTTACGGTACGTGATCTTACGATGCTAGCTTTGTACTAC'
    
    And then, as a file-object:
    
    >>> from io import StringIO
    >>> filewrap = StringIO(example_data)
    >>> file_seqs = [s for s in parseFASTA(file=filewrap)]
    >>> len(file_seqs)
    2

    The results are equivalent:
    
    >>> for s1,s2 in zip(seqs,file_seqs):
    ...     s1.sequence == s2.sequence
    ...     s1.identifier == s2.identifier
    True
    True
    True
    True

    """

    if (file and data) or (not file and not data):
        raise ValueError('You must specify either file or data, but not both')
        
    if file:
        data = file.read()

    if not data[0] == '>':
        raise ValueError('Misformatted FASTA {}'.format(data))

    for seq_data in data[1:].split('>'):
        all_lines = seq_data.split('\n')
        ident = all_lines[0]
        seq = ''.join(all_lines[1:])
        yield FASTASequence(sequence=seq,identifier=ident)
        

def writeFASTA(file, *seqs):
    """Write an arbitray amount of sequences to an open writable file object.

    The sequences in *seqs* will be converted to ``FASTASequence`` objects
    first, and then printed using the ``write`` method.

    The result is a valid FASTA-formatted file.

    >>> import sys
    >>> from tigerlily.sequences import NucleicSequence
    >>> writeFASTA(sys.stdout, NucleicSequence('ATTTCGAT'))
    >Unknown
    ATTTCGAT
    """

    for seq in seqs:
        seq.convert(FASTASequence).write(file)
    # Yup. That simple.
            
        
