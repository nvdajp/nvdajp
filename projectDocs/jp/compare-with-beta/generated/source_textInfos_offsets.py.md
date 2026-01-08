# Diff for: `source\textInfos\offsets.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\textInfos\offsets.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\textInfos\offsets.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\textInfos\\offsets.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\textInfos\\offsets.py"
index 1def339..f9a6973 100644
--- "a/F:\\nvda\\gh\\beta\\source\\textInfos\\offsets.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\textInfos\\offsets.py"
@@ -1,14 +1,14 @@
+# textInfos/offsets.py
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2006-2025 NV Access Limited, Babbage B.V., Leonard de Ruijter
-# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
-# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
+# This file is covered by the GNU General Public License.
+# See the file COPYING for more details.
+# Copyright (C) 2006-2024 NV Access Limited, Babbage B.V., Leonard de Ruijter
 
 from abc import abstractmethod
 import re
 import ctypes
 import unicodedata
 import NVDAHelper
-import NVDAState
 import config
 import textInfos
 import locationHelper
@@ -643,27 +643,11 @@ def unitCount(self, unit):
 		else:
 			raise NotImplementedError
 
-	def allowMoveToUnitOffsetPastEnd(self, unit: str) -> bool:
+	allowMoveToOffsetPastEnd = True
 	"""
-		This method indicates whether the `move` method is allowed to move one unit past the end of the text info.
-		For example, normally we should be able to move 1 past story length
-		to allow braille routing to move to an insertion point at the end. (#2096)
-		Furthermore, review cursor should be able to reach the last, empty line in some controls,
-		like Scintilla. (#18348)
-		:param unit: the TextInfo unit (e.g. character or word)
-		:return: Whether or not to allow movement past end for the specific unit.
+	We can move 1 past story length to allow braille routing to end insertion point. (#2096)
+	Furthermore, review cursor is able to reach the last, empty line in some controls, like Scintilla. (#18348)
 	"""
-		return True
-
-	if NVDAState._allowDeprecatedAPI():
-
-		def _get_allowMoveToOffsetPastEnd(self) -> bool:
-			log.warning(
-				"OffsetsTextInfo.allowMoveToOffsetPastEnd is deprecated. "
-				"Use the OffsetsTextInfo.allowMoveToUnitOffsetPastEnd method instead.",
-				stack_info=True,
-			)
-			return self.allowMoveToUnitOffsetPastEnd(textInfos.UNIT_CHARACTER)
 
 	def move(self, unit, direction, endPoint=None):
 		if direction == 0:
@@ -679,7 +663,9 @@ def move(self, unit, direction, endPoint=None):
 		count = 0
 		lowLimit = 0
 		highLimit = self._getStoryLength()
-		if self.allowMoveToUnitOffsetPastEnd(unit):
+		if self.allowMoveToOffsetPastEnd:
+			# #2096: There is often an uncounted character at the end of the text
+			# where the caret is placed to append text.
 			highLimit += 1
 		while (
 			count != direction

```