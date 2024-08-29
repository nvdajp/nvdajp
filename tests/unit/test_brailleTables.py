# tests/unit/test_brailleTables.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.

"""Unit tests for the brailleTables module."""

import unittest
import brailleTables
import os.path


class TestFBrailleTables(unittest.TestCase):
	"""Tests for braille table files and their existence."""

	def test_tableExistence(self):
		"""Tests whether all defined tables exist."""
		tables = brailleTables.listTables()
		for table in tables:
			tables_dir = brailleTables.TABLES_DIR
			if table.displayName in (
				"Japanese 6 dot computer braille",
				"Japanese 6 dot with UEB grade 2",
				"Japanese 6 dot with English (U.S.) grade 2",
				"Japanese 6 dot kanji braille",
			):
				tables_dir = brailleTables.TABLES_DIR_JP
			self.assertTrue(
				os.path.isfile(os.path.join(tables_dir, table.fileName)),
				msg="{table} table not found".format(table=table.displayName)
			)

	def test_renamedTableExistence(self):
		"""Tests whether all defined renamed tables are part of the actual list of tables."""
		tableNames = [table.fileName for table in brailleTables.listTables()]
		for name in brailleTables.RENAMED_TABLES.values():
			self.assertIn(name, tableNames)
