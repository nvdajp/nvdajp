# Diff for: `source\inputCore.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\inputCore.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\inputCore.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\inputCore.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\inputCore.py"
index 822c033..3bcfc19 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\inputCore.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\inputCore.py"
@@ -43,7 +43,7 @@
 import languageHandler
 import controlTypes
 import extensionPoints
-from NVDAState import WritePaths
+from NVDAState import WritePaths, shouldWriteToDisk
 
 
 InputGestureBindingClassT = TypeVar("InputGestureBindingClassT")
@@ -438,6 +438,9 @@ def save(self):
 		"""Save this gesture map to disk.
 		@precondition: L{load} must have been called.
 		"""
+		if not shouldWriteToDisk():
+			log.debug("Not saving user gesture map, as shouldWriteToDisk returned false.")
+			return
 		if not self.fileName:
 			raise ValueError("No file name")
 		out = configobj.ConfigObj(self.export(), encoding="UTF-8")
@@ -601,12 +604,6 @@ def suppressCancelSpeech():
 				gesture.displayName,
 				_immediate=True,
 			)
-		# nvdajp begin
-		import winUser
-
-		if hasattr(gesture, "vkCode") and gesture.vkCode == winUser.VK_RETURN:
-			_ = winUser.getAsyncKeyState(winUser.VK_BACK)  # noqa: F841
-		# nvdajp end
 
 		gesture.reportExtra()
 

```