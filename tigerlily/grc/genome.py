# genome.py - Download and manage 
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

"""tigerlily.ncbi - functions and extensions for common GRC-related tasks.

The members of this package generally interact with online or downloaded
resources from the members of the GRC (Genome Reference Consortium) and
other online resource entities such as NCBI, Sanger Institute, and the
UCSC Genome Browser.
"""

import abc

class ReferenceGenome(metaclass=abc.ABCMeta):
    """Abstract base class for all Genome objects.

    ReferenceGenome objects represent an underlying file or data structure that
    encodes a Reference Genome assembly (often called simply an 'assembly',
    although in Tiger Lily they will normally use the full name Reference Genome
    to help clarity).

    ReferenceGenome objects convert such file structures in to sequence groups,
    normally of the type tigerlily.sequences.MixedGroup, with the contained
    sequences being tigerlily.sequences.NucleicSequence - one per each
    assembly unit (nominally chromosomes, but often with other meta-units 
    included), with the identifier set appropriately.
    """
    
    @abc.abstractmethod
    def sequences(self):
        """Return a PolymerSequenceGroup representing this Genome.

        Normally this will be a MixedSequenceGroup with NucleicSequence members.
        """
        raise NotImplementedError('attempt to call abstract method sequences()')

class GRCGenome(ReferenceGenome):
    """Fetch, store, load, parse, and extract sequences from a GCR ref assembly

    NCBI has released many top-quality reference genomes. As of late 2010, these
    assemblies are produced under the brand of the GRC - the Genome Reference
    Consortium. The UCSC Genome Browser mirrors each of these assemblies in
    such a way that makes it very conveniant to download and extract data that
    is useful to Tiger Lily.

    This class provides an interface to automatically download, store, load,
    parse, and extract sequences from the UCSC Genome Browser's copies of the
    GRC reference genomes.

    Support for different assemblies will be added manually to this class. For
    a list of supported assemblies by their name, see
    GRCGenome.SUPPORTED_ASSEMBLIES . The default (most current) assembly will
    be stored in GRCGenome.DEFAULT_ASSEMBLY
    """

    # Default assembly goes FIRST
    SUPPORTED_ASSEMBLIES = ['hg19']
    # TODO: hg18-hg15 use .zip. This should still be supportable.
    DEFAULT_ASSEMBLY = SUPPORTED_ASSEMBLIES[0]
    
    def sequences(self):
        """Created a MixedSequenceGroup of the FASTA sequences from this ref.
        """
        pass

    @classmethod
    def download(cls,name=DEFAULT_ASSEMBLY,store=False,silent=True):
        """Download a reference genome of the given name, and return a GRCGenome

        Fetches the named reference assembly (default is
        GRCGenome.DEFAULT_ASSEMBLY) from the UCSC Genome Browser, and creates
        a new GRCGenome object to handle it.

        If store is False (default), the data will be kept entirely in memory,
        and will be destroyed as soon as the object is released. If True,
        the .tar.gz of the entire assembly will be saved in the current
        directory - ValueError will be raised if this file seems to already
        exist. If store is a string, it will be assumed to be a path to a
        directory (trailing slash optional) in which the .tar.gz archive should
        be stored. (Again, ValueError will be raised if the file already
        exists.)

        If silent is False, status messages will be printed using print() to 
        keep the user informed of the progress. This is usually very important
        in command line applications as the reference archives are about 900 MB
        in size and may take minutes or hours to download depending on the
        internet connection.

        Because of the large size of these files, it is highly recommended that
        the store option be set. Please do not use Tiger Lily to abuse the
        UCSC Genome Browser group's generosity in hosting these large files to
        the general public.
        """
        # IMPORTANT: make sure to take advantage of the md5sum file
        pass

    @classmethod
    def load(cls,path):
        """Load the given .tar.gz archive file as a downloaded GRC Genome.

        It is expected that this file will be named <assembly>.tar.gz and that
        <assembly> is one of GRCGenome.SUPPORTED_ASSEMBLES - if not,
        ValueError will be raised.
        """
