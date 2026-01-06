# Diff for: `source\brailleTables\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\brailleTables\__init__.py`  
**Current**: `F:\nvda\gh\alphajp\source\brailleTables\__init__.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\brailleTables\\__init__.py" "b/F:\\nvda\\gh\\alphajp\\source\\brailleTables\\__init__.py"
index ffa12f43d6..5ae213057e 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\brailleTables\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\brailleTables\\__init__.py"
@@ -171,10 +171,7 @@ def listTables() -> list[BrailleTable]:
 	"""
 	return sorted(
 		_tables.values(),
-		key=lambda table: (
-			table.source not in (TableSource.BUILTIN, TableSource.BUILTIN_JP),
-			strxfrm(table.displayName),
-		),
+		key=lambda table: (table.source != TableSource.BUILTIN, strxfrm(table.displayName)),
 	)
 
 

```