# Diff for: `source\tones.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\tones.py`  
**Current**: `F:\nvda\gh\alphajp\source\tones.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\tones.py" "b/F:\\nvda\\gh\\alphajp\\source\\tones.py"
index 9d1dacd2f4..69a0d4700a 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\tones.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\tones.py"
@@ -81,7 +81,7 @@ def beep(
 		return
 	if not player:
 		return
-	from NVDAHelper import generateBeep
+	from NVDAHelper.localLib import generateBeep
 
 	bufSize = generateBeep(None, hz, length, left, right)
 	buf = create_string_buffer(bufSize)

```