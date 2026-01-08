# Diff for: `source\eventHandler.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\eventHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\eventHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\eventHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\eventHandler.py"
index fc9ce92..127a777 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\eventHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\eventHandler.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2007-2023 NV Access Limited, Babbage B.V., Joseph Lee
+# Copyright (C) 2007-2025 NV Access Limited, Babbage B.V., Joseph Lee
 
 import threading
 import typing
@@ -18,6 +18,7 @@
 from logHandler import log
 import globalPluginHandler
 import config
+from winBindings import user32
 import winUser
 import extensionPoints
 import oleacc
@@ -500,9 +501,11 @@ def shouldAcceptEvent(eventName, windowHandle=None):
 	if eventName == "hide":
 		return False
 	if eventName == "show":
-		# ATOKxxUIComment
+		# BEGIN JP PATCH
+		# nvdajp: ATOKxxUIComment
 		if wClass.startswith("ATOK") and wClass.endswith("UIComment"):
 			return True
+		# END JP PATCH
 		# Only accept 'show' events for specific cases, as otherwise we get flooded.
 		return wClass in (
 			"Frame Notification Bar",  # notification bars
@@ -553,8 +556,8 @@ def shouldAcceptEvent(eventName, windowHandle=None):
 		# This is for the foreground application.
 		return True
 	if (
-		winUser.user32.GetWindowLongW(windowHandle, winUser.GWL_EXSTYLE) & winUser.WS_EX_TOPMOST
-		or winUser.user32.GetWindowLongW(
+		user32.GetWindowLong(windowHandle, winUser.GWL_EXSTYLE) & winUser.WS_EX_TOPMOST
+		or user32.GetWindowLong(
 			winUser.getAncestor(windowHandle, winUser.GA_ROOT),
 			winUser.GWL_EXSTYLE,
 		)

```