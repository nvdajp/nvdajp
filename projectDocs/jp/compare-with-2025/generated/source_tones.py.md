# Diff for: `source\tones.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\tones.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\tones.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\tones.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\tones.py"
index 9d1dacd..69a0d47 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\tones.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\tones.py"
@@ -81,7 +81,7 @@ def beep(
 		return
 	if not player:
 		return
-	from NVDAHelper import generateBeep
+	from NVDAHelper.localLib import generateBeep
 
 	bufSize = generateBeep(None, hz, length, left, right)
 	buf = create_string_buffer(bufSize)

```