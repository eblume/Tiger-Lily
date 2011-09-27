# test_tests.py - A test of the unit testing framework
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

"""A somewhat frivolous class that tests the ability to test.

This test was used to bootstrap the testing system. It isn't a comprehensive
test of the testing system (which is unfortunate as that might actually be
useful), but it should catch the more glaring - and likely - issues in a bad
testing environment. Such failures won't occur as usual test failures but
rather will occur as runtime exceptions that crash the entire testing suite.

It also serves as an example for unit testing modules in general.
"""

import unittest

class TestTesting(unittest.TestCase):

    def setUp(self):
        self.shared_resource = ""

    def tearDown(self):
        self.shared_resource = None

    def test_assertEqual(self):
        self.assertEqual('1','1')
        self.assertEqual(None,None)
        self.assertEqual(1,1)
        self.assertEqual([2,3],[2,3])

        self.assertNotEqual('1','2')
        self.assertNotEqual(None,True)
        self.assertNotEqual(1,2)
        self.assertNotEqual([2,3],[3,2])

    def test_assertRaises(self):
        with self.assertRaises(ValueError):
            raise ValueError('yay')

        
