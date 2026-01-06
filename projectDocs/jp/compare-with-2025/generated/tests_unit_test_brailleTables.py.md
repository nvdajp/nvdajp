# Diff for: `tests\unit\test_brailleTables.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\tests\unit\test_brailleTables.py`  
**Current**: `F:\nvda\gh\alphajp\tests\unit\test_brailleTables.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_brailleTables.py" "b/F:\\nvda\\gh\\alphajp\\tests\\unit\\test_brailleTables.py"
index abb7be4ceb..2a687265b5 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\unit\\test_brailleTables.py"
+++ "b/F:\\nvda\\gh\\alphajp\\tests\\unit\\test_brailleTables.py"
@@ -18,17 +18,15 @@ def test_tableExistence(self):
 		"""Tests whether all defined tables exist."""
 		tables = brailleTables.listTables()
 		for table in tables:
-			tables_dir = brailleTables.TABLES_DIR
-			if table.displayName in (
-				"Japanese 6 dot computer braille",
-				"Japanese 6 dot with UEB grade 2",
-				"Japanese 6 dot with English (U.S.) grade 2",
-				"Japanese 6 dot kanji braille",
-			):
-				tables_dir = brailleTables.TABLES_DIR_JP
+			# BEGIN JP PATCH (Support TABLES_DIR_JP for Japanese tables)
+			if table.source == brailleTables.TableSource.BUILTIN_JP:
+				tableDir = brailleTables.TABLES_DIR_JP
+			else:
+				tableDir = brailleTables._tablesDirs.get(table.source, brailleTables.TABLES_DIR)
+			# END JP PATCH
 			self.assertTrue(
-				os.path.isfile(os.path.join(tables_dir, table.fileName)),
-				msg="{table} table not found".format(table=table.displayName),
+				os.path.isfile(os.path.join(tableDir, table.fileName)),
+				msg="{table} table not found in {dir}".format(table=table.displayName, dir=tableDir),
 			)
 
 	def test_renamedTableExistence(self):

```