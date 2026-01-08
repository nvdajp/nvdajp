# Diff for: `source\brailleDisplayDrivers\albatross\_threading.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\brailleDisplayDrivers\albatross\_threading.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\brailleDisplayDrivers\albatross\_threading.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\brailleDisplayDrivers\\albatross\\_threading.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleDisplayDrivers\\albatross\\_threading.py"
index b8b8190..d9fad82 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\brailleDisplayDrivers\\albatross\\_threading.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleDisplayDrivers\\albatross\\_threading.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2023 NV Access Limited, Burman's Computer and Education Ltd.
+# Copyright (C) 2023-2025 NV Access Limited, Burman's Computer and Education Ltd.
 
 """Threads for Tivomatic Caiku Albatross braille display driver.
 Classes:
@@ -31,7 +31,7 @@
 	Timer,
 )
 from typing import Callable
-
+import winBindings.kernel32
 from .constants import KC_INTERVAL
 
 
@@ -91,7 +91,7 @@ def run(self):
 					self._disableFunction()
 					log.debug("SetCommMask failed")
 					continue
-				result = ctypes.windll.kernel32.WaitCommEvent(
+				result = winBindings.kernel32.WaitCommEvent(
 					self._dev._port_handle,
 					byref(dwEvtMask),
 					byref(self._dev._overlapped_read),
@@ -102,7 +102,7 @@ def run(self):
 					self._disableFunction()
 					log.debug("WaitCommEvent failed")
 					continue
-				result = ctypes.windll.kernel32.GetOverlappedResult(
+				result = winBindings.kernel32.GetOverlappedResult(
 					self._dev._port_handle,
 					byref(self._dev._overlapped_read),
 					byref(data),

```