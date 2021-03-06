# fixedtree.py - Fixed-width substring tree index for nucleic sequences.
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

import os
import struct
import bz2
import io

from tigerlily.index.index import GroupIndex
from tigerlily.sequences import reverse_complement
from tigerlily.utility import hamming_distance, greatest_common_prefix

class FixedTree(GroupIndex):
    def __init__(self, width, genome=None, reverse=False):
        """``FixedTree`` objects support alignment of fixed-width reads.

        *width* is the fixed width of reads that can be aligned to this index.
        It must be an integer and must be greater than 0, although for
        reasonable
        performance it should also be greater than about 20. After this index
        is created, only reads that are exactly as long as *width* may be
        aligned.

        If *genome* is set, it must be a member of
        ``tigerlily.grc.genome.GRCGenome``. The index will load every sequence
        in that genome. (You may omit this and then simply add sequences later.)

        If *reverse* is set to ``True``, then each input sequence's reverse
        complement is also processed. Alignments on these strands are reported
        with the same position and chromosome name, but with 'strand' as 
        ``False``.
        Note that the reported position of a reverse strand alignment will be
        the same position as the given sequence's reverse complement's position.

        Other than this function, you may also create a new ``FixedTree``
        object by using ``FixedTree.load()`` to load a stored index.
        """

        self.root = FixedTreeNode()
        self.width = width
        self.sequence_name_table = {}
        
        if genome:
            for sequence in genome.sequences():
                self.add_sequence(sequence, reverse)

    def store(self, filename):
        """Save the FixedTree to the file named by *filename*.

        If *filename* already exists, EnvironmentError will be raised.
        """
        if os.path.exists(filename):
            raise EnvironmentError('File {} already exists.'.format(filename))

        buffer = bz2.BZ2File(filename,mode='w')
        buffer.write(struct.pack('<II',self.width,
                                       len(self.sequence_name_table)))

        for i in sorted(self.sequence_name_table.keys()):
            ident = self.sequence_name_table[i]
            buffer.write(struct.pack('<I',len(ident)))
            buffer.write(struct.pack('<{}s'.format(len(ident)),
                ident.encode('utf-8')))

        self.root.store(buffer)

    @classmethod
    def load(cls, filename):
        """Create a new FixedTree from the named file."""

        buffer = bz2.BZ2File(filename)
        
        width, num_seqs = _unpack_buffer('<II',buffer)

        newtree = FixedTree(width)
        newtree.width=width
        
        newtree.sequence_name_table = {}
        
        for i in range(1,num_seqs+1):
            (name_len,) = _unpack_buffer('<I',buffer)
            (name,) = _unpack_buffer('<{}s'.format(name_len),buffer)
            name = name.decode('utf-8')
            newtree.sequence_name_table[i] = name

        newtree.root = FixedTreeNode.load(buffer)

        return newtree


    def add_sequence(self, sequence,reverse):
        """Add the given sequence to this index. 

        The sequence must be a NucleicSequence, and it will be split in to
        subsequences of the length specified by this index.

        If reverse is True, each individual subsequence will also be reversed.
        """
        seq = sequence.sequence
        id = self._get_id(sequence.identifier)
        for i in range(len(seq)-self.width+1):
            subseq = seq[i:i+self.width]
            # This loop will generate each overlapping subsequence
            # Keep in mind that in the common use case, this loop will be
            # executed as much as 250 million times. So, keep it light.

            alignment = (id,i,True)
            self.root.insert(subseq,alignment)

            if reverse:
                alignment = (id,i,False)
                self.root.insert(reverse_complement(subseq),alignment)

    def _get_id(self,identifier):
        """Assign a unique integer to this identifier, to be shared amongst
        all members claiming the same identifier."""
        tab = self.sequence_name_table
        val = 0
        for val in tab:
            if identifier == tab[val]:
                return val
        tab[val+1] = identifier
        return val+1

    def __contains__(self, sequence):
        """Return true if, given the arguments, the sequence is in the index.

        As with alignments(), sequence must be a string. Raises ValueError if
        the length of the sequence does not match the index width.

        The alignment is performed as if alignments() was called with all
        optional arguments left at their default.
        """
        return len(self.alignments(sequence)) > 0

    def alignments(self, sequence, mismatches=0,
            maximum_alignments=None,
            best_alignments=False,
        ):
        """Returns a list of all alignments produced by the given input.

        Retrurns a list of tuples, each tuple containing three values. They are:
            0: str - 'chromosome name'
            1: int - 'position'
            2: boolean - 'strand' (True means 'reported strand', False means
                                   'opposing strand'. Opposing strand matches
                                   do not alter the original position.)

        Each reported alignment will have a computed 'Hamming Distance' (see
        http://en.wikipedia.org/wiki/Hamming_distance ) of no greater than the
        mismatches argument. If left at 0, no actual edit distance calculations
        are performed.

        If maximum_alignments is an integer greater than 0, then only that many
        alignments will be found - after that many are found, the search ends.

        If best_alignments is True, then every possible alignment will be found
        even if maximum_alignments is set. Then, alignments are reported in
        increasing order of their edit distance from the search sequence. In
        general, this function will slow down the search considerably,
        particularly if maximum_alignments is set (since the primary benefit of
        maximim_alignments will be negated.) If left at False, no sorting is
        performed and the search can end as soon maximum_alignments has been
        reached.

        This will raise ValueError if the given sequence does not match the
        pre-specified width of the index.
        """

        if self.width != len(sequence):
            raise ValueError('aligned read is not the right width for this '
                             'index')
        
        alignments = self.root.alignments(sequence,mismatches,
            remaining_mismatches=mismatches,
            maximum_alignments= None if best_alignments else maximum_alignments,
        )

        # Sort the alignments if best_alignments is on.
        if best_alignments:
            alignments.sort(key=_extract_result_mismatch)

        # Truncate the result to maximum_alignments if not done already.
        if maximum_alignments and len(alignments) > maximum_alignments:
            alignments = alignments[:maximum_alignments]

        # Format the results for their final return
        alignments = [(self.sequence_name_table[v[1]],v[2],v[3])
                      for v in alignments]

        # And we are done!
        return alignments
        

