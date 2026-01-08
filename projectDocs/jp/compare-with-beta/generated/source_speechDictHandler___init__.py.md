# Diff for: `source\speechDictHandler\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\speechDictHandler\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\speechDictHandler\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\speechDictHandler\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\speechDictHandler\\__init__.py"
index bafa772..ac0794d 100644
--- "a/F:\\nvda\\gh\\beta\\source\\speechDictHandler\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\speechDictHandler\\__init__.py"
@@ -10,7 +10,7 @@
 import os
 import codecs
 
-from NVDAState import WritePaths, shouldWriteToDisk
+from NVDAState import WritePaths
 from . import dictFormatUpgrade
 
 
@@ -118,9 +118,6 @@ def load(self, fileName):
 		return
 
 	def save(self, fileName=None):
-		if not shouldWriteToDisk():
-			log.debugWarning("Not writing dictionary, as shouldWriteToDisk returned False.")
-			return
 		if not fileName:
 			fileName = getattr(self, "fileName", None)
 		if not fileName:

```