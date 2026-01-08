# Diff for: `source\textInfos\offsets.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\textInfos\offsets.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\textInfos\offsets.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\textInfos\\offsets.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\textInfos\\offsets.py"
index e67102c..1def339 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\textInfos\\offsets.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\textInfos\\offsets.py"
@@ -1,14 +1,14 @@
-# textInfos/offsets.py
 # A part of NonVisual Desktop Access (NVDA)
-# This file is covered by the GNU General Public License.
-# See the file COPYING for more details.
-# Copyright (C) 2006-2024 NV Access Limited, Babbage B.V., Leonard de Ruijter
+# Copyright (C) 2006-2025 NV Access Limited, Babbage B.V., Leonard de Ruijter
+# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
+# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
 
 from abc import abstractmethod
 import re
 import ctypes
 import unicodedata
 import NVDAHelper
+import NVDAState
 import config
 import textInfos
 import locationHelper
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
@@ -648,7 +643,27 @@ def unitCount(self, unit):
 		else:
 			raise NotImplementedError
 
-	allowMoveToOffsetPastEnd = True  #: move with unit_character can move 1 past story length to allow braille routing to end insertion point. (#2096)
+	def allowMoveToUnitOffsetPastEnd(self, unit: str) -> bool:
+		"""
+		This method indicates whether the `move` method is allowed to move one unit past the end of the text info.
+		For example, normally we should be able to move 1 past story length
+		to allow braille routing to move to an insertion point at the end. (#2096)
+		Furthermore, review cursor should be able to reach the last, empty line in some controls,
+		like Scintilla. (#18348)
+		:param unit: the TextInfo unit (e.g. character or word)
+		:return: Whether or not to allow movement past end for the specific unit.
+		"""
+		return True
+
+	if NVDAState._allowDeprecatedAPI():
+
+		def _get_allowMoveToOffsetPastEnd(self) -> bool:
+			log.warning(
+				"OffsetsTextInfo.allowMoveToOffsetPastEnd is deprecated. "
+				"Use the OffsetsTextInfo.allowMoveToUnitOffsetPastEnd method instead.",
+				stack_info=True,
+			)
+			return self.allowMoveToUnitOffsetPastEnd(textInfos.UNIT_CHARACTER)
 
 	def move(self, unit, direction, endPoint=None):
 		if direction == 0:
@@ -664,9 +679,7 @@ def move(self, unit, direction, endPoint=None):
 		count = 0
 		lowLimit = 0
 		highLimit = self._getStoryLength()
-		if self.allowMoveToOffsetPastEnd and unit == textInfos.UNIT_CHARACTER:
-			# #2096: There is often an uncounted character at the end of the text
-			# where the caret is placed to append text.
+		if self.allowMoveToUnitOffsetPastEnd(unit):
 			highLimit += 1
 		while (
 			count != direction

```