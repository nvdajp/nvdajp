# Diff for: `source\louisHelper.py`

**Source**: `F:\nvda\gh\beta\source\louisHelper.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\louisHelper.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\louisHelper.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\louisHelper.py"
index d59b673..f0a1b56 100644
--- "a/F:\\nvda\\gh\\beta\\source\\louisHelper.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\louisHelper.py"
@@ -162,6 +162,24 @@ def translate(
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
@@ -170,6 +188,7 @@ def translate(
 			cursorPos=cursorPos or 0,
 			mode=mode,
 		)
+	# nvdajp end
 	# liblouis gives us back a character string of cells, so convert it to a list of ints.
 	# For some reason, the highest bit is set, so only grab the lower 8 bits.
 	braille = [ord(cell) & 255 for cell in braille]

```