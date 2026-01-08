# Diff for: `source\NVDAObjects\IAccessible\winword.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\IAccessible\winword.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAObjects\IAccessible\winword.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\IAccessible\\winword.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\winword.py"
index 9da9d3b..061301b 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\IAccessible\\winword.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\winword.py"
@@ -1,14 +1,14 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2006-2023 NV Access, Cyrille Bougot and other NVDA Contributors
+# Copyright (C) 2006-2025 NV Access, Cyrille Bougot and other NVDA Contributors
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
 from comtypes import COMError
-import ctypes
 import operator
 import uuid
 from logHandler import log
-import winUser
+import winBindings.kernel32
+from winBindings import user32
 import speech
 import controlTypes
 import config
@@ -585,9 +585,9 @@ def event_gainFocus(self):
 			return
 		document = next((x for x in self.children if isinstance(x, WordDocument)), None)
 		if document:
-			curThreadID = ctypes.windll.kernel32.GetCurrentThreadId()
-			winUser.user32.AttachThreadInput(curThreadID, document.windowThreadID, True)
-			winUser.user32.SetFocus(document.windowHandle)
-			winUser.user32.AttachThreadInput(curThreadID, document.windowThreadID, False)
+			curThreadID = winBindings.kernel32.GetCurrentThreadId()
+			user32.AttachThreadInput(curThreadID, document.windowThreadID, True)
+			user32.SetFocus(document.windowHandle)
+			user32.AttachThreadInput(curThreadID, document.windowThreadID, False)
 			if not document.WinwordWindowObject.active:
 				document.WinwordWindowObject.activate()

```