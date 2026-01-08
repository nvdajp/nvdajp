# Diff for: `source\louisHelper.py`

**Source**: `F:\nvda\gh\beta\source\louisHelper.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\louisHelper.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\louisHelper.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\louisHelper.py"
index d59b673..a90d6b4 100644
--- "a/F:\\nvda\\gh\\beta\\source\\louisHelper.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\louisHelper.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2018-2025 NV Access Limited, Babbage B.V., Julien Cochuyt, Leonard de Ruijter
+# Copyright (C) 2018-2024 NV Access Limited, Babbage B.V., Julien Cochuyt, Leonard de Ruijter
 
 """Helper module to ease communication to and from liblouis."""
 
@@ -94,12 +94,8 @@ def _resolveTable(tablesList: bytes, base: bytes | None) -> int | None:
 	except LookupError:
 		log.exception()
 		return None
-	# Terminate the list of paths
-	paths.append(None)
 	if _isDebug():
-		log.debug(
-			f"Storing paths in a null terminated array of length {len(paths)} with null terminated strings",
-		)
+		log.debug(f"Storing paths in an array of {len(paths)} null terminated strings")
 	# Keeping a reference to the last returned value to ensure the returned
 	# value is not GC'ed before it is copied on liblouis' side.
 	_resolveTable._lastRes = arr = (c_char_p * len(paths))(*paths)
@@ -149,19 +145,31 @@ def terminate():
 	louis.liblouis.lou_free()
 
 
-def translate(
-	tableList: list[str],
-	inbuf: str,
-	typeform: list[int] | None = None,
-	cursorPos: int | None = None,
-	mode: int = 0,
-) -> tuple[list[int], list[int], list[int], int | None]:
+def translate(tableList, inbuf, typeform=None, cursorPos=None, mode=0):
 	"""
 	Convenience wrapper for louis.translate that:
 	* returns a list of integers instead of a string with cells, and
 	* distinguishes between cursor position 0 (cursor at first character) and None (no cursor at all)
 	"""
 	text = inbuf.replace("\0", "")
+	# nvdajp begin
+	try:
+		from synthDrivers.jtalk.translator2 import translate as jpTranslate
+	except ModuleNotFoundError:
+		log.warning("Japanese translation module not found.")
+		jpTranslate = None
+	if jpTranslate and tableList and len(tableList) > 0 and tableList[0].endswith("ja-jp-comp6.utb"):
+		log.debug(text)
+		nabcc = config.conf["braille"]["expandAtCursor"]
+		try:
+			braille, brailleToRawPos, rawToBraillePos, brailleCursorPos = jpTranslate(
+				text,
+				cursorPos=cursorPos or 0,
+				nabcc=nabcc,
+			)
+		except Exception as e:
+			raise
+	else:
 		braille, brailleToRawPos, rawToBraillePos, brailleCursorPos = louis.translate(
 			tableList,
 			text,
@@ -170,6 +178,7 @@ def translate(
 			cursorPos=cursorPos or 0,
 			mode=mode,
 		)
+	# nvdajp end
 	# liblouis gives us back a character string of cells, so convert it to a list of ints.
 	# For some reason, the highest bit is set, so only grab the lower 8 bits.
 	braille = [ord(cell) & 255 for cell in braille]

```