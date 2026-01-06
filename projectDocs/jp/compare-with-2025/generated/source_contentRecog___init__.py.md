# Diff for: `source\contentRecog\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\contentRecog\__init__.py`  
**Current**: `F:\nvda\gh\alphajp\source\contentRecog\__init__.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\contentRecog\\__init__.py" "b/F:\\nvda\\gh\\alphajp\\source\\contentRecog\\__init__.py"
index f0825aa276..8f6ec59a6c 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\contentRecog\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\contentRecog\\__init__.py"
@@ -21,26 +21,11 @@
 import textInfos.offsets
 from abc import ABCMeta, abstractmethod
 from locationHelper import RectLTWH
-from unicodedata import east_asian_width
 from NVDAObjects import NVDAObject
 
 onRecognizeResultCallbackT = Callable[[Union["RecognitionResult", Exception]], None]
 
 
-def isEastAsianNarrow(c):
-	from six import text_type
-
-	return c and (east_asian_width(text_type(c)) == "Na")
-
-
-def startsWithEastAsianNarrow(s):
-	return s and isEastAsianNarrow(s[0])
-
-
-def endsWithEastAsianNarrow(s):
-	return s and isEastAsianNarrow(s[-1])
-
-
 class BaseContentRecogTextInfo(cursorManager._ReviewCursorManagerTextInfo):
 	"""
 	The TextInfo class that all TextInfos emitted by implementations of RecognitionResult must inherit from.
@@ -251,11 +236,7 @@ def _parseData(self):
 			for word in line:
 				if firstWordOfLine:
 					firstWordOfLine = False
-				elif (
-					self._textList
-					and endsWithEastAsianNarrow(self._textList[-1])
-					and startsWithEastAsianNarrow(word["text"])
-				):
+				else:
 					# Separate with a space.
 					self._textList.append(" ")
 					self.textLen += 1

```