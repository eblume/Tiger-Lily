# download_test.py - unit tests for download.py
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

"""This module provides unit tests for the ``tigerlily.utility.download``
module.

As with all unit test modules, the tests it contains can be executed in many
ways, but most easily by going to the project root dir and executing
``python3 setup.py nosetests``.
"""

import unittest
import tempfile
import os
import shutil

import tigerlily.utility.download as dl


class ConsoleDownloaderTests(unittest.TestCase):
    """Test harness for ``tigerlily.utility.download.ConsoleDownloader`` class.
    """

    def setUp(self):
        """Create the testing environment"""
        self.test_dir = tempfile.mkdtemp()
        self.orig_dir = os.getcwd()
        os.chdir(self.test_dir)

    def tearDown(self):
        """Remove the testing environment"""
        os.chdir(self.orig_dir)
        shutil.rmtree(self.test_dir)
    
    def test_local(self):
        """download.py: Test 'downloading' local resources."""
        client = dl.ConsoleDownloader()

        # Download this test file as 'thisfile.py'

        filename, headers = client.retrieve(__file__,
            filename=os.path.join(self.test_dir,'thisfile.py'),
            silent=True
        )

        orig_contents = open(__file__).read()
        dl_contents = open(filename).read()

        self.assertEqual(orig_contents,dl_contents)

    def test_remote_open(self):
        """download.py: Test the Downloader.open() method"""
        client = dl.ConsoleDownloader()

        filobj = client.open('http://www.google.com')
        content = filobj.read().decode(encoding='utf-8')
        self.assertTrue('Search the world' in content)

    def test_remote_retrieve(self):
        """download.py: Test the Downloader.retrieve() method"""
        client = dl.ConsoleDownloader()

        filename,headers = client.retrieve('http://www.google.com',silent=True)
        self.assertTrue(os.path.isfile(filename))

        contents = open(filename).read()

        self.assertTrue('Search the world' in contents)


        # Store to a specified name as well
        filename,headers = client.retrieve('http://www.google.com',
            filename='rr_test.html', silent=True)
        self.assertTrue(os.path.isfile(filename))
        self.assertTrue(os.path.isfile('rr_test.html'))
        self.assertEqual(os.path.basename(filename),'rr_test.html')
            
    def test_make_filename(self):
        """download.py: Test directory structure creation from make_filename""" 
        
        dest = dl.make_filename(name='full_path.html', dir=self.test_dir)
        self.assertEqual(dest,os.path.join(self.test_dir,'full_path.html'))

        long_new_path = os.path.join(self.test_dir,'alpha','beta','gamma') 

        # First the negative test - assert it fails to create new directories
        with self.assertRaises(EnvironmentError):
            dest = dl.make_filename(name='foobar.html', dir=long_new_path)

        self.assertFalse(os.path.isdir(long_new_path))

        # Then the positive - assert it succeeds when makedirs is on

        dest = dl.make_filename(name='foobar.html', dir=long_new_path,
                                makedirs=True)
        self.assertTrue(os.path.isdir(long_new_path))
        
        
