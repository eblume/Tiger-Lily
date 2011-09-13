# fixedtree.py - Fixed-width substring tree index for genomic sequences.
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

from .index import GroupIndex


class FixedTree(GroupIndex):

    # TODO - document, test cases, then implement
    
    def __init__(self, sequence_group, width):
        pass

    def __contains__(self, sequence, **kwargs):
        return len(self.alignments(sequence, **kwargs)) > 0

    def alignments(self, sequence, mismatches=0,
            maximum_alignments=None,
            best_alignment=False,
        ):
        pass
