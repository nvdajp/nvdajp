# Diff for: `tests\unit\test_louisHelper.py`

**Source**: `F:\nvda\gh\beta\tests\unit\test_louisHelper.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\unit\test_louisHelper.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_louisHelper.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_louisHelper.py"
index c988443..691a9db 100644
--- "a/F:\\nvda\\gh\\beta\\tests\\unit\\test_louisHelper.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\unit\\test_louisHelper.py"
@@ -20,9 +20,15 @@ def test_tableResolvingInternal(self):
 		"""Test whether our custom braille table resolver can resolve all defined tables."""
 		tables = brailleTables.listTables()
 		for table in tables:
+			# BEGIN JP PATCH (Support TABLES_DIR_JP for Japanese tables)
+			if table.source == brailleTables.TableSource.BUILTIN_JP:
+				expectedDir = brailleTables.TABLES_DIR_JP
+			else:
+				expectedDir = brailleTables._tablesDirs.get(table.source, brailleTables.TABLES_DIR)
+			# END JP PATCH
 			self.assertEqual(
 				list(louisHelper._resolveTableInner(tables=[table.fileName])),
-				[os.path.join(brailleTables.TABLES_DIR, table.fileName)],
+				[os.path.join(expectedDir, table.fileName)],
 			)
 
 	def test_internalTableIncludedInternal(self):

```