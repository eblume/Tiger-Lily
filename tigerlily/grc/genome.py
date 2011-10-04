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
import hashlib
import os
import tempfile

from tigerlily.sequences import parseFASTA, NucleicSequence
from tigerlily.utility.download import ConsoleDownloader, make_filename
from tigerlily.utility.archive import Archive

SUPPORTED_ASSEMBLIES = {
    #format: (url, md5 hashcode)
    'hg19' : ('http://hgdownload.cse.ucsc.edu/goldenPath/hg19/bigZips/'
             'chromFa.tar.gz', 'ec3c974949f87e6c88795c17985141d3'),
    'hg18' : ('http://hgdownload.cse.ucsc.edu/goldenPath/hg18/bigZips/'
             'chromFa.zip', '7fc7f751134f3800f646118e39f9991d'),
    'hg17' : ('http://hgdownload.cse.ucsc.edu/goldenPath/hg17/bigZips/'
             'chromFa.zip', None),
    'hg16' : ('http://hgdownload.cse.ucsc.edu/goldenPath/hg16/bigZips/'
             'chromFa.zip', None),
    'hg15' : ('http://hgdownload.cse.ucsc.edu/goldenPath/hg15/bigZips/'
             'chromFa.zip', None),
    'test1': ('file://{}'.format(
                os.path.join(
                    os.path.dirname(os.path.abspath(__file__)),
                    'test_assemblies',
                    'test1.tar.gz'),
             ), '58795cc5f72ffacf5c403a13da1d59e9'),
    'test_biopython': ('http://biopython.org/DIST/biopython-1.58.tar.gz', None),
}

DEFAULT_ASSEMBLY = 'h19'

class GRCGenome:
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
        self._archive = None
    
    def sequences(self):
        """Generates each sequence in the genome as a FASTASequence

        >>> from tigerlily.sequences import PolymerSequence
        >>> refgen = GRCGenome.download('test1')
        >>> for seq in refgen.sequences():
        ...     isinstance(seq,PolymerSequence)
        True
        True
        True
        """
        if self._archive is None:
            raise ValueError('Empty reference genome, no archive loaded')

        for fasta_file in self._archive.getfasta():
            for seq in  parseFASTA(file=fasta_file):
                yield seq
            

    @classmethod
    def download(cls,name=DEFAULT_ASSEMBLY,store=False,silent=True):
        """Download a reference genome of the given name, and return a GRCGenome

        Fetches the named reference assembly (default is DEFAULT_ASSEMBLY) from
        the web, and creates a new GRCGenome object to handle it.

        If store is False (default), the data will be kept in a temporary file,
        and will be destroyed as soon as the object is released. If True,
        the entire assembly will be saved in the current
        directory - ValueError will be raised if this file seems to already
        exist. The resulting file will have the '.assembly' suffix, and may be
        either a .zip, a .tar, a .tar.gz, or a .tar.bz2 file. See 
        ``tigerlily.utility.archive.Archive`` for more information.
        If store is a string, it will be assumed to be a path to a
        directory (trailing slash optional) in which the .tar.gz archive should
        be stored. (Again, ValueError will be raised if the file already
        exists.) If necessary, any intermiediate directories will be created.

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
        >>> os.path.isfile('test1.assembly')
        True
        >>> os.unlink('test1.assembly')

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

        if store and store is True:
            filename = make_filename(name='{}.assembly'.format(name))
        elif store:
            name,dir = os.path.split(store)
            filename = make_filename(name=name,dir=dir,makedirs=True)
        else:
            temp = tempfile.NamedTemporaryFile()
            filename = temp.name
            
        client.retrieve(url[0], filename=filename, silent=silent)
        if url[1] != None:
            infile = open(filename,'rb')
            content = infile.read()
            infile.close()
            md5 = hashlib.md5(content).hexdigest()
            if md5 == url[1]:
                return GRCGenome.load_archive(Archive(filepath=filename))
            else:
                return GRCGenome.download(name,store,silent)
        else:
            return GRCGenome.load_archive(Archive(filepath=filename))
        
    @classmethod
    def load(cls,filename):
        """Load the file given by filename as an ``Archive`` of a ref genome.

        >>> import os
        >>> refgen = GRCGenome.download('test1',store=True)
        >>> os.path.isfile('test1.assembly')
        True
        >>> refgen2 = GRCGenome.load('test1.assembly')
        >>> for seq1,seq2 in zip(refgen.sequences(),refgen2.sequences()):
        ...     seq1.sequence == seq2.sequence
        True
        True
        True
        >>> os.unlink('test1.assembly')
        """
        return cls.load_archive(Archive(filepath=filename))

    @classmethod
    def load_archive(cls,archive):
        """Load the given ``tigerlily.utility.archive.Archive`` object as a
        reference genome assembly.
        """
        newgrc = GRCGenome()
        newgrc._archive = archive
        return newgrc
            
        
        
