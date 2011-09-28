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

import zipfile
import tarfile
import re
import io

class Archive:
    """Common interface for extracting file objects from common archive formats.

    When initializing, you must specify either *filepath* or *data* but not
    both. In general, prefer to use *filepath* as it prevents using a layer of
    abstraction to provide a file-like object to the underlying archive formats,
    but either will work more or less equivalently.

    The format of the archive will be automatically detected without using the
    file name or extension.

    Currently supported formats are (again, recall that extensions may be
    arbitrary):
    .tar
    .tar.gz
    .tar.bz2
    .zip

    In all cases the archive may contain one file or many files. If the 
    archive has a nested folder structure, this structure will be ignored and
    all file members will be scanned without regard to their placement in the
    arhcive's folder structure.
    """

    def __init__(self, filepath=None, data=None):
        pass

    def getnames(self):
        """Return a list of the names of every member in the archive.

        These names will be suitable for passing to the getmember() function,
        but their explicit type is not specified.
        """
        pass

    def getmembers(self):
        """Generate every member of the archive as a file-like object."""
        pass

    def getmember(self,name):
        """Open the given member as a file-like object."""
        pass

    def getfasta(self):
        """Generate every member of the archive that looks like it is a
        FASTA file as a file-like object.
        """
        pass

    def getnofasta(self):
        """Generate every member of the archive that does NOT look like it is a
        FASTA file as a file-like object.
        """
        pass

