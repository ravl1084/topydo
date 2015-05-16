# Topydo - A todo.txt client written in Python.
# Copyright (C) 2015 Bram Schoenmakers <me@bramschoenmakers.nl>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import codecs
import re
import sys
import unittest

from test.CommandTest import CommandTest
from topydo.lib.IcalCommand import IcalCommand
from test.TestFacilities import load_file_to_todolist

class IcalCommandTest(CommandTest):
    def setUp(self):
        super(IcalCommandTest, self).setUp()
        self.todolist = load_file_to_todolist("test/data/ListCommandTest.txt")

    @unittest.skipIf((sys.version_info.major, sys.version_info.minor) == (3, 2), "icalendar is not supported for Python 3.2")
    def test_ical(self):
        def replace_ical_tags(p_text):
            # replace identifiers with dots, since they're random.
            result = re.sub(r'\bical:....\b', 'ical:....', p_text)
            result = re.sub(r'\bUID:....\b', 'UID:....', result)

            return result

        command = IcalCommand([""], self.todolist, self.out, self.error)
        command.execute()

        self.assertTrue(self.todolist.is_dirty())

        icaltext = ""
        with codecs.open('test/data/ListCommandTest.ics', 'r', encoding='utf-8') as ical:
            icaltext = ical.read()

        self.assertEqual(replace_ical_tags(self.output), replace_ical_tags(icaltext))
        self.assertEqual(self.errors, "")

    @unittest.skipUnless((sys.version_info.major, sys.version_info.minor) == (3,2), "icalendar is not supported for Python 3.2")
    def test_ical_python32(self):
        """
        Test case for Python 3.2 where icalendar is not supported.
        """
        command = IcalCommand([""], self.todolist, self.out, self.error)
        command.execute()

        self.assertFalse(self.todolist.is_dirty())
        self.assertEqual(self.output, '')
        self.assertEqual(self.errors, "icalendar is not supported in this Python version.\n")

    def test_help(self):
        command = IcalCommand(["help"], self.todolist, self.out, self.error)
        command.execute()

        self.assertEqual(self.output, "")
        self.assertEqual(self.errors, command.usage() + "\n\n" + command.help() + "\n")

if __name__ == '__main__':
    unittest.main()
