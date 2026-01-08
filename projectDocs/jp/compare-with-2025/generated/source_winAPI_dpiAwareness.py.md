# Diff for: `source\winAPI\dpiAwareness.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\winAPI\dpiAwareness.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winAPI\dpiAwareness.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\winAPI\\dpiAwareness.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winAPI\\dpiAwareness.py"
index fa1feed..74e7b45 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\winAPI\\dpiAwareness.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winAPI\\dpiAwareness.py"
@@ -1,11 +1,13 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2022 NV Access Limited
+# Copyright (C) 2022-2025 NV Access Limited
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
 import ctypes
 
 from logHandler import log
+from winBindings import user32
+import winBindings.shcore
 
 from .constants import (
 	HResult,
@@ -35,7 +37,7 @@ def setDPIAwareness() -> None:
 		DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2 = -4
 		# Method introduced in Windows 10
 		# https://docs.microsoft.com/en-us/windows/win32/hidpi/dpi-awareness-context
-		success = ctypes.windll.user32.SetProcessDpiAwarenessContext(
+		success = user32.SetProcessDpiAwarenessContext(
 			DPI_AWARENESS_CONTEXT_PER_MONITOR_AWARE_V2,
 		)
 	except AttributeError:
@@ -66,7 +68,7 @@ def setDPIAwareness() -> None:
 		# These processes are not automatically scaled by the system.
 		PROCESS_PER_MONITOR_DPI_AWARE = 2
 		# Method introduced in Windows 8.1
-		hResult = ctypes.windll.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
+		hResult = winBindings.shcore.SetProcessDpiAwareness(PROCESS_PER_MONITOR_DPI_AWARE)
 	except AttributeError:
 		# Windows 8 / Server 2012 - `shcore` library exists,
 		# but `SetProcessDpiAwareness` is not present yet.
@@ -91,7 +93,7 @@ def setDPIAwareness() -> None:
 
 	# Method introduced in Windows Vista
 	# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-setprocessdpiaware
-	result = ctypes.windll.user32.SetProcessDPIAware()
+	result = user32.SetProcessDPIAware()
 	if result == 0:
 		errorCode = ctypes.GetLastError()
 		log.error(f"Unknown error setting DPI Awareness. Error code: {errorCode}")

```