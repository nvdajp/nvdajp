# Diff for: `source\brailleInput.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\brailleInput.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\brailleInput.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\brailleInput.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleInput.py"
index 4b7fedb..0e961cb 100644
--- "a/F:\\nvda\\gh\\beta\\source\\brailleInput.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleInput.py"
@@ -409,12 +409,12 @@ def sendChars(self, chars: str):
 			for ch in chars
 		)
 		for ch in chars:
-			for direction in (0, winBindings.user32.KEYEVENTF.KEYUP):
+			for direction in (0, winUser.KEYEVENTF_KEYUP):
 				input = winBindings.user32.INPUT()
-				input.type = winBindings.user32.INPUT_TYPE.KEYBOARD
+				input.type = winUser.INPUT_KEYBOARD
 				input.ii.ki = winBindings.user32.KEYBDINPUT()
 				input.ii.ki.wScan = ord(ch)
-				input.ii.ki.dwFlags = winBindings.user32.KEYEVENTF.UNICODE | direction
+				input.ii.ki.dwFlags = winUser.KEYEVENTF_UNICODE | direction
 				inputs.append(input)
 		winUser.SendInput(inputs)
 		focusObj = api.getFocusObject()

```