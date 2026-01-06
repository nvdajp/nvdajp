# Diff for: `source\contentRecog\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\contentRecog\__init__.py`  
**Current**: `F:\nvda\gh\alphajp\source\contentRecog\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\contentRecog\\__init__.py" "b/F:\\nvda\\gh\\alphajp\\source\\contentRecog\\__init__.py"
index f0825aa276..4bfb5b4f43 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\contentRecog\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\contentRecog\\__init__.py"
@@ -21,16 +21,18 @@
 import textInfos.offsets
 from abc import ABCMeta, abstractmethod
 from locationHelper import RectLTWH
+# BEGIN JP PATCH
+# nvdajp: import for East Asian width checking
 from unicodedata import east_asian_width
+# END JP PATCH
 from NVDAObjects import NVDAObject
 
 onRecognizeResultCallbackT = Callable[[Union["RecognitionResult", Exception]], None]
 
-
+# BEGIN JP PATCH
+# nvdajp: functions for checking East Asian narrow characters
 def isEastAsianNarrow(c):
-	from six import text_type
-
-	return c and (east_asian_width(text_type(c)) == "Na")
+	return c and (east_asian_width(str(c)) == "Na")
 
 
 def startsWithEastAsianNarrow(s):
@@ -41,6 +43,10 @@ def endsWithEastAsianNarrow(s):
 	return s and isEastAsianNarrow(s[-1])
 
 
+# nvdajp end
+# END JP PATCH
+
+
 class BaseContentRecogTextInfo(cursorManager._ReviewCursorManagerTextInfo):
 	"""
 	The TextInfo class that all TextInfos emitted by implementations of RecognitionResult must inherit from.
@@ -251,11 +257,17 @@ def _parseData(self):
 			for word in line:
 				if firstWordOfLine:
 					firstWordOfLine = False
+				# BEGIN JP PATCH
+				# nvdajp: don't add space between East Asian narrow characters
 				elif (
 					self._textList
 					and endsWithEastAsianNarrow(self._textList[-1])
 					and startsWithEastAsianNarrow(word["text"])
 				):
+					# Don't separate with a space for East Asian narrow characters.
+					pass
+				# END JP PATCH
+				else:
 					# Separate with a space.
 					self._textList.append(" ")
 					self.textLen += 1

```