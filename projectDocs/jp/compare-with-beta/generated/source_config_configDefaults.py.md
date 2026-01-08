# Diff for: `source\config\configDefaults.py`

**Source**: `F:\nvda\gh\beta\source\config\configDefaults.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\config\configDefaults.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\config\\configDefaults.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\configDefaults.py"
index 400f387..613e9e8 100644
--- "a/F:\\nvda\\gh\\beta\\source\\config\\configDefaults.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\config\\configDefaults.py"
@@ -27,5 +27,8 @@
 	# since they don't trigger as many false positives.
 	punc2=r"[?!]",
 	# We also check for CJK full-width punctuation marks without any extra rules.
-	cjk=r"[．！？：；]",
+	# BEGIN JP PATCH
+	# nvdajp: include Japanese period (。) in CJK punctuation marks
+	cjk=r"[．。！？：；]",
+	# END JP PATCH
 )

```