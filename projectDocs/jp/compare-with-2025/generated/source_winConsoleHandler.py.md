# Diff for: `source\winConsoleHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\winConsoleHandler.py`  
**Current**: `F:\nvda\gh\alphajp\source\winConsoleHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\winConsoleHandler.py" "b/F:\\nvda\\gh\\alphajp\\source\\winConsoleHandler.py"
index 8446131aa6..8dbd10c5ca 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\winConsoleHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\winConsoleHandler.py"
@@ -2,10 +2,11 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2009-2018 NV Access Limited, Babbage B.V.
+# Copyright (C) 2009-2025 NV Access Limited, Babbage B.V.
 
 import gui
 import winUser
+import winBindings.user32
 import winKernel
 import wincon
 from colors import RGB
@@ -153,7 +154,7 @@ def getConsoleVisibleLines():
 	return newLines
 
 
-@winUser.WINEVENTPROC
+@winBindings.user32.WINEVENTPROC
 def consoleWinEventHook(handle, eventID, window, objectID, childID, threadID, timestamp):
 	from NVDAObjects.behaviors import KeyboardHandlerBasedTypedCharSupport
 

```