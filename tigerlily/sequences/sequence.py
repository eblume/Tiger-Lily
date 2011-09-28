# sequence.py - Abstraction between sequence formats and sequence data.
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
        """All subclasses of ``PolymerSequence`` must have an initializer which
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


class FormattedSequence(PolymerSequence,metaclass=abc.ABCMeta):
    """Abstract base class for PolymerSequence objects which can be formatted.

    Children of this class are sequences with some sort of character-encoded
    format. In particular, they support a  .format() method and a .write()
    method.
    """
    
    def format(self,to_type=None):
        """Return a string representing this sequence in the perscribed format.

        The last character of the format is gaurunteed to be a newline.

        To return this string in the format that the Sequence is already in,
        you may omit to_type.

        Note that some FormattedSequence descendants will be representing a
        binary format. These descendants can choose whether they wish to return
        a 'bytes' object instead of a string, or simply raise an exception.
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

