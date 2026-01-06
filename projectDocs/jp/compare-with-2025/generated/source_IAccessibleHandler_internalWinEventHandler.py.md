# Diff for: `source\IAccessibleHandler\internalWinEventHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\IAccessibleHandler\internalWinEventHandler.py`  
**Current**: `F:\nvda\gh\alphajp\source\IAccessibleHandler\internalWinEventHandler.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\IAccessibleHandler\\internalWinEventHandler.py" "b/F:\\nvda\\gh\\alphajp\\source\\IAccessibleHandler\\internalWinEventHandler.py"
index 4243d40c13..e2b17d4be6 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\IAccessibleHandler\\internalWinEventHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\IAccessibleHandler\\internalWinEventHandler.py"
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
 
@@ -185,7 +186,7 @@ def winEventCallback(handle, eventID, window, objectID, childID, threadID, times
 
 
 # Register internal object event with IAccessible
-cWinEventCallback = WINFUNCTYPE(None, c_int, c_int, c_int, c_int, c_int, c_int, c_int)(winEventCallback)
+cWinEventCallback = WINEVENTPROC(winEventCallback)
 # A list to store handles received from setWinEventHook, for use with unHookWinEvent
 winEventHookIDs = []
 

```