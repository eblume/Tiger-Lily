# __init__.py - Package meta file for tigerlily.sequences
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

"""tigerlily.sequences - tools for handling polynomial sequences (DNA, RNA, etc)

All sequences descend from two parent classes, ``PolymerSequence`` and
``PolymerSequenceGroup``. Another group of ``PolymerSequence`` descendents
inherit from ``FormattedSequence``, which adds support for printing or saving
the sequence to some file format.

"""

from tigerlily.sequences.sequence import ( PolymerSequence, FormattedSequence,
    PolymerSequenceGroup, 
)

from tigerlily.sequences.fasta import ( FASTA, FASTASequence)

from tigerlily.sequences.raw import ( RawSequence, Raw )

from tigerlily.sequences.mixed import ( MixedSequenceGroup)

from tigerlily.sequences.genomic import ( NucleicSequence, AminoSequence,
    createNucleicSequenceGroup, reverse_complement,
)

