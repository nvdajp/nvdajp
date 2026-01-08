# Diff for: `source\mouseHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\mouseHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\mouseHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\mouseHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\mouseHandler.py"
index 0564d27..69e1c81 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\mouseHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\mouseHandler.py"
@@ -1,15 +1,13 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2016-2023 NV Access Limited
+# Copyright (C) 2016-2025 NV Access Limited
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
 from dataclasses import dataclass
-from typing import Optional
 import time
 import wx
 import gui
 import tones
-import ctypes
 import winUser
 import queueHandler
 import api
@@ -25,6 +23,7 @@
 from contextlib import contextmanager
 import threading
 from winAPI.winUser.constants import SystemMetrics
+from winBindings import user32
 
 
 WM_MOUSEMOVE = 0x0200
@@ -127,27 +126,23 @@ def internal_mouseEvent(msg, x, y, injected):
 	return True
 
 
-def executeMouseEvent(flags, x, y, data=0):
+def executeMouseEvent(flags: int, x: int, y: int, data: int = 0) -> None:
 	"""
-	Mouse events generated with this rapper for L{winUser.mouse_event}
-	will be ignored by NVDA.
-	Consult https://docs.microsoft.com/en-us/windows/desktop/api/winuser/nf-winuser-mouse_event
-	for detailed parameter documentation.
-	@param flags: Controls various aspects of mouse motion and button clicking.
-		The supplied value should be one or a combination of the C{winUser.MOUSEEVENTF_*} constants.
-	@type flags: int
-	@param x: The mouse's absolute position along the x-axis
+	Generates mouse events that will be ignored by NVDA.
+
+	.. seealso::
+		https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-mouse_event
+
+	:param flags: Controls various aspects of mouse motion and button clicking.
+		The supplied value should be one or a combination of the :var:`winUser.MOUSEEVENTF_*` constants.
+	:param x: The mouse's absolute position along the x-axis,
 		or its amount of motion since the last mouse event was generated.
-	@type x: int
-	@param y: The mouse's absolute position along the y-axis
+	:param y: The mouse's absolute position along the y-axis,
 		or its amount of motion since the last mouse event was generated.
-	@type y: int
-	@param data: Additional data depending on what flags are specified.
-		This defaults to 0.
-	@type data: int
+	:param data: Additional data depending on what flags are specified, default 0.
 	"""
 	with ignoreInjection():
-		winUser.mouse_event(flags, x, y, data, None)
+		winUser.mouse_event(flags, x, y, data, 0)
 
 
 def getMouseRestrictedToScreens(x, y, displays):
@@ -318,7 +313,7 @@ def getLogicalButtonFlags() -> LogicalButtonFlags:
 	taking into account the Windows user setting
 	for which button (left or right) is primary and which is secondary.
 	"""
-	swappedButtons = ctypes.windll.user32.GetSystemMetrics(SystemMetrics.SWAP_BUTTON)
+	swappedButtons = user32.GetSystemMetrics(SystemMetrics.SWAP_BUTTON)
 	if not swappedButtons:
 		return LogicalButtonFlags(
 			primaryDown=winUser.MOUSEEVENTF_LEFTDOWN,
@@ -338,7 +333,7 @@ def getLogicalButtonFlags() -> LogicalButtonFlags:
 def _doClick(
 	downFlag: int,
 	upFlag: int,
-	releaseDelay: Optional[float] = None,
+	releaseDelay: float | None = None,
 ):
 	executeMouseEvent(downFlag, 0, 0)
 	if releaseDelay:
@@ -346,7 +341,7 @@ def _doClick(
 	executeMouseEvent(upFlag, 0, 0)
 
 
-def doPrimaryClick(releaseDelay: Optional[float] = None):
+def doPrimaryClick(releaseDelay: float | None = None):
 	"""
 	Performs a primary mouse click at the current mouse pointer location.
 	The primary button is the one that usually activates or selects an item.
@@ -359,7 +354,7 @@ def doPrimaryClick(releaseDelay: Optional[float] = None):
 	_doClick(buttonFlags.primaryDown, buttonFlags.primaryUp, releaseDelay)
 
 
-def doSecondaryClick(releaseDelay: Optional[float] = None):
+def doSecondaryClick(releaseDelay: float | None = None):
 	"""
 	Performs a secondary mouse click at the current mouse pointer location.
 	The secondary button is the one that usually displays a context menu for an item when clicked.

```