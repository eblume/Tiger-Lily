# download.py - Tools for downloading online resources
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

"""Tools for downloading resources from URLs with a variety of 'fancy'
interfaces (such as progressbars and login info for HTTP authentication).
"""

import urllib.request
import os
import sys

class Downloader:
    """Class which facilitates downloading of resources in scripted
    environments.

    This class will download a resource without generating any output. It is
    not asynchronous and communicates success or failure through return
    values and exceptions only. This makes it suitable for use inside of an
    environment that does not directly interact with a human (IE in a script
    or as part of a wrapping environment).
    """

    def __init__(self):
        """Create a new Downloader, including internal objects for URL access.
        """

        self.client = urllib.request.URLopener()

    def download(url,dest=None, makedirs=False):
        """Download the url, optionally to the location ``dest``.

        Returns the path to the newly created file, which is gaurunteed to
        exist unless an exception was raised.

        If ``dest`` is not specified (the default),
        the resource will be downloaded
        in to the current working directory and will be named after the
        basename of the url.

        If ``dest`` is specified and is a full file path, the file will be
        downloaded to and named as ``dest``. If ``dest`` is
        specified as a directory,
        the url will be downloaded in to that directory and named after the
        basename of the url.

        In all cases, if the final destination path already exists,
        ``EnvironmentError`` will be raised.

        If makedirs is ``True`` then the final path may contain directories
        which do not yet exist in the file system - these directories will be
        created. If makedirs is ``False`` (the default), any nonexistant
        directories in the final path will cause ``EnvironmentError`` to be
        raised.
        """
        self.client.retrieve(url,filname=self._get_dest(url,dest,makedirs))

    def _get_dest(url,dest,makedirs):
        """Helper function to generate a filepath to the destination.

        See ``Downloader.download`` in this module for further documentation.
        """
        if dest is None or not os.path.basename(dest):
            basename = os.path.basename(url)
            if not basename:
                # basename() couldn't find a suitable base name, make one up
                basename = 'unknown_resource'

            if dest:
                # We know from above that dest was set to a path (no basename)
                basepath = dest
            else:
                basepath = os.getcwd()
            
            dest = os.path.join(basepath,basename)
            

        if os.path.isfile(dest):
            raise EnvironmentError('File with name {} already exists'.format(
                                   dest))

        if makedirs:
            os.makedirs(os.path.basepath(dest))
        elif not os.path.isdir(os.path.basepath(dest)):
            raise EnvironmentError('Destination folder {} does not exist'
                                   .format(os.path.basepath(dest)))

        return dest