def _extract_result_mismatch(alignment):
    "Helper function to return the mismatch value in an alignments() lookup."
    return alignment[0]
            


class FixedTreeNode:
    """Implicit tree data structure for storing a fixed read length index.

    Each node in the graph may contain alignments (although the Root node is
    gaurunteed to not store any alignments). Any input sequence that lands on
    a node with a set of alignments may report those alignments.

    Each node in the graph may contain a dictionary that maps strings to other
    nodes - these strings represent labeled edges. Moving along an edge consumes
    the corresponding prefix from the input sequence.

    Hamming distance may be used to move along an edge that doesn't exactly
    match to a prefix of the input sequence. If the Hamming distance between an
    edge and a prefix of the input sequence is less than or equal to the number
    of remaining mismatches, then travel may proceed across that edge, although
    the mismatch count is decremented by that hamming distance.

    Great care is made to ensure that the following properties are maintained in
    this structure at all times:
        * For any given node N, for all of N's edges E1, there exists no edge
          in N called E2 that is not E1 but for which E2 is an exact prefix
          of E1.
        * For any given node N, for all of N's children M, there is no way to
          re-distribute the edges between N and the M's (even by creating new
          children nodes in-between) in order to increase the length of an
          edge's label without violating the first property.
    In other words, the edges of each node are 'maximally uncommon' - they are
    chosen to be as long as possible without sharing any prefixes.

    Because of this property, we can be sure of correctness and optimality.

    Well, I'm mostly hoping about the optimality part. I haven't done the math.
    """

    def __init__(self,alignment=None):
        self.edges = {}
        self._alignments = []

        if alignment is not None:
            self._alignments.append(alignment)

    def store(self,buffer):
        """Copy this node in to *buffer*, and then recursively (but in a fixed
        order) copy the children.
        """

        # save alignments
        buffer.write(struct.pack('<I',len(self._alignments)))
        for alignment in self._alignments:
            buffer.write(struct.pack('<II?',*alignment))

        # save edges
        buffer.write(struct.pack('<I',len(self.edges)))
        for label,node in self.edges.items():
            length = len(label)
            buffer.write(struct.pack('<I',length))
            buffer.write(struct.pack('<{}s'.format(length),
                                     label.encode('utf-8')))
            node.store(buffer)

    @classmethod
    def load(cls,buffer):
        """Return a new node by reading it from buffer, recursively"""
        newnode = FixedTreeNode()        

        # load alignments
        (num_alignments,) = _unpack_buffer('<I',buffer)
        for i in range(num_alignments):
            alignment = _unpack_buffer('<II?',buffer)
            newnode._alignments.append(alignment)

        # load edges
        (num_edges,) = _unpack_buffer('<I',buffer)
        for i in range(num_edges):
            (label_len,) = _unpack_buffer('<I',buffer)
            (label,) = _unpack_buffer('<{}s'.format(label_len),buffer)
            label = label.decode('utf-8')
            newnode.edges[label] = FixedTreeNode.load(buffer)

        return newnode

    def insert(self,sequence,alignment):
        # The goal is to create the maximum possible length edge without
        # violating the rules listed in the class definition documentation.

        if not sequence:
            self._alignments.append(alignment)
            return

        for edge_label in self.edges:

            # If the given edge_label is an exact prefix, just follow the link.
            if sequence.startswith(edge_label):
                self.edges[edge_label].insert(sequence[len(edge_label):],
                                                     alignment)
                return

            # If the given edge_label shares a prefix, we have to split.
            gsc = greatest_common_prefix(edge_label,sequence)
            if gsc > 0:
                # SPLIT!!!!

                # First create the new intermediate node, and point it at the
                # current (soon to no longer be a child) node.
                old_child = self.edges[edge_label]
                new_child = FixedTreeNode()
                new_child.edges[edge_label[gsc:]] = old_child

                # Make the old node no longer be a child of the active node.
                del self.edges[edge_label]
                # Link the active node to the new intermediate node.
                self.edges[edge_label[:gsc]] = new_child

                # Start over the insertion process at the new node.
                new_child.insert(sequence[gsc:],alignment)
                return
            

        # Finally we use the catch-all - just use the rest of the sequence as
        # an edge to a leaf node.
        self.edges[sequence] = FixedTreeNode(alignment)

    def alignments(self,sequence,original_mismatches,
                   remaining_mismatches=0,maximum_alignments=None):

        if not sequence:
            return [(original_mismatches - remaining_mismatches,
                     v[0],v[1],v[2]) for v in self._alignments]

        alignments = []

        for edge_label in self.edges:
            # Perfect prefix match
            if sequence.startswith(edge_label):
                alignments += self.edges[edge_label].alignments(
                    sequence[len(edge_label):], original_mismatches,
                    remaining_mismatches = remaining_mismatches,
                    maximum_alignments = (maximum_alignments - len(alignments)
                                            if maximum_alignments else None
                                         ),
                )
                # Shortcut exit if maximum_alignments is exceeded
                if maximum_alignments and len(alignments) > maximum_alignments:
                    return alignments
                continue

            # Edit distance, if mismatches allow
            if remaining_mismatches > 0:
                hd = hamming_distance(edge_label, sequence[:len(edge_label)])
                if hd <= remaining_mismatches:
                    alignments += self.edges[edge_label].alignments(
                        sequence[len(edge_label):], original_mismatches,
                        remaining_mismatches = remaining_mismatches - hd,
                        maximum_alignments = (maximum_alignmets -
                                              len(alignments) if
                                              maximum_alignments else None
                                             ),
                    )
                    # Shortcut exit if maximum_alignments is exceeded
                    if maximum_alignments and (
                       len(alignments) > maximum_alignments):
                        return alignments
                    continue

        return alignments
        
def _unpack_buffer(format,buffer):
    """Helper function that should be in stdlib to unpack from a file-like"""
    this = struct.Struct(format)
    return this.unpack(buffer.read(this.size))
        
