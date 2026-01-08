# Diff for: `tests\unit\test_brailleTables.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\tests\unit\test_brailleTables.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\unit\test_brailleTables.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_brailleTables.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_brailleTables.py"
index 44b1310..2a68726 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_brailleTables.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_brailleTables.py"
@@ -2,61 +2,35 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2018-2025 NV Access Limited, Babbage B.V., Leonard de Ruijter
+# Copyright (C) 2018-2019 NV Access Limited, Babbage B.V.
 
 """Unit tests for the brailleTables module."""
 
 import unittest
 import brailleTables
-import louis
-import louisHelper
 import os.path
 
 
-class TestBrailleTables(unittest.TestCase):
+class TestFBrailleTables(unittest.TestCase):
 	"""Tests for braille table files and their existence."""
 
 	def test_tableExistence(self):
 		"""Tests whether all defined tables exist."""
 		tables = brailleTables.listTables()
 		for table in tables:
-			with self.subTest(table=table.fileName):
+			# BEGIN JP PATCH (Support TABLES_DIR_JP for Japanese tables)
+			if table.source == brailleTables.TableSource.BUILTIN_JP:
+				tableDir = brailleTables.TABLES_DIR_JP
+			else:
+				tableDir = brailleTables._tablesDirs.get(table.source, brailleTables.TABLES_DIR)
+			# END JP PATCH
 			self.assertTrue(
-					os.path.isfile(os.path.join(brailleTables.TABLES_DIR, table.fileName)),
-					msg="{table} table not found".format(table=table.displayName),
+				os.path.isfile(os.path.join(tableDir, table.fileName)),
+				msg="{table} table not found in {dir}".format(table=table.displayName, dir=tableDir),
 			)
 
 	def test_renamedTableExistence(self):
 		"""Tests whether all defined renamed tables are part of the actual list of tables."""
 		tableNames = [table.fileName for table in brailleTables.listTables()]
 		for name in brailleTables.RENAMED_TABLES.values():
-			with self.subTest(name=name):
 			self.assertIn(name, tableNames)
-
-
-class TestTranslate(unittest.TestCase):
-	"""Ensures that all tables can be used for translation."""
-
-	def test_translate(self):
-		"""Tests whether all tables can be used for translation."""
-		tables = brailleTables.listTables()
-		for table in tables:
-			if not table.output:
-				continue
-			with self.subTest(table=table.fileName):
-				try:
-					louisHelper.translate([table.fileName, "braille-patterns.cti"], "test")
-				except Exception as e:
-					self.fail(f"Translation failed for {table.displayName}: {e}")
-
-	def test_backtranslate(self):
-		"""Tests whether all tables can be used for back-translation."""
-		tables = brailleTables.listTables()
-		for table in tables:
-			if not table.input:
-				continue
-			with self.subTest(table=table.fileName):
-				try:
-					louis.backTranslate([table.fileName, "braille-patterns.cti"], "⠞⠑⠎⠞")
-				except Exception as e:
-					self.fail(f"Back-translation failed for {table.displayName}: {e}")

```