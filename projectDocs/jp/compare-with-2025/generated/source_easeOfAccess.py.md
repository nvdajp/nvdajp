# Diff for: `source\easeOfAccess.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\easeOfAccess.py`  
**Current**: `F:\nvda\gh\alphajp\source\easeOfAccess.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\easeOfAccess.py" "b/F:\\nvda\\gh\\alphajp\\source\\easeOfAccess.py"
index 22487b37f8..1d9934ff3e 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\easeOfAccess.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\easeOfAccess.py"
@@ -13,6 +13,7 @@
 import NVDAState
 import winreg
 import winUser
+import winBindings.user32
 
 
 def __getattr__(attrName: str) -> Any:
@@ -79,14 +80,14 @@ def notify(signal):
 	inputs = []
 	# Release unwanted keys and press desired keys.
 	for vk, desired in keys:
-		input = winUser.Input(type=winUser.INPUT_KEYBOARD)
+		input = winBindings.user32.INPUT(type=winUser.INPUT_KEYBOARD)
 		input.ii.ki.wVk = vk
 		if not desired:
 			input.ii.ki.dwFlags = winUser.KEYEVENTF_KEYUP
 		inputs.append(input)
 	# Release desired keys and press unwanted keys.
 	for vk, desired in reversed(keys):
-		input = winUser.Input(type=winUser.INPUT_KEYBOARD)
+		input = winBindings.user32.INPUT(type=winUser.INPUT_KEYBOARD)
 		input.ii.ki.wVk = vk
 		if desired:
 			input.ii.ki.dwFlags = winUser.KEYEVENTF_KEYUP

```