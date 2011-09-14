# amino.py - Support for qminoacid sequences (proteins)
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

import re

from tigerlily.sequences.sequence import PolymerSequence

class AminoSequence(PolymerSequence):
    """PolymerSequence for aminoacid sequences (e.g. protein sequences).

    Each member of the sequence must be one of ABCDEFGHIKLMNOPQRSTUVWYZX*-
    """
    
    def __init__(self,sequence,identifier=None):
        pass

    @property
    def sequence(self):
        pass

    @property
    def identifier(self):
        pass

    def _format(self):
        raise NotImplementedError('Attempt to format a genomic sequence. '
                                  'Try casting to another sequence type first.')
    def write(self,file):
        raise NotImplementedError('Attempt to write a genomic sequence. '
                                  'Try casting to another sequence type first.')

