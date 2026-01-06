# Diff for: `source\textInfos\offsets.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\textInfos\offsets.py`  
**Current**: `F:\nvda\gh\alphajp\source\textInfos\offsets.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\textInfos\\offsets.py" "b/F:\\nvda\\gh\\alphajp\\source\\textInfos\\offsets.py"
index e67102c85a..f9a6973bd7 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\textInfos\\offsets.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\textInfos\\offsets.py"
@@ -344,26 +344,21 @@ def _calculateUniscribeOffsets(
 			raise NotImplementedError(f"Unit: {unit}")
 		relStart = ctypes.c_int()
 		relEnd = ctypes.c_int()
-		# uniscribe does some strange things
-		# when you give it a string  with not more than two alphanumeric chars in a row.
-		# Inject two alphanumeric characters at the end to fix this
-		uniscribeLineText = lineText + "xx"
 		# We can't rely on len(lineText) to calculate the length of the line.
 		offsetConverter = textUtils.WideStringOffsetConverter(lineText)
 		lineLength = offsetConverter.encodedStringLength
 		if self.encoding != textUtils.WCHAR_ENCODING:
 			# We need to convert the str based line offsets to wide string offsets.
 			relOffset = offsetConverter.strToEncodedOffsets(relOffset, relOffset)[0]
-		uniscribeLineLength = lineLength + 2
 		if helperFunc(
-			uniscribeLineText,
-			uniscribeLineLength,
+			lineText,
+			lineLength,
 			relOffset,
 			ctypes.byref(relStart),
 			ctypes.byref(relEnd),
 		):
 			relStart = relStart.value
-			relEnd = min(lineLength, relEnd.value)
+			relEnd = relEnd.value
 			if self.encoding != textUtils.WCHAR_ENCODING:
 				# We need to convert the uniscribe based offsets to str offsets.
 				relStart, relEnd = offsetConverter.encodedToStrOffsets(relStart, relEnd)
@@ -648,7 +643,11 @@ def unitCount(self, unit):
 		else:
 			raise NotImplementedError
 
-	allowMoveToOffsetPastEnd = True  #: move with unit_character can move 1 past story length to allow braille routing to end insertion point. (#2096)
+	allowMoveToOffsetPastEnd = True
+	"""
+	We can move 1 past story length to allow braille routing to end insertion point. (#2096)
+	Furthermore, review cursor is able to reach the last, empty line in some controls, like Scintilla. (#18348)
+	"""
 
 	def move(self, unit, direction, endPoint=None):
 		if direction == 0:
@@ -664,7 +663,7 @@ def move(self, unit, direction, endPoint=None):
 		count = 0
 		lowLimit = 0
 		highLimit = self._getStoryLength()
-		if self.allowMoveToOffsetPastEnd and unit == textInfos.UNIT_CHARACTER:
+		if self.allowMoveToOffsetPastEnd:
 			# #2096: There is often an uncounted character at the end of the text
 			# where the caret is placed to append text.
 			highLimit += 1

```