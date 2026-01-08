# Diff for: `source\inputCore.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\inputCore.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\inputCore.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\inputCore.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\inputCore.py"
index 3bcfc19..d2529a4 100644
--- "a/F:\\nvda\\gh\\beta\\source\\inputCore.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\inputCore.py"
@@ -43,7 +43,7 @@
 import languageHandler
 import controlTypes
 import extensionPoints
-from NVDAState import WritePaths, shouldWriteToDisk
+from NVDAState import WritePaths
 
 
 InputGestureBindingClassT = TypeVar("InputGestureBindingClassT")
@@ -438,9 +438,6 @@ def save(self):
 		"""Save this gesture map to disk.
 		@precondition: L{load} must have been called.
 		"""
-		if not shouldWriteToDisk():
-			log.debug("Not saving user gesture map, as shouldWriteToDisk returned false.")
-			return
 		if not self.fileName:
 			raise ValueError("No file name")
 		out = configobj.ConfigObj(self.export(), encoding="UTF-8")

```