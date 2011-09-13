#!/usr/bin/env python3
# index.py
# Abstract interface for genomic sequence indexes supporting alignment.
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


import abc


class GroupIndex(metaclass=abc.ABCMeta):
    """Abstract base class for all genomic indexes."""
    
    @abc.abstractmethod
    def __init__(self, sequence_group, **kwargs):
        """Initialize a genomic index.

        No type checking should be performed on sequence_group by the
        implementing subclass, but in general you want sequence_group to be
        at *least* a tigerlily.sequences.PolymerSequenceGroup object. In
        practical terms you will actually probably want to use GenomicSequence
        sequences, in a MixedSequenceGroup sequence group.

        A helper method exists called 
            tigerlily.sequences.createGenomicSequenceGroup()
        which will convert any SequenceGroup in to a MixedSequenceGroup with
        only GenomicSequence objects. This is suitable for creating an index.

        As with all implementing subclasses, each subclass may add additional
        required or optional arguments to this method.
        """

        raise NotImplementedError('Attempt to call abstract method `__init__`')
    
    @abc.abstractmethod
    def __contains__(self, sequence, **kwargs):
        """Boolean check to see if the sequence is in this index in some sense.

        It is perfectly acceptable (and generally encouraged) for this function
        to be identical to:

        def __contains__(self,sequence):
            return len(self.alignments(sequence)) > 0

        However some indexes may treat this method differently. If at all
        possible, implementing subclasses should ensure that this method
        runs at least as fast as alignments(), if not faster.
        
        Like with __init__, sequence could be any PolymerSequence but will
        probably always be a GenomicSequence. 
        """
        raise NotImplementedError('Attempt to call abstract method '
                                  '`__contains__`')
    
    @abc.abstractmethod
    def alignments(self, sequence, **kwargs):
        """Gather all alignments for the given sequence. (See __contains__).

        Implementing subclasses may (and almost certainly will) provide
        additional arguments to constrain the alignment set, such as to
        allow for a certain number of mismatches or to only generate the
        closest fit, etc.

        The return value will always be a list or list-like object, with
        each item corresponding to an alignment. (The list may be empty.)
        However, each alignment's representation is *undefind*. This is
        because different indexing methods may or may not be able to
        provide the different details allowed by other indexing methods.
        Consult the implementing subclasses' documentation for the structure
        of an alignment.

        """
        raise NotImplementedError('Attempt to call abstract method '
                                  '`alignments`')


