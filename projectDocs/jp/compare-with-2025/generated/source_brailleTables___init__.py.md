# Diff for: `source\brailleTables\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\brailleTables\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\brailleTables\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\brailleTables\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleTables\\__init__.py"
index ffa12f4..efcfc8c 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\brailleTables\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleTables\\__init__.py"
@@ -171,10 +171,12 @@ def listTables() -> list[BrailleTable]:
 	"""
 	return sorted(
 		_tables.values(),
+		# BEGIN JP PATCH
 		key=lambda table: (
 			table.source not in (TableSource.BUILTIN, TableSource.BUILTIN_JP),
 			strxfrm(table.displayName),
 		),
+		# END JP PATCH
 	)
 
 

```