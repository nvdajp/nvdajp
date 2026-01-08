# Diff for: `source\winConsoleHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\winConsoleHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winConsoleHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\winConsoleHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winConsoleHandler.py"
index 8446131..648c488 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\winConsoleHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winConsoleHandler.py"
@@ -2,10 +2,13 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2009-2018 NV Access Limited, Babbage B.V.
+# Copyright (C) 2009-2025 NV Access Limited, Babbage B.V.
 
+from ctypes.wintypes import SMALL_RECT
 import gui
 import winUser
+import winBindings.kernel32
+import winBindings.user32
 import winKernel
 import wincon
 from colors import RGB
@@ -54,7 +57,7 @@
 COMMON_LVB_UNDERSCORE = 0x8000
 
 
-@wincon.PHANDLER_ROUTINE
+@winBindings.kernel32.PHANDLER_ROUTINE
 def _consoleCtrlHandler(event):
 	if event in (wincon.CTRL_C_EVENT, wincon.CTRL_BREAK_EVENT):
 		return True
@@ -153,8 +156,16 @@ def getConsoleVisibleLines():
 	return newLines
 
 
-@winUser.WINEVENTPROC
-def consoleWinEventHook(handle, eventID, window, objectID, childID, threadID, timestamp):
+@winBindings.user32.WINEVENTPROC
+def consoleWinEventHook(
+	handle: int | None,
+	eventID: int,
+	window: int | None,
+	objectID: int,
+	childID: int,
+	threadID: int,
+	timestamp: int,
+) -> None:
 	from NVDAObjects.behaviors import KeyboardHandlerBasedTypedCharSupport
 
 	# We don't want to do anything with the event if the event is not for the window this console is in
@@ -262,7 +273,7 @@ def getTextWithFields(self, formatConfig: Optional[Dict] = None) -> textInfos.Te
 			formatConfig = config.conf["documentFormatting"]
 		left, top = self._consoleCoordFromOffset(self._startOffset)
 		right, bottom = self._consoleCoordFromOffset(self._endOffset - 1)
-		rect = wincon.SMALL_RECT(left, top, right, bottom)
+		rect = SMALL_RECT(left, top, right, bottom)
 		if bottom - top > 0:  # offsets span multiple lines
 			rect.Left = 0
 			rect.Right = self.consoleScreenBufferInfo.dwSize.x - 1

```