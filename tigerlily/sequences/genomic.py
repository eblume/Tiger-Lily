# genomic.py - Support for genomic (chromosomal DNA) sequences
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
import string

from tigerlily.sequences.sequence import PolymerSequence
from tigerlily.sequences.mixed import MixedSequenceGroup


COMPLEMENT_TRANS = str.maketrans('atgcATGC','tacgTACG')

class NucleicSequence(PolymerSequence):
    """Container for nucleic (chromosomal DNA) sequences.
    
    In general this is not an 'input' or 'output' format, but rather an
    internal format that constrains the sequence to a certain set of
    allowed characters in the sequence.

    The set of characters allowed is the following:
        ATGC
    If a sequence is converted to a NucleicSequence and doesn't fit that
    set, ValueError will be raised.

    NucleicSequence objects do not have a valid write() method, nor do
    they have a valid format() method. (Instead they will raise
    NotImplementedError.)

    >>> from . import raw
    >>> seqdata = 'CTAGCATACTCACAGT'
    >>> seq = raw.RawSequence(seqdata)
    >>> nucleic = seq.convert(NucleicSequence)
    >>> nucleic.sequence
    'CTAGCATACTCACAGT'

    An example showing that NucleicSequence objects can be instantiated
    directly.

    >>> seq2 = NucleicSequence(seqdata)
    >>> seq2.sequence == nucleic.sequence
    True
    
    An example where the constraint fails:
    
    >>> seq = raw.RawSequence('CAGTTACTm')
    >>> nucleic = seq.convert(NucleicSequence)
    Traceback (most recent call last):
        ...
    ValueError: Invalid nucleic sequence format
    """

    
    def __init__(self,sequence,identifier=None):
        if not re.match(r'[ATGC]+$',sequence):
            raise ValueError('Invalid nucleic sequence format')

        self._sequence = sequence
        self._identifier = identifier

    @property
    def sequence(self):
        return self._sequence

    @property
    def identifier(self):
        """The identifier for this read.

        If the identifier was unspecified, a placeholder will be used that
        includes a hash value checksum of the sequence.

        >>> seq = NucleicSequence('GGGACTG')
        >>> seq.identifier
        'UnknownSeq_7276410743868358753'
        >>> seq = NucleicSequence('AGGCTA')
        >>> seq.identifier
        'UnknownSeq_-8092672563224726703'
        >>> seq = NucleicSequence('AGGCTA',identifier='chr1')
        >>> seq.identifier
        'chr1'
        """
        # TODO - don't use hash(), use something smarter.
        if self._identifier is None:
            return 'UnknownSeq_{}'.format(hash(self._sequence))
        return self._identifier

    def reverse(self):
        """Return a new sequence that is the reverse of this sequence.
        
        >>> seq1 = NucleicSequence('AATGCC')
        >>> rseq1 = seq1.reverse()
        >>> rseq1.sequence
        'CCGTAA'
        >>> seq2 = rseq1.reverse()
        >>> seq2.sequence == seq1.sequence
        True

        """
        return NucleicSequence(self._sequence[::-1],identifier=self._identifier)

    def complement(self):
        """Return the purine<->pyrimidine complement of the sequence
        as a new sequence.

        >>> seq1 = NucleicSequence('AATGCC')
        >>> cseq1 = seq1.complement()
        >>> cseq1.sequence
        'TTACGG'
        >>> seq2 = cseq1.complement()
        >>> seq2.sequence == seq1.sequence
        True
        """
        return NucleicSequence(self._sequence.translate(COMPLEMENT_TRANS),  
                               identifier=self._identifier)

    def reverse_complement(self):
        """Return the reverse complement of the sequence as a new sequence.

        Has the same result as sequence.reverse().complement(), but slightly
        more efficient.

        >>> seq1 = NucleicSequence('AATGCC')
        >>> rcseq1 = seq1.reverse_complement()
        >>> rcseq1.sequence
        'GGCATT'
        >>> seq2 = rcseq1.reverse_complement()
        >>> seq2.sequence == seq1.sequence
        True
        >>> rcseq1.sequence == seq1.reverse().complement().sequence
        True
        """
        return NucleicSequence(reverse_complement(self.sequence),
                               identifier=self._identifier)

    def translate(self,reading_frame=1,use_control_codes=False):
        """Convert this NucleicSequence to a corresponding AminoSequence.

        Conversion is performed by taking each codon and replacing it with
        the corresponding amino acid. In the nucleic sequence, thymine (T)
        is automatically converted to uracil (U). In biological terms,
        translate() assumes that the NucleicSequence object's sequence is
        the coding sequence (and not the template). Incidentally, to get
        the coding sequence of a template, just call
        template.reverse_complement().

        reading_frame is either 1, 2, or 3, and corresponds to the 1-based
        offset into the sequence from which to begin collecting codons. In
        other words, reading_frame=1 (the default) will start from the first
        base in the sequence, and reading_frame=2 from the 2nd, and so on.
        Higher values are allowed and will start further in to the sequence by
        skipping codons that would otherwise have been in the reading frame.

        use_control_codes is a flag which, when True, enables an alternative
        processing algorithm. The new algorithm is like the first one (including
        the reading_frame), but after processing has finished the following
        constraint is placed upon the strand: all amino acids prior to and
        including the first Methionine (M/AUG) will be removed, and all amino
        acids after the first STOP codon (*/UAA,UGA,UAG) will be removed. If
        no Methionine is detected, ValueError will be raised. (It is not
        necessary for there to be a STOP codon.)

        >>> nucleic = NucleicSequence('CA TGG TAT GTT TTG GGT TTA GAA ACG T')
        >>> amino = nucleic.translate()
        >>> amino.sequence
        'HGMFWV*KR'

        We can also specify a reading_frame even though it will mean that the
        given input sequence doesn't cleanly subdivide in to codons - this is
        not an error.

        >>> amino = nucleic.translate(reading_frame=2)
        >>> amino.sequence
        'MVCFGFRN'

        Here is an example using use_control_codes mode.

        >>> amino = nucleic.translate(use_control_codes=True)
        'FWV'
        >>> amino = nucleic.translate(use_control_codes=True,reading_frame=2)
        'VCFGFRN'
        >>> amino = nucleic.translate(use_control_codes=True,reading_frame=3)
        Traceback (most recent call last):
            ...
        ValueError: No Methionine found in translated nucleic sequence
    
        """
        # TODO - EXTREMELY IMPORTANT - above, I claim that if the user
        # has a NucleicSequence that is equivalent to the template strand,
        # then the user can simply call template.reverse_complement() to get
        # the coding sequence. Is this true, or do you simply call
        # template.complement()?
        pass

