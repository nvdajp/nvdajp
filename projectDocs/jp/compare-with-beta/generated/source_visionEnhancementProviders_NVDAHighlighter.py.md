# Diff for: `source\visionEnhancementProviders\NVDAHighlighter.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\visionEnhancementProviders\NVDAHighlighter.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\visionEnhancementProviders\NVDAHighlighter.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\visionEnhancementProviders\\NVDAHighlighter.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\visionEnhancementProviders\\NVDAHighlighter.py"
index ea881f6..e8e5f4e 100644
--- "a/F:\\nvda\\gh\\beta\\source\\visionEnhancementProviders\\NVDAHighlighter.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\visionEnhancementProviders\\NVDAHighlighter.py"
@@ -24,7 +24,7 @@
 )
 import api
 from ctypes import byref, WinError
-from ctypes.wintypes import MSG
+from ctypes.wintypes import COLORREF, MSG
 import winUser
 from logHandler import log
 from mouseHandler import getTotalWidthAndHeightAndMinimumPosition
@@ -32,7 +32,6 @@
 from collections import namedtuple
 import threading
 from winAPI.messageWindow import WindowMessage
-import winBindings.gdi32
 import winGDI
 import weakref
 from colors import RGB
@@ -95,7 +94,7 @@ class HighlightWindow(CustomWindow):
 	def _get__wClass(cls):
 		wClass = super()._wClass
 		wClass.style = winUser.CS_HREDRAW | winUser.CS_VREDRAW
-		wClass.hbrBackground = winBindings.gdi32.CreateSolidBrush(cls.transparentColor)
+		wClass.hbrBackground = winGDI.gdi32.CreateSolidBrush(COLORREF(cls.transparentColor))
 		return wClass
 
 	def updateLocationForDisplays(self):

```