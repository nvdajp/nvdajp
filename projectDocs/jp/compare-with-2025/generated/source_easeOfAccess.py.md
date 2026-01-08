# Diff for: `source\easeOfAccess.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\easeOfAccess.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\easeOfAccess.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\easeOfAccess.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\easeOfAccess.py"
index 22487b3..c9c5ea7 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\easeOfAccess.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\easeOfAccess.py"
@@ -13,6 +13,7 @@
 import NVDAState
 import winreg
 import winUser
+import winBindings.user32
 
 
 def __getattr__(attrName: str) -> Any:
@@ -79,17 +80,17 @@ def notify(signal):
 	inputs = []
 	# Release unwanted keys and press desired keys.
 	for vk, desired in keys:
-		input = winUser.Input(type=winUser.INPUT_KEYBOARD)
+		input = winBindings.user32.INPUT(type=winBindings.user32.INPUT_TYPE.KEYBOARD)
 		input.ii.ki.wVk = vk
 		if not desired:
-			input.ii.ki.dwFlags = winUser.KEYEVENTF_KEYUP
+			input.ii.ki.dwFlags = winBindings.user32.KEYEVENTF.KEYUP
 		inputs.append(input)
 	# Release desired keys and press unwanted keys.
 	for vk, desired in reversed(keys):
-		input = winUser.Input(type=winUser.INPUT_KEYBOARD)
+		input = winBindings.user32.INPUT(type=winBindings.user32.INPUT_TYPE.KEYBOARD)
 		input.ii.ki.wVk = vk
 		if desired:
-			input.ii.ki.dwFlags = winUser.KEYEVENTF_KEYUP
+			input.ii.ki.dwFlags = winBindings.user32.KEYEVENTF.KEYUP
 		inputs.append(input)
 	winUser.SendInput(inputs)
 
@@ -137,6 +138,7 @@ def _getAutoStartConfiguration(autoStartContext: AutoStartContext) -> list[str]:
 			exc_info=True,
 		)
 	else:
+		k.Close()
 		if not conf[0]:
 			# "".split(",") returns [""], so remove the empty string.
 			del conf[0]
@@ -166,11 +168,11 @@ def setAutoStart(autoStartContext: AutoStartContext, enable: bool) -> None:
 		changed = True
 
 	if changed:
-		k = winreg.OpenKey(
+		with winreg.OpenKey(
 			autoStartContext.value,
 			_RegistryKey.EASE_OF_ACCESS.value,
 			access=winreg.KEY_READ | winreg.KEY_WRITE | winreg.KEY_WOW64_64KEY,
-		)
+		) as k:
 			winreg.SetValueEx(
 				k,
 				"Configuration",

```