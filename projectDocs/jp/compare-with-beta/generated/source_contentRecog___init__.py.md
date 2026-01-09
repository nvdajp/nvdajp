# Diff for: `source\contentRecog\__init__.py`

**Source**: `F:\nvda\gh\beta\source\contentRecog\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\contentRecog\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\contentRecog\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\contentRecog\\__init__.py"
index 39975b1..bb63381 100644
--- "a/F:\\nvda\\gh\\beta\\source\\contentRecog\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\contentRecog\\__init__.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2017-2025 NV Access Limited, James Teh, Leonard de Ruijter, Cary-rowen
+# Copyright (C) 2017-2023 NV Access Limited, James Teh, Leonard de Ruijter
 # This file is covered by the GNU General Public License.
 #  See the file COPYING for more details.
 
@@ -21,11 +21,35 @@
 import textInfos.offsets
 from abc import ABCMeta, abstractmethod
 from locationHelper import RectLTWH
+
+# BEGIN JP PATCH
+# nvdajp: import for East Asian width checking
+from unicodedata import east_asian_width
+
+# END JP PATCH
 from NVDAObjects import NVDAObject
 
 onRecognizeResultCallbackT = Callable[[Union["RecognitionResult", Exception]], None]
 
 
+# BEGIN JP PATCH
+# nvdajp: functions for checking East Asian narrow characters
+def isEastAsianNarrow(c):
+	return c and (east_asian_width(str(c)) == "Na")
+
+
+def startsWithEastAsianNarrow(s):
+	return s and isEastAsianNarrow(s[0])
+
+
+def endsWithEastAsianNarrow(s):
+	return s and isEastAsianNarrow(s[-1])
+
+
+# nvdajp end
+# END JP PATCH
+
+
 class BaseContentRecogTextInfo(cursorManager._ReviewCursorManagerTextInfo):
 	"""
 	The TextInfo class that all TextInfos emitted by implementations of RecognitionResult must inherit from.
@@ -242,6 +266,16 @@ def _parseData(self):
 			for word in line:
 				if firstWordOfLine:
 					firstWordOfLine = False
+				# BEGIN JP PATCH
+				# nvdajp: don't add space between East Asian narrow characters
+				elif (
+					self._textList
+					and endsWithEastAsianNarrow(self._textList[-1])
+					and startsWithEastAsianNarrow(word["text"])
+				):
+					# Don't separate with a space for East Asian narrow characters.
+					pass
+				# END JP PATCH
 				else:
 					# Separate with a space.
 					self._textList.append(" ")

```