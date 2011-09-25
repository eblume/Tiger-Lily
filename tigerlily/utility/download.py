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


class ConsoleDownloader(urllib.request.FancyURLopener):
    """Class which provides an interface to download URLs in a console
    environment. This may be interactive and have verbose status messages,
    or alternately supports a silent non-interactive mode.
    """

    def retrieve(self, url, filename=None, silent=False, makedirs=False,
                 overwrite=False, **kwargs):
        """Wrapper for ``urllib.request.URLopener.retrieve``.

        Retrieves the contents of ``url`` and places it in a filepath 
        calculated from url, filename, makedirs, and overwrite
        (see ``get_dest``).

        If ``silent`` is set to ``False``, a status message indicator for the
        download will be displayed for remote resources.

        ``kwargs`` can be any argument that will be passed to 
        ``urllib.request.URLopener.retrieve``, but please do not specify either
        ``url``, ``filename``, or ``reporthook`` to avoid conflicting with
        arguents given by this function. At the time of this writing, the
        only option would be ``data``.
        """
        filepath = get_dest(url,dest=filename,makedirs=makedirs,
                            overwrite=overwrite)
        hook = None if silent else self._make_reporthook()
        if not silent:
            print('Downloading',url)
            print('Sending file request...')
        return super().retrieve(url,filename=filepath,reporthook=hook,**kwargs)
        
    def _make_reporthook(self):
        """Create a reporting function for a console download."""
        start_download_time = time.time()
        def _reporthook(block_count,block_size,total_size):
            elapsed_download_time = time.time() - start_download_time
            received_bytes = block_count * block_size

            if block_count == 0 or block_count % 8 == 0:
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
    """Create a string form of the duration of the seconds given."""
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

def get_dest(url,dest=None,makedirs=False, overwrite=False):
    """Return (or create) a complete file path including file name for the
    given url.

    By default, the filepath will be the basename of the url inside of the
    current working directory.

    If ``dest`` is specified as a folder, the filepath will be the basename
    of the url inside of ``dest``. If ``dest`` is specified as a complete
    filepath, it will be the returned filepath.

    If ``makedirs`` is left as ``False`` (the default), then if the resulting
    filepath contains directories that do not exist EnvironmentError will be
    raised. Otherwise, if ``makedirs`` is ``True``, the directories will be
    created.

    If ``overwrite`` is left as ``False``, EnvironmentError
    will be raised if the
    filepath already exists. Otherwise the file will be overwritten.
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
        

    if os.path.isfile(dest) and not overwrite:
        raise EnvironmentError('File with name {} already exists'.format(
                               dest))

    if makedirs:
        try:
            os.makedirs(os.path.dirname(dest),exist_ok = True)
        except OSError as err:
            # Even though exist_ok is specified there is some weird thing where
            # OSError can still be raised, particularly when tempfile is being
            # used. Wonder why?
            pass
    elif not os.path.isdir(os.path.dirname(dest)):
        raise EnvironmentError('Destination folder {} does not exist'
                               .format(os.path.dirname(dest)))

    return dest


