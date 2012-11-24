#
# Copyright (c) 2012 by Lifted Studios.  All Rights Reserved.
#

import os
import sys

test_dir = os.path.dirname(os.path.abspath(__file__))
source_dir = os.path.dirname(test_dir)
sys.path.append(test_dir)
sys.path.append(source_dir)

import constants
import unittest
import sublime

from Exception import MissingOwnerException
from MockEdit import MockEdit
from MockView import MockView
from UpdateCopyrightCommand import UpdateCopyrightCommand

test_copyright = u"#\n# Copyright (c) 2010 by Lifted Studios.  All Rights Reserved.\n#\n"
single_owner = u"Lifted Studios"
single_owner_pattern = u"\\|(\\d+)(-\\d+)?\\|Lifted Studios\\|"
single_owner_array = [u"Lifted Studios"]
multiple_owner = [u"Lifted Studios", u"FooBar Industries"]


class TestUpdateCopyrightCommand(unittest.TestCase):
    def setUp(self):
        self.edit = MockEdit()
        self.view = MockView(test_copyright)
        self.command = UpdateCopyrightCommand(self.view)

    def test_update_single_owner_happy_path(self):
        sublime.settings.set(constants.SETTING_OWNERS, single_owner)
        self.command.run(self.edit)

    def test_get_owners_single_owner(self):
        sublime.settings.set(constants.SETTING_OWNERS, single_owner)
        owners = self.command.get_owners()

        self.assertEqual([single_owner], owners)

    def test_get_owners_single_owner_in_array(self):
        sublime.settings.set(constants.SETTING_OWNERS, single_owner_array)
        owners = self.command.get_owners()

        self.assertEqual(single_owner_array, owners)

    def test_get_owners_multiple_owners(self):
        sublime.settings.set(constants.SETTING_OWNERS, multiple_owner)
        owners = self.command.get_owners()

        self.assertEqual(multiple_owner, owners)

    def test_get_owners_no_owners_setting(self):
        sublime.settings.set(constants.SETTING_OWNERS, None)
        with self.assertRaises(MissingOwnerException):
            self.command.get_owners()

    def test_get_owners_empty_owners_list(self):
        sublime.settings.set(constants.SETTING_OWNERS, [])
        with self.assertRaises(MissingOwnerException):
            self.command.get_owners()

    def test_get_patterns_single_owner(self):
        sublime.settings.set(constants.SETTING_OWNERS, single_owner)
        patterns = self.command.get_patterns()

        self.assertEqual({single_owner_pattern: single_owner}, patterns)
