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
			# BEGIN JP PATCH (Support TABLES_DIR_JP for Japanese tables)
			if table.source == brailleTables.TableSource.BUILTIN_JP:
				tableDir = brailleTables.TABLES_DIR_JP
			else:
				tableDir = brailleTables._tablesDirs.get(table.source, brailleTables.TABLES_DIR)
			# END JP PATCH
			self.assertTrue(
				os.path.isfile(os.path.join(tableDir, table.fileName)),
				msg="{table} table not found in {dir}".format(table=table.displayName, dir=tableDir),
			)

	def test_renamedTableExistence(self):
		"""Tests whether all defined renamed tables are part of the actual list of tables."""
		tableNames = [table.fileName for table in brailleTables.listTables()]
		for name in brailleTables.RENAMED_TABLES.values():
			self.assertIn(name, tableNames)
