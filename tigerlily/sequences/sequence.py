#!/usr/bin/env python3
# sequence.py
# Abstraction between sequence formats and sequence data.
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

"""Module providing an abstraction of nucleic or amino acid polymer sequences.
"""


import abc
import collections
import textwrap


class PolymerSequence(metaclass=abc.ABCMeta):
    """Abstract base class for representing genomic sequences.

    See the documentation for this module for examples on using this class.
    """

    @abc.abstractmethod
    def __init__(self,sequence=None,identifier=None):
        """All subclasses of PolymerSequence must have an initializer which
        accepts AT LEAST the keyword arguments 'sequence' and 'identifier'.
        Note that the contract requires that these arguments be supported
        if they are passed... it doesn't specify that there needs to be
        support for if they AREN'T passed. In other words, you may make
        these arguments mandatory or positional.
        
        There is no specification on what the subclass must do with these
        data, although the usual response would be to store them in such
        a way that they can be accessed by the sequence and identifier
        property.
        """
        raise NotImplementedError('Attempt to call abstract method `__init__`')
    
    def __str__(self):
        "Return the sequence for the PolymerSequence by giving the sequence."
        return self.sequence

    @abc.abstractproperty
    def sequence(self):
        """Return a str object representing the sequence."""
        raise NotImplementedError('Attempt to call abstract method `sequence`')

    @abc.abstractproperty
    def identifier(self):
        """Return a str object identifying the sequence.

        Ideally this will come straight from the underlying source data (e.g.
        the header row on FASTA sequences), however, some data sources have
        no given identifier. In this case it is better to give SOME sort of
        contextualizing identifier than to give up and use a placeholder like
        'Unknown'. An example would be to return the line number the sequence
        occured on, or the file that the sequence was contained in, or the
        date and time the sequence was processed, etc.

        If all else fails and you can't identify the sequence properly, just
        use 'return super()'. Currently this will return the string 'Unknown'.
        """
        return 'Unknown' # Use if all else fails. :)

    def convert(self,to_type):
        """Return this sequence as an instance of to_type.

        This can be useful in changing a sequence from one format to another.
        For this purpose, see format()

        No checking is made to ensure that to_type is a subclass of
        PolymerSequence, but it would probably be bad to pass in a type that
        isn't a PolymerSequence type.
        """
        return to_type(sequence=self.sequence,identifier=self.identifier)
    
    def format(self,to_type=None):
        """Return a string representing this sequence in the perscribed format.

        The last character of the format is gaurunteed to be a newline.

        To return this string in the format that the Sequence is already in,
        you may omit to_type.
        """

        if to_type is None:
            return self._format()
        else:
            return self.convert(to_type)._format()

    @abc.abstractmethod
    def _format(self):
        """Return a string representing this sequence in THIS format.

        For example, for FASTA, this would be a FASTA entry complete with
        a header row and the sequence split in to 80-character-wide lines.
        """
        raise NotImplementedError('Attempt to call abstract method `_format`')

    @abc.abstractmethod
    def write(self,file):
        """Write the formatted output of this sequence in to the file.
        
        For some formats this function may not make sense (such as for
        tile-and-cycle based outputs like Illumina's BCL format), and
        may return NotImplementedError instead.

        The result, otherwise, will be the same as if you had called:
            file.write(sequence.format())
        However, note that for some formats, calling this method is
        considerably faster than using .format(), particularly for large
        sequences.
        """
        raise NotImplementedError('Attempt to call abstract method `write`')



class PolymerSequenceGroup(collections.Iterable,metaclass=abc.ABCMeta):
    """Abstract base class for representing groups of genomic sequences.

    This could be used for any purpose you like, but was originally intended
    for use when the underlying format implies a grouping of PolymerSequence
    objects, such as in the FASTA format.
    """

    @abc.abstractmethod
    def __iter__(self):
        "Return each PolymerSequence object contained wtihin this group in turn."
        raise NotImplementedError('Attempt to call abstract method `__iter__`')

    @abc.abstractmethod
    def __len__(self):
        """Return the number of PolymerSequence objects contained."""
        raise NotImplementedError('Attempt to call abstract method `__len__`')



##### FASTA IMPLEMENTATION ############
# 
# Keep in mind that other formats can and probably should be created in their
# own modules. The FASTA implementation is included inside of this file for
# two reasons:
#   1) It makes doctest testing much simpler
#   2) Developers looking to extend PolymerSequence will have an example in
#      this file.
#

class FASTASequence(PolymerSequence):
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
        self._sequence = sequence
        self._identifier = identifier
    
    @property
    def sequence(self):
        return self._sequence

    @property
    def identifier(self):
        return self._identifier

    def _format(self):
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
        
        *: OK, the performance will be mostly identical, it's just that the
           memory footprint should be much smaller.
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

        file may point to a file-like object from which the source data will
        be read. data may point to a string in which the same will be done.

        If both file and data are set, ValueError will be raised.

        Note that this formatter uses the NCBI definition of the FASTA format,
        which you can find at this URL:
            http://blast.ncbi.nlm.nih.gov/blastcgihelp.shtml
        However, no checking is done to make sure that the sequence is composed
        of valid bases - that's between you and your end use case. Importantly,
        the NCBI definition does not allow for comments and mandates '>' as the
        decleration row's prefix, which is honored here.

        Example:

        >>> data = ">seq1\nLCLYTHGIGRN\n>seq2\nVALAGVHLTFLHETGSNN"
        >>> seqs = FASTA(data=data)
        >>> len(seqs)
        2

        We can then iterate over the FASTASequence sequences in this group:

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
    
        You'll just have to trust me that the output is consistent, and that
        it only differs from data in terms of superficial formatting.

        """

        for seq in self:
            seq.write(file)

    def _load(self,data):
        # TODO - performance optimization? This might be VERY slow on large sets
        self._sequences = []

        if data[0] != '>':
            raise ValueError('Improperly formatted data')

        for entry in data[1:].split('>'):
            all_lines = entry.split('\n')
            ident = all_lines[0]
            seq = ''.join(all_lines[1:])
            self._sequences.append(FASTASequence(sequence=seq,identifier=ident))
            
        


if __name__ == "__main__":
    import doctest
    doctest.testmod(verbose=True)
