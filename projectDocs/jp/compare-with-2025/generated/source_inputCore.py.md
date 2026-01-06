# Diff for: `source\inputCore.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\inputCore.py`  
**Current**: `F:\nvda\gh\alphajp\source\inputCore.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\inputCore.py" "b/F:\\nvda\\gh\\alphajp\\source\\inputCore.py"
index 822c0335fb..d2529a40af 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\inputCore.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\inputCore.py"
@@ -601,12 +601,6 @@ def suppressCancelSpeech():
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