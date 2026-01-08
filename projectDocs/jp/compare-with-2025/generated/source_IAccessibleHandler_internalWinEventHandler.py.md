# Diff for: `source\IAccessibleHandler\internalWinEventHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\IAccessibleHandler\internalWinEventHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\IAccessibleHandler\internalWinEventHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\IAccessibleHandler\\internalWinEventHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\IAccessibleHandler\\internalWinEventHandler.py"
index 4243d40..4669248 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\IAccessibleHandler\\internalWinEventHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\IAccessibleHandler\\internalWinEventHandler.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2020 NV Access Limited
+# Copyright (C) 2020-2025 NV Access Limited
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -7,11 +7,12 @@
 Provides a non-threaded (limited by GIL) Windows Event Hook and processing.
 """
 
-from ctypes import WINFUNCTYPE, c_int
+from ctypes import c_int
 
 from typing import Dict, Callable
 
 import core
+from winBindings.user32 import WINEVENTPROC
 import winUser
 from .utils import getWinEventLogInfo, isMSAADebugLoggingEnabled
 
@@ -65,7 +66,17 @@
 
 
 # C901: winEventCallback is too complex
-def winEventCallback(handle, eventID, window, objectID, childID, threadID, timestamp):  # noqa: C901
+def winEventCallback(
+	handle: int | None,
+	eventID: int,
+	window: int | None,
+	objectID: int,
+	childID: int,
+	threadID: int,
+	timestamp: int,
+) -> None:  # noqa: C901
+	if window is None:
+		window = 0
 	if isMSAADebugLoggingEnabled():
 		log.debug(
 			f"Hook received winEvent: {getWinEventLogInfo(window, objectID, childID, eventID, threadID)}",
@@ -185,7 +196,7 @@ def winEventCallback(handle, eventID, window, objectID, childID, threadID, times
 
 
 # Register internal object event with IAccessible
-cWinEventCallback = WINFUNCTYPE(None, c_int, c_int, c_int, c_int, c_int, c_int, c_int)(winEventCallback)
+cWinEventCallback = WINEVENTPROC(winEventCallback)
 # A list to store handles received from setWinEventHook, for use with unHookWinEvent
 winEventHookIDs = []
 

```