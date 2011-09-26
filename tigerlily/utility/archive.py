# archive.py - Tools for extracting resources from archive files
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

"""Tools for extracting files from common archive formats like .tar.gz and .zip.

Additionally includes helper functions to extract common sequence formats from
these archives without actually 'inflating' the archive on the disk.
"""

import abc
import gzip
import bz2
import zipfile
import tarfile
import re

class Archive(metaclass=abc.ABCMeta):
    """Common abstract base class for all ``Archive`` objects.

    Users will generally want to use this class if they wish to load data
    from an archive with any valid archive format. Generally speaking, this
    class will detect the correct subclass of archivers to load (tarfile,
    zipfile, etc.) However the user may also wish to explicitly use one of the
    subclasses.

    Descendents can (and should) implement a class variable called
    ``file_name_regex`` which is a regular expression that will be called as
    ``re.match(<Class>.file_name_regex,filename)``. This will allow users to
    simply call the constructor of ``Archive`` and, hopefully, the correct
    format will be deduced from the file name. If this fails then the
    constructor for every descendent will be tried one-by-one until one of
    them accepts the file without error.

    Descendents can also define the class variable
    ``disable_fallback_detection`` and set it to ``True`` to prevent the loader
    from being tried during the fallback auto-format-detection procedure. This
    is useful if for some reason the given loader will likely accept any input
    even if it is not a valid object of that format.

    Finally, if no format is detected, ValueError will be raised.
    """

    @abc.abstractmethod
    def __init__(self, filepath=None, data=None):
        """Default constructor for generic ``Archive`` objects.
    
        The user must set either *filepath* or *data* but not both. *filepath*
        is a ``str`` representing a path to the file that will be
        loaded. *data* is a ``bytes`` object which is the contents of the
        given archive file. If possible use *filepath* and not *data* to avoid
        inefficiency, as some archive formats require a file object and so a
        memory-based file object will be created for some *data* archives.

        The auto-detection method used by this function is described in the
        class documentation for ``Archive``, see above.

        Descendents **MUST** implement at least the *filepath* and *data*
        constructors in order for auto-detection to work. If a descendent
        determines that it can't process the file for any reason, ValueError
        must be raised. All additional arguments to the constructor must be
        optional.
        """
        pass

    @abc.abstractproperty
    def singlemember(self):
        """True if the format allows only a single member, otherwise False.

        Descendents must return True or False, with True indicating that
        the given file format **implies** only a single member. Note that
        file formats which support multiple members but happen to only contain
        a single member must return False.
        """
        pass

    @abc.abstractmethod
    def getnames(self):
        """Return a list of the names of every member in the archive.

        These names will be suitable for passing to the getmember() function,
        but their explicit type is not specified.
        """
        pass

    @abc.abstractmethod
    def getmembers(self):
        """Generate every member of the archive as a file-like object."""
        pass

    @abc.abstractmethod
    def getmember(self,name):
        """Open the given member as a file-like object."""
        pass

    @abc.abstractmethod
    def getfasta(self):
        """Generate every member of the archive that looks like it is a
        FASTA file as a file-like object.
        """
        pass

    @abc.abstractmethod
    def getnofasta(self):
        """Generate every member of the archive that does NOT look like it is a
        FASTA file as a file-like object.
        """

