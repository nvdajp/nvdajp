# Diff for: `source\NVDAObjects\IAccessible\MSHTML.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\IAccessible\MSHTML.py`  
**Current**: `F:\nvda\gh\alphajp\source\NVDAObjects\IAccessible\MSHTML.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\IAccessible\\MSHTML.py" "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\IAccessible\\MSHTML.py"
index db53b29d5b..6aca35437e 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\IAccessible\\MSHTML.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\IAccessible\\MSHTML.py"
@@ -1,6 +1,6 @@
 # NVDAObjects/MSHTML.py
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2006-2015 NV Access Limited, Aleksey Sadovoy
+# Copyright (C) 2006-2025 NV Access Limited, Aleksey Sadovoy
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -11,6 +11,7 @@
 import ctypes
 import ctypes.wintypes
 import contextlib
+from winBindings import user32
 import winUser
 import oleacc
 import UIAHandler
@@ -520,7 +521,7 @@ def kwargsFromSuper(cls, kwargs, relation=None):
 		elif isinstance(relation, tuple):
 			windowHandle = kwargs.get("windowHandle")
 			p = ctypes.wintypes.POINT(x=relation[0], y=relation[1])
-			ctypes.windll.user32.ScreenToClient(windowHandle, ctypes.byref(p))
+			user32.ScreenToClient(windowHandle, ctypes.byref(p))
 			# #3494: MSHTML's internal coordinates are always at a hardcoded DPI (usually 96) no matter the system DPI or zoom level.
 			xFactor, yFactor = getZoomFactorsFromHTMLDocument(HTMLNode.document)
 			try:

```