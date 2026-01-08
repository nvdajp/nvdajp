# Diff for: `source\keyLabels.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\keyLabels.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\keyLabels.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\keyLabels.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\keyLabels.py"
index 1ea4912..56bc16d 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\keyLabels.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\keyLabels.py"
@@ -167,6 +167,8 @@
 	"break": _("break"),
 	# Translators: This is the name of a key on the keyboard.
 	"tab": pgettext("keyLabel", "tab"),
+	# BEGIN JP PATCH
+	# nvdajp: IME key labels
 	# Translators: This is the name of a key on the keyboard.
 	"imenonconvert": _("IME non convert"),
 	# Translators: This is the name of a key on the keyboard.
@@ -179,6 +181,7 @@
 	"imechangestatus3": _("toggle input method"),
 	# Translators: This is the name of a key on the keyboard.
 	"pause": _("pause"),
+	# END JP PATCH
 }
 
 

```