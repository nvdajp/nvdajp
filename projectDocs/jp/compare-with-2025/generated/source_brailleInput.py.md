# Diff for: `source\brailleInput.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\brailleInput.py`  
**Current**: `F:\nvda\gh\alphajp\source\brailleInput.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\brailleInput.py" "b/F:\\nvda\\gh\\alphajp\\source\\brailleInput.py"
index e19cb67589..0e961cb0f2 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\brailleInput.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\brailleInput.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2012-2024 NV Access Limited, Rui Batista, Babbage B.V., Julien Cochuyt, Leonard de Ruijter
+# Copyright (C) 2012-2025 NV Access Limited, Rui Batista, Babbage B.V., Julien Cochuyt, Leonard de Ruijter
 
 import time
 from typing import Optional, List, Set
@@ -12,6 +12,7 @@
 import config
 from logHandler import log
 import winUser
+import winBindings.user32
 import inputCore
 import speech
 import keyboardHandler
@@ -409,9 +410,9 @@ def sendChars(self, chars: str):
 		)
 		for ch in chars:
 			for direction in (0, winUser.KEYEVENTF_KEYUP):
-				input = winUser.Input()
+				input = winBindings.user32.INPUT()
 				input.type = winUser.INPUT_KEYBOARD
-				input.ii.ki = winUser.KeyBdInput()
+				input.ii.ki = winBindings.user32.KEYBDINPUT()
 				input.ii.ki.wScan = ord(ch)
 				input.ii.ki.dwFlags = winUser.KEYEVENTF_UNICODE | direction
 				inputs.append(input)

```