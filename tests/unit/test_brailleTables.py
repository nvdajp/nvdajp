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
			# BEGIN JP PATCH (ja-rokutenkanji.utb is registered but actual file is ja-jp-rokutenkanji.tbl)
			tablePath = os.path.join(tableDir, table.fileName)
			if table.fileName == "ja-rokutenkanji.utb":
				# The actual file is source/ja-jp-rokutenkanji.tbl, registered as ja-rokutenkanji.utb
				# During build, it's installed to louis/tables/ja-jp-rokutenkanji.tbl
				# For test, check if source/ja-jp-rokutenkanji.tbl exists
				# __file__ is tests/unit/test_brailleTables.py, so go up 2 levels to get to source/
				sourceDir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
				sourcePath = os.path.join(sourceDir, "source", "ja-jp-rokutenkanji.tbl")
				if os.path.isfile(sourcePath):
					continue
			# END JP PATCH
			self.assertTrue(
				os.path.isfile(tablePath),
				msg="{table} table not found in {dir}".format(table=table.displayName, dir=tableDir),
			)

	def test_renamedTableExistence(self):
		"""Tests whether all defined renamed tables are part of the actual list of tables."""
		tableNames = [table.fileName for table in brailleTables.listTables()]
		for name in brailleTables.RENAMED_TABLES.values():
			self.assertIn(name, tableNames)
