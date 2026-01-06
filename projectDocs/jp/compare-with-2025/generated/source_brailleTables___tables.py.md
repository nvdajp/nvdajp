# Diff for: `source\brailleTables\__tables.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\brailleTables\__tables.py`  
**Current**: `F:\nvda\gh\alphajp\source\brailleTables\__tables.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\brailleTables\\__tables.py" "b/F:\\nvda\\gh\\alphajp\\source\\brailleTables\\__tables.py"
index 4a1d40b472..649716aaa1 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\brailleTables\\__tables.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\brailleTables\\__tables.py"
@@ -318,8 +318,14 @@
 	# braille settings dialog.
 	_("Japanese (Kantenji) literary braille"),
 	input=False,
-	outputForLangs={"ja"},
 )
+addTable(
+	"ja-rokutenkanji.utb",
+	# Translators: The name of a braille table displayed in the
+	# braille settings dialog.
+	_("Japanese (Rokuten Kanji) Braille"),
+)
+# BEGIN JP PATCH (Japanese 6 dot computer braille as default for Japanese)
 # Translators: The name of a braille table displayed in the
 # braille settings dialog.
 addTable(
@@ -329,7 +335,9 @@
 	_("Japanese 6 dot computer braille"),
 	contracted=True,
 	source=TableSource.BUILTIN_JP,
+	outputForLangs={"ja"},
 )
+# END JP PATCH
 # Translators: The name of a braille table displayed in the
 # braille settings dialog.
 addTable("ka-in-g1.utb", _("Kannada grade 1"), inputForLangs={"kn"}, outputForLangs={"kn"})

```