# Diff for: `source\textUtils\uniscribe.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\textUtils\uniscribe.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\textUtils\uniscribe.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\textUtils\\uniscribe.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\textUtils\\uniscribe.py"
index f6b1ed5..9080849 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\textUtils\\uniscribe.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\textUtils\\uniscribe.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2024 NV Access Limited, Leonard de Ruijter
+# Copyright (C) 2024-2025 NV Access Limited, Leonard de Ruijter
 
 """Wrapper functions for NVDAHelper uniscribe functions."""
 
@@ -20,23 +20,19 @@ def splitAtCharacterBoundaries(text: str) -> Generator[str, None, None]:
 		raise RuntimeError("NVDAHelper not initialized")
 	if not text:
 		return
-	# uniscribe does some strange things
-	# when you give it a string with not more than two alphanumeric chars in a row.
-	# Inject two alphanumeric characters at the end to fix this
-	uniscribeText = text + "xx"
-	buffer = ctypes.create_unicode_buffer(uniscribeText)
+	buffer = ctypes.create_unicode_buffer(text)
 	textLength = len(buffer) - 1  # Length without terminating NULL character
 	offsetsCount = ctypes.c_int()
-	offsets = (ctypes.c_int * textLength)()
+	offsets = (ctypes.c_int * (textLength + 1))()
 	if not NVDAHelper.localLib.calculateCharacterBoundaries(
 		buffer,
 		textLength,
-		ctypes.byref(offsets),
+		offsets,
 		ctypes.byref(offsetsCount),
 	):
 		raise RuntimeError("NVDAHelper calculateCharacterBoundaries failed")
 	# Get the end offsets of the characters we need.
-	calculatedOffsets = offsets[1 : (offsetsCount.value - 1)]
+	calculatedOffsets = offsets[1 : offsetsCount.value]
 	start = 0
 	for end in calculatedOffsets:
 		yield buffer[start:end]

```