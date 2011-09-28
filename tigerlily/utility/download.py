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
import time
import math
import subprocess
import tempfile


class ConsoleDownloader(urllib.request.FancyURLopener):
    """Class which provides an interface to download URLs in a console
    environment. This may be interactive and have verbose status messages,
    or alternately supports a silent non-interactive mode.
    """

    def retrieve(self, url, filename=None, silent=False, **kwargs):
        """Wrapper for ``urllib.request.URLopener.retrieve``.

        If *silent* is left as False, a status message will be printed to
        the console informing the user of the progress on the file download.

        ***kwargs* will be passed to ``urllib.request.URLopener.retrieve``,
        but please do not specify either ``'url'``, ``'filename'``, 
        or ``'reporthook'``
        as those values are provided by this function. As of this writing,
        this leaves only ``'data'`` as an extra argument to specify in
        ***kwargs*.

        A helper function, ``make_filename``, has been provided in this
        module to assist in creating filenames - see its documentation for
        further information.

        This function returns a tuple ``(filename, headers)`` as per the
        documentation given in ``urllib.request.URLopener.retrieve``.
        """
        hook = None if silent else self._make_reporthook()
        if not silent:
            print('Downloading',url)
            print('Sending file request...')
        return super().retrieve(url,filename=filename, reporthook=hook,**kwargs)
        
    def _make_reporthook(self):
        """Create a reporting function for a console download."""
        start_download_time = time.time()
        def _reporthook(block_count,block_size,total_size):
            """Closure that prints the report each time a block is downloaded.

            This closure uses control sequences to attempt to erase the previous
            message, thus giving the illusion of a constantly updating progress
            bar.
            """
            elapsed_download_time = time.time() - start_download_time
            received_bytes = block_count * block_size

            if block_count % 8 == 0:
                return

            if total_size > 0:
                remaining_bytes = total_size - received_bytes
                seconds_per_byte = elapsed_download_time / received_bytes
                remaining_time = remaining_bytes * seconds_per_byte
                if remaining_time < 0:
                    # It means we're basically done anyway (last byte)
                    remaining_time = elapsed_download_time
                total_time = total_size * seconds_per_byte

                show_hours = total_time > 3600

                print("\033[F\033[K{elp} | {tot} : {prog: <30} | {rem} "
                      "({i}K / {t}K)".format(
                    elp = _convert_time(elapsed_download_time,show_hours),
                    tot = _convert_time(total_time,show_hours),
                    prog = '='*math.floor(30*(received_bytes/total_size)),
                    rem = _convert_time(remaining_time,show_hours),
                    i = math.ceil(received_bytes / 1024),
                    t = math.ceil(total_size / 1024),
                ))

            else:
                # We don't know how big the file is, so... yeah
                print('\033[F\033[KRecieved: {} bytes'.format(
                      received_bytes))
        return _reporthook


def _convert_time(seconds,show_hours=False):
    """Create a string form of the duration of the seconds given.

    >>> _convert_time(61)
    '01:01'
    >>> _convert_time(2)
    '00:02'
    >>> _convert_time(120)
    '02:00'
    >>> _convert_time(60*2)
    '02:00'
    >>> _convert_time(60*2-1)
    '01:59'
    >>> _convert_time(60*900)
    '900:00'
    >>> _convert_time(60*60*3+5, show_hours=True)
    '03:00:05'
    >>> _convert_time(60*60*200 + 60*61 + 17, show_hours=True)
    '201:01:17'
    """
    if show_hours:
        hours = math.floor(seconds/3600)
        seconds -= 3600 * hours
        minutes = math.floor(seconds/60)
        seconds -= 60 * minutes
        seconds = math.floor(seconds)
        return '{hh:02}:{mm:02}:{ss:02}'.format(
            hh=hours, mm=minutes, ss=seconds,
        )
    else:
        minutes = math.floor(seconds/60)
        seconds -= 60 * minutes
        seconds = math.floor(seconds)
        return '{mm:02}:{ss:02}'.format(mm=minutes,ss=seconds)


def make_filename(name=None,dir=None, makedirs=False, overwrite=False):
    """Return (or create) a complete file path, optionally creating directories.

    *name* will be the name of the file created, irrespective of (and not
    including) the directory path that will contain the file. If left as
    ``None``, a randomly generated file name will be chosen in the directory.

    *dir* will be the directory in which *name* is created. If left as
    ``None``, the current working directory is used.

    If the directory structure that will contain *name* does not exist,
    EnvironmentError will be raised. This behavior can be surpressed by
    enabling *makedirs*, in which case the necessary folders will be created.

    If the resulting filepath already exists, EnvironmentError will be raised.
    This behaior can be surpressed by enabling *overwrite*, which will simpy
    return the filepath as generated (which would generally cause the file
    to be overwritten, depending on what the caller uses the path for.)
    """
    
    if dir is None:
        dir = os.getcwd()

    if not os.path.isdir(dir) and makedirs:
        #os.makedirs(os.path.dirname(dir), exist_ok=True)
        # Unfortunately the above line of code doesn't seem to work as it
        # doesn't honor exist_ok. We should probably submit a bug to the python
        # team.
        # 
        # for now, let's just use a shell command - an ugly kludge but oh well.
        subprocess.check_call(['mkdir','-p',dir])
    elif not os.path.isdir(dir):
        raise EnvironmentError('Download directory {} does not exist'.format(
                               dir))

    if name is None:
        filename = tempfile.mktemp(prefix='unknown_resource',
                                   dir=dir)
    else:
        filename = os.path.join(dir,name)

    if os.path.isfile(filename):
        if not overwrite:
            raise EnvironmentError('Download file {} already exists'.format(
                                   filename))
    return filename
        