class AminoSequence(PolymerSequence):
    """PolymerSequence for aminoacid sequences (e.g. protein sequences).

    Each member of the sequence must be one of ABCDEFGHIKLMNOPQRSTUVWYZX*
    """
    
    def __init__(self,sequence,identifier=None):
        """Create a new AminoSequence, and validates the sequence.

        If the sequence is not composed of characters that are in
        ABCDEFGHIKLMNOPQRSTUVWYZX* then ValueError will be raised.

        This notation is similar to the NCBI amino acid query sequence
        format, but does not allow for the gap indicator (-) nor masked
        acids (lowercase variant).
        
        >>> seq = AminoSequence('ADKKYMZZB*EE')
        >>> seq2 = AminoSequence('ADKKYMZZB*EE',identifier='seq2')
        >>> seq3 = AminoSequence('ADKKYMZZB*EEJ')
        Traceback (most recent call last):
            ...
        ValueError: invalid character in AminoSequence
        """
        if not re.match(r'[ABCDEFGHIKLMNOPQRSTUVWYZX*]+$',sequence):
            raise ValueError('invalid character in AminoSequence')

        self._sequence = sequence
        self._identifier = identifier

    @property
    def sequence(self):
        return self._sequence

    @property
    def identifier(self):
        """Returns the identifier, if any.

        If the identifier has not been explicitly set, the default identifier
        will be used instead.
        """
        if self._identifier is None:
            return super().identifier
        return self._identifier
        
