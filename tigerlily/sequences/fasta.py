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

Only a subset of the NCBI specification for FASTA is supported. In particular,
the sequences allowed in a NucleicSequence or an AminoSequence are allowed.

This implementation honors the NCBI FASTA requirement that sequences not
contain any comments (only a single identifier line is allowed), and that '>'
is the only valid identifier character (not ';').
"""

import re


from tigerlily.sequences.sequence import FormattedSequence, PolymerSequenceGroup

class FASTASequence(FormattedSequence):
    """Container for a single FASTA Sequence.

    Do not use this object. Instead, use the FASTA object, which subclasses
    PolymerSequenceGroup. The FASTA format is intrinsically a set, so most of
    the parsing logic is left in the FASTA object.

    Nothing is *stopping* you from using this object, but you will probably
    find that it doesn't do very much work for you.
    """
    
    # The FASTA format often specified a maximum line width. This is that.
    MAX_LINE_WIDTH = 79

    # Required functions

    def __init__(self,sequence,identifier):
        # Note that for FASTA, unlike other formats, an identifier is REQUIRED

        # Check the sequence to make sure it conforms to NCBI-reduced
        allowed_nucleic_chars = 'ATGCUN'
        allowed_amino_chars = 'ACDEFGHIKLMNPQRSTVWYX*'
        all_allowed = ''.join(set(
            allowed_nucleic_chars + allowed_nucleic_chars.lower() + 
            allowed_amino_chars + allowed_amino_chars.lower()))

        if not re.match(r'[{}]+'.format(all_allowed),sequence):
            raise ValueError('FASTA sequence contains bad chars'
                             .format(sequence))

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
        return ">{id}\n{seq}".format(
            id=self.identifier,
            seq=['{}\n'.format(line) for line in textwrap.wrap(
                                                    self.sequence,
                                                    width=self.MAX_LINE_WIDTH,
                                                 )]
        )

    def write(self,file):
        """Write this FASTA sequence to the opened file object.

        Note that this function has the same result as writing the output of
        .format(). However, this function will outperform* that approach for
        large sequences (such as reference genomes stored in FASTA format),
        because this function doesn't store the entire sequence in memory a
        second time like .format() does (for text wrapping purposes).
        
        *: *OK, the performance will be mostly identical, it's just that the
           memory footprint should be much smaller.*
        """
    
        seq = self.sequence
        if not seq:
            raise ValueError('Empty or invalid sequence: "{}"'.format(seq))
        
        file.write('>{}\n'.format(self.identifier))

        for i in range(0,len(seq),self.MAX_LINE_WIDTH):
            file.write('{}\n'.format(seq[i:i+self.MAX_LINE_WIDTH]))



class FASTA(PolymerSequenceGroup):
    def __init__(self,file=None,data=None):
        r"""Load a FASTA set either from the given source.

        *file* may point to a file-like object from which the source data will
        be read. *data* may point to a ``str`` in which the same will be done.

        If both *file* and *data* are set, ValueError will be raised. You may
        create an empty ``FASTA`` object if you like by specifying neither.

        Note that this formatter uses the NCBI definition of the FASTA format,
        which you can find at this URL:
            http://blast.ncbi.nlm.nih.gov/blastcgihelp.shtml
        However, no checking is done to make sure that the sequence is composed
        of valid bases - that's between you and your end use case.

        Importantly, the NCBI definition does not allow for comments and
        mandates '>' as the decleration row's prefix, which is honored here.

        Example:

        >>> data = ">seq1\nLCLYTHGIGRN\n>seq2\nVALAGVHLTFLHETGSNN"
        >>> seqs = FASTA(data=data)
        >>> len(seqs)
        2

        We can then iterate over the ``FASTASequence`` sequences in this group:

        >>> for seq in seqs:
        ...     isinstance(seq,FASTASequence)
        ...     seq.identifier,seq.sequence
        ...
        True
        ('seq1', 'LCLYTHGIGRN')
        True
        ('seq2', 'VALAGVHLTFLHETGSNN')

        Here is some proof that the various inheritance schemes are working:

        >>> isinstance(seqs,FASTA)
        True
        >>> isinstance(seqs,PolymerSequenceGroup)
        True
        >>> issubclass(FASTA,PolymerSequenceGroup)
        True
        """
        if file and data:
            raise ValueError('Only specify file or data, not both')

        self._sequences = []

        if file:
            data = file.read().decode('utf-8')

        if data:
            self._load(data)

    @classmethod
    def load_sequences(cls,*sequences):
        """Create a new FASTA object from a list of arbitrary sequences.

        >>> from tigerlily.sequences import RawSequence,NucleicSequence
        >>> seq1 = RawSequence('AACGGTTACGATCAGGACTACGGGAGGAGAGA')
        >>> seq2 = NucleicSequence('ACGGACTTACCAGGACTACGGACTCAGACG')
        >>> fasta = FASTA.load_sequences(seq1,seq2)
        >>> len(fasta)
        2
        """
        newfasta = FASTA()
        for seq in sequences:
            newfasta._sequences.append(seq.convert(FASTASequence))
        return newfasta

    def __iter__(self):
        for seq in self._sequences:
            yield seq

    def __len__(self):
        return len(self._sequences)

    def write(self,file):
        """Write this FASTA group to a file, producing a conforming FASTA file.

        >>> data = r'''>SEQUENCE_1
        ... MTEITAAMVKELRESTGAGMMDCKNALSETNGDFDKAVQLLREKGLGKAAKKADRLAAEG
        ... LVSVKVSDDFTIAAMRPSYLSYEDLDMTFVENEYKALVAELEKENEERRRLKDPNKPEHK
        ... IPQFASRKQLSDAILKEAEEKIKEELKAQGKPEKIWDNIIPGKMNSFIADNSQLDSKLTL
        ... MGQFYVMDDKKTVEQVIAEKEKEFGGKIKIVEFICFEVGEGLEKKTEDFAAEVAAQL
        ... >SEQUENCE_2
        ... SATVSEINSETDFVAKNDQFIALTKDTTAHIQSNSLQSVEELHSSTINGVKFEEYLKSQI
        ... ATIGENLVVRRFATLKAGANGVVNGYIHTNGRVGVVIAAACDSAEVASKSRDLLRQICMH
        ... '''
        
        We could use the file-based loading initializer for FASTA, but let's
        just leave it as a string for simplicity.

        >>> seqs = FASTA(data=data)
        >>> len(seqs)
        2
        
        Now we write the sequences out to a buffer.

        >>> import io
        >>> buffer = io.StringIO()
        >>> seqs.write(buffer)
    
        You'll just have to trust that the output is consistent, and that
        it only differs from data in terms of superficial formatting.

        """

        for seq in self:
            seq.write(file)

    def _load(self,data):
        if data[0] != '>':
            raise ValueError('Improperly formatted data')

        for entry in data[1:].split('>'):
            all_lines = entry.split('\n')
            ident = all_lines[0]
            seq = ''.join(all_lines[1:])
            self._sequences.append(FASTASequence(sequence=seq,identifier=ident))
            
        
