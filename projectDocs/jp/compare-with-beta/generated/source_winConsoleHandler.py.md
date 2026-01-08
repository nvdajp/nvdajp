# Diff for: `source\winConsoleHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winConsoleHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winConsoleHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winConsoleHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winConsoleHandler.py"
index 648c488..aff67ec 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winConsoleHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winConsoleHandler.py"
@@ -4,7 +4,6 @@
 # See the file COPYING for more details.
 # Copyright (C) 2009-2025 NV Access Limited, Babbage B.V.
 
-from ctypes.wintypes import SMALL_RECT
 import gui
 import winUser
 import winBindings.kernel32
@@ -157,15 +156,7 @@ def getConsoleVisibleLines():
 
 
 @winBindings.user32.WINEVENTPROC
-def consoleWinEventHook(
-	handle: int | None,
-	eventID: int,
-	window: int | None,
-	objectID: int,
-	childID: int,
-	threadID: int,
-	timestamp: int,
-) -> None:
+def consoleWinEventHook(handle, eventID, window, objectID, childID, threadID, timestamp):
 	from NVDAObjects.behaviors import KeyboardHandlerBasedTypedCharSupport
 
 	# We don't want to do anything with the event if the event is not for the window this console is in
@@ -273,7 +264,7 @@ def getTextWithFields(self, formatConfig: Optional[Dict] = None) -> textInfos.Te
 			formatConfig = config.conf["documentFormatting"]
 		left, top = self._consoleCoordFromOffset(self._startOffset)
 		right, bottom = self._consoleCoordFromOffset(self._endOffset - 1)
-		rect = SMALL_RECT(left, top, right, bottom)
+		rect = wincon.SMALL_RECT(left, top, right, bottom)
 		if bottom - top > 0:  # offsets span multiple lines
 			rect.Left = 0
 			rect.Right = self.consoleScreenBufferInfo.dwSize.x - 1

```