# Diff for: `source\brailleTables\__tables.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\brailleTables\__tables.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\brailleTables\__tables.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\brailleTables\\__tables.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleTables\\__tables.py"
index 4a1d40b..88880a6 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\brailleTables\\__tables.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleTables\\__tables.py"
@@ -157,6 +157,9 @@
 addTable("en-GB-g2.ctb", _("English (U.K.) grade 2"), contracted=True)
 # Translators: The name of a braille table displayed in the
 # braille settings dialog.
+addTable("en-g3.ctb", _("English grade 3"), contracted=True, input=False)
+# Translators: The name of a braille table displayed in the
+# braille settings dialog.
 addTable("en-nabcc.utb", _("English North American Braille Computer Code"))
 # Translators: The name of a braille table displayed in the
 # braille settings dialog.
@@ -318,8 +321,14 @@
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
@@ -329,7 +338,9 @@
 	_("Japanese 6 dot computer braille"),
 	contracted=True,
 	source=TableSource.BUILTIN_JP,
+	outputForLangs={"ja"},
 )
+# END JP PATCH
 # Translators: The name of a braille table displayed in the
 # braille settings dialog.
 addTable("ka-in-g1.utb", _("Kannada grade 1"), inputForLangs={"kn"}, outputForLangs={"kn"})
@@ -377,6 +388,9 @@
 addTable("Lv-Lv-g1.utb", _("Latvian grade 1"))
 # Translators: The name of a braille table displayed in the
 # braille settings dialog.
+addTable("mk-g1.utb", _("Macedonian grade 1"))
+# Translators: The name of a braille table displayed in the
+# braille settings dialog.
 addTable("ml-in-g1.utb", _("Malayalam grade 1"))
 # Translators: The name of a braille table displayed in the
 # braille settings dialog.

```