def reverse_complement(sequence):
    """Compute the reverse complement of the input string.

    Input is assumed to be a string that could be the sequence of a
    NucleicSequence. 

    >>> reverse_complement('ACGGTC')
    'GACCGT'
    >>> reverse_complement('GACCGT')
    'ACGGTC'
    """
    return sequence[::-1].translate(COMPLEMENT_TRANS)

def createNucleicSequenceGroup(*sequences):
    r"""Convert any group of sequences in to a nucleic MixedSequence group.

    >>> from tigerlily.sequences.raw import Raw
    >>> sequences = Raw(data='AGTACGTATTTCAT\nTTCATACGACTAC\n')
    >>> len(sequences)
    2
    >>> nucleic = createNucleicSequenceGroup(*[s for s in sequences])
    >>> len(nucleic)
    2
    >>> for seq in nucleic:
    ...     isinstance(seq,NucleicSequence)
    ...
    True
    True

    """

    new_group = MixedSequenceGroup()
    
    for sequence in sequences:
        new_group.add(sequence.convert(NucleicSequence))

    return new_group


#### Genetic Code matrix   ####

# GENETIC_CODE_AMINO - the genetic code, going from amino acid to codon
GENETIC_CODE_AMINO = {
    'A': {'GCU','GCC','GCA','GCG'},
    'R': {'CGU','CGC','CGA','CGG','AGA','AGG'},
    'N': {'AAU','AAC'},
    'D': {'GAU','GAC'},
    'C': {'UGU','UGC'},
    'Q': {'CAA','CAG'},
    'E': {'GAA','GAG'},
    'G': {'GGU','GGC','GGA','GGG'},
    'H': {'CAU','CAC'},
    'I': {'AUU','AUC','AUA'},
    'M': {'AUG'},
    'L': {'UUA','UUG','CUU','CUC','CUA','CUG'},
    'K': {'AAA','AAG'},
    'F': {'UUU','UUC'},
    'P': {'CCU','CCC','CCA','CCG'},
    'S': {'UCU','UCC','UCA','UCG','AGU','AGC'},
    'T': {'ACU','ACC','ACA','ACG'},
    'W': {'UGG'},
    'Y': {'UAU','UAC'},
    'V': {'GUU','GUC','GUA','GUG'},
    '*': {'UAA','UGA','UAG'}
}

def _generate_inverse_gc_matrix(matrix):
    """Private initializer to create the inverse of the genetic code matrix.

    Importantly, this initializer will also detect inconsistancies in the above
    matrix and raise ValueError if either of the following two occur:
        1. A given codon is listed twice in any two amino acids' groups.
        2. Some possible codon is not listed in the above matrix.

    In general, please do not call this function yourself. It will be called
    once when the module is imported.
    """
    inv_matrix = {}

    for amino in GENETIC_CODE_AMINO:
        for codon in GENETIC_CODE_AMINO[amino]:
            if codon in inv_matrix:
                raise ValueError('Codon {} is listed at least twice in '
                                 'GENETIC_CODE_AMINO'.format(codon))
            inv_matrix[codon] = amino

    from itertools import combinations_with_replacement as cPr

    for codon in cPr('AUGC',3):
        codon = ''.join(codon)
        if not codon in inv_matrix:
            raise ValueError('Codon {} is not listed in '
                             'GENETIC_CODE_ADMINO'.format(codon))

    return inv_matrix

# GENETIC_CODE_CODON - the genetic code, going from codon to amino acid
GENETIC_CODE_CODON = _generate_inverse_gc_matrix(GENETIC_CODE_AMINO)

