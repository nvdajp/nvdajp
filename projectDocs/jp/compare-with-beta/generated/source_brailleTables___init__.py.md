# Diff for: `source\brailleTables\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\brailleTables\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\brailleTables\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\brailleTables\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleTables\\__init__.py"
index 9ffba14..efcfc8c 100644
--- "a/F:\\nvda\\gh\\beta\\source\\brailleTables\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleTables\\__init__.py"
@@ -22,6 +22,9 @@
 TABLES_DIR = os.path.join(globalVars.appDir, "louis", "tables")
 """The directory in which liblouis braille tables are located."""
 
+TABLES_DIR_JP = os.path.join(globalVars.appDir)
+"""The directory in which Japanese braille tables are located."""
+
 DEFAULT_TABLE = "en-ueb-g1.ctb"
 """The default braille table."""
 
@@ -29,6 +32,8 @@
 class TableSource(StrEnum):
 	BUILTIN = "builtin"
 	"""The name of the builtin table source"""
+	BUILTIN_JP = "builtin_jp"
+	"""The name of the builtin Japanese table source"""
 	SCRATCHPAD = "scratchpad"
 	"""The name of the scratchpad table source"""
 
@@ -43,6 +48,7 @@ class TableType(Enum):
 _tablesDirs = collections.ChainMap(
 	{
 		TableSource.BUILTIN: TABLES_DIR,
+		TableSource.BUILTIN_JP: TABLES_DIR_JP,
 	},
 )
 """Chainmap of directories for braille tables lookup, including custom tables."""
@@ -165,7 +171,12 @@ def listTables() -> list[BrailleTable]:
 	"""
 	return sorted(
 		_tables.values(),
-		key=lambda table: (table.source != TableSource.BUILTIN, strxfrm(table.displayName)),
+		# BEGIN JP PATCH
+		key=lambda table: (
+			table.source not in (TableSource.BUILTIN, TableSource.BUILTIN_JP),
+			strxfrm(table.displayName),
+		),
+		# END JP PATCH
 	)
 
 

```