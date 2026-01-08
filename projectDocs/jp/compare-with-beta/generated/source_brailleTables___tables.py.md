# Diff for: `source\brailleTables\__tables.py`

**Source**: `F:\nvda\gh\beta\source\brailleTables\__tables.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\brailleTables\__tables.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\brailleTables\\__tables.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleTables\\__tables.py"
index 8b81c60..88880a6 100644
--- "a/F:\\nvda\\gh\\beta\\source\\brailleTables\\__tables.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleTables\\__tables.py"
@@ -7,7 +7,7 @@
 Note that importing this module for the first time will add all tables to the internal table store.
 """
 
-from . import addTable
+from . import addTable, TableSource
 
 # Translators: The name of a braille table displayed in the
 # braille settings dialog.
@@ -321,7 +321,6 @@
 	# braille settings dialog.
 	_("Japanese (Kantenji) literary braille"),
 	input=False,
-	outputForLangs={"ja"},
 )
 addTable(
 	"ja-rokutenkanji.utb",
@@ -329,6 +328,19 @@
 	# braille settings dialog.
 	_("Japanese (Rokuten Kanji) Braille"),
 )
+# BEGIN JP PATCH (Japanese 6 dot computer braille as default for Japanese)
+# Translators: The name of a braille table displayed in the
+# braille settings dialog.
+addTable(
+	"ja-jp-comp6.utb",
+	# Translators: The name of a braille table displayed in the
+	# braille settings dialog.
+	_("Japanese 6 dot computer braille"),
+	contracted=True,
+	source=TableSource.BUILTIN_JP,
+	outputForLangs={"ja"},
+)
+# END JP PATCH
 # Translators: The name of a braille table displayed in the
 # braille settings dialog.
 addTable("ka-in-g1.utb", _("Kannada grade 1"), inputForLangs={"kn"}, outputForLangs={"kn"})

```