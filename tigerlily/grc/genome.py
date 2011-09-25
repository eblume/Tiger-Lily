# genome.py - Download and manage GRC reference genomes
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

import abc
import os
import tarfile
import io
import tempfile

from tigerlily.sequences import FASTA
from tigerlily.utility.download import ConsoleDownloader

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


SUPPORTED_ASSEMBLIES = {
    'hg19' : 'http://hgdownload.cse.ucsc.edu/goldenPath/hg19/bigZips/'
             'chromFa.tar.gz',
    'test1': 'file://{}'.format(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    'test_assemblies',
                    'test1.tar.gz'),
             ),
    'test_biopython': 'http://biopython.org/DIST/biopython-1.58.tar.gz',
}

DEFAULT_ASSEMBLY = 'h19'

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
    a list of supported assemblies by their name, see SUPPORTED_ASSEMBLIES .
    The default (most current) assembly will be stored in DEFAULT_ASSEMBLY

    For the convenience of faster non-networked tests, extremely small made-up
    reference genomes are provided inside of this package in a folder called
    'test_assemblies'. They can be loaded either by using the GRCGenome.load
    method (as normal), or else by using GRCGenome.download with names that
    start with 'test' (eg. 'test1', 'test2', 'testnomask', etc.).
    """

    def __init__(self):
        """Initializer for a GRCGenome object.

        Do not call this method directly. Instead, call either
        GRCGenome.download or GRCGenome.load
        """
        self._sequences = None
    
    def sequences(self):
        """Create a MixedSequenceGroup of the FASTA sequences from this ref.

        >>> from tigerlily.sequences import PolymerSequenceGroup
        >>> refgen = GRCGenome.download('test1')
        >>> seqs = refgen.sequences()
        >>> isinstance(seqs,PolymerSequenceGroup)
        True
        """
        return self._sequences

    @classmethod
    def download(cls,name=DEFAULT_ASSEMBLY,store=False,silent=True):
        """Download a reference genome of the given name, and return a GRCGenome

        Fetches the named reference assembly (default is DEFAULT_ASSEMBLY) from
        the web, and creates a new GRCGenome object to handle it.

        If store is False (default), the data will be kept in a temporary file,
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

        >>> refgen = GRCGenome.download('test1')
        >>> refgen2 = GRCGenome.download('test1',store=True)
        >>> import os
        >>> os.path.isfile('test1.tar.gz')
        True
        >>> os.unlink('test1.tar.gz')

        Only supported reference genome assemblies are allowed, otherwise
        ValueError will be raised.

        >>> GRCGenome.download('invalid')
        Traceback (most recent call last):
            ...
        ValueError: Unknown or unsupported reference genome specified
        """

        if name not in SUPPORTED_ASSEMBLIES:
            raise ValueError('Unknown or unsupported reference genome'
                             ' specified')

        url = SUPPORTED_ASSEMBLIES[name]
        client = ConsoleDownloader()

        # Generate target
        if store and store is True:
            target = '{}.tar.gz'.format(name)
        elif store:
            target = store
        else:
            temp = tempfile.NamedTemporaryFile()
            target = temp.name

        client.retrieve(url,filename=target, silent=silent, makedirs=True,
                            overwrite=True)

        # Generate buffer (file obj of target)
        if store:
            buffer = open(target,'rb')
        else:
            buffer = temp
            buffer.seek(0)

        return GRCGenome.load_tarfile(tarfile.open(
                                                   mode='r:gz',
                                                   fileobj=buffer,
                                                  ))
        
    @classmethod
    def load(cls,path):
        """Load the given .tar.gz archive file as a downloaded GRC Genome.

        It is expected that this file will be named <assembly>.tar.gz

        >>> import os
        >>> refgen = GRCGenome.download('test1',store=True)
        >>> os.path.isfile('test1.tar.gz')
        True
        >>> refgen2 = GRCGenome.load('test1.tar.gz')
        >>> len(refgen2.sequences()) == len(refgen.sequences())
        True
        >>> os.unlink('test1.tar.gz')
        """

        archive = tarfile.open(name=path,mode='r:gz')

        return GRCGenome.load_tarfile(archive)


    @classmethod
    def load_tarfile(cls,archive):
        """Given an instance of tarfile.TarFile, load it as a ref. assembly."""
        sequences = []

        for member in archive.getmembers():
            fasta = FASTA(file=archive.extractfile(member))
            for seq in fasta:
                sequences.append(seq)
        
        newgrc = GRCGenome()
        newgrc._sequences = FASTA.load_sequences(*sequences)
        return newgrc
            
        
        
