# Diff for: `source\displayModel.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\displayModel.py`  
**Current**: `F:\nvda\gh\alphajp\source\displayModel.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\displayModel.py" "b/F:\\nvda\\gh\\alphajp\\source\\displayModel.py"
index d81d878f03..fde2cb0110 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\displayModel.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\displayModel.py"
@@ -1,13 +1,12 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2006-2022 NV Access Limited, Babbage B.V., Joseph Lee, Cyrille Bougot
+# Copyright (C) 2006-2025 NV Access Limited, Babbage B.V., Joseph Lee, Cyrille Bougot
 
-import ctypes
-from ctypes import *  # noqa: F403
-from comtypes import BSTR
+from ctypes import byref, c_short, c_long
 import unicodedata
 import math
+from NVDAHelper import localLib
 import colors
 import XMLFormatting
 import api
@@ -200,50 +199,31 @@ def processFieldsAndRectsRangeReadingdirection(
 		rects[startOffset:endOffset] = newRects
 
 
-_getWindowTextInRect = None
 _requestTextChangeNotificationsForWindow = None
 #: Objects that have registered for text change notifications.
 _textChangeNotificationObjs = []
 
 
 def initialize():
-	global _getWindowTextInRect, _requestTextChangeNotificationsForWindow, _getFocusRect
-	_getWindowTextInRect = CFUNCTYPE(  # noqa: F405
-		c_long,  # noqa: F405
-		c_long,  # noqa: F405
-		c_long,  # noqa: F405
-		c_bool,  # noqa: F405
-		c_int,  # noqa: F405
-		c_int,  # noqa: F405
-		c_int,  # noqa: F405
-		c_int,  # noqa: F405
-		c_int,  # noqa: F405
-		c_int,  # noqa: F405
-		c_bool,  # noqa: F405
-		POINTER(BSTR),  # noqa: F405
-		POINTER(BSTR),  # noqa: F405
-	)(
-		("displayModel_getWindowTextInRect", NVDAHelper.localLib),
-		((1,), (1,), (1,), (1,), (1,), (1,), (1,), (1,), (1,), (1,), (2,), (2,)),
-	)  # noqa: F405
+	global _requestTextChangeNotificationsForWindow
 	_requestTextChangeNotificationsForWindow = (
 		NVDAHelper.localLib.displayModel_requestTextChangeNotificationsForWindow
 	)
 
 
 def getCaretRect(obj):
-	left = ctypes.c_long()
-	top = ctypes.c_long()
-	right = ctypes.c_long()
-	bottom = ctypes.c_long()
+	left = c_long()
+	top = c_long()
+	right = c_long()
+	bottom = c_long()
 	res = watchdog.cancellableExecute(
 		NVDAHelper.localLib.displayModel_getCaretRect,
 		obj.appModule.helperLocalBindingHandle,
 		obj.windowThreadID,
-		ctypes.byref(left),
-		ctypes.byref(top),
-		ctypes.byref(right),
-		ctypes.byref(bottom),
+		byref(left),
+		byref(top),
+		byref(right),
+		byref(bottom),
 	)
 	if res != 0:
 		raise RuntimeError(f"displayModel_getCaretRect failed with res {res}")
@@ -268,7 +248,7 @@ def getWindowTextInRect(
 	includeDescendantWindows=True,
 ):
 	text, cpBuf = watchdog.cancellableExecute(
-		_getWindowTextInRect,
+		localLib.displayModel_getWindowTextInRect,
 		bindingHandle,
 		windowHandle,
 		includeDescendantWindows,

```