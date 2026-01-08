# Diff for: `source\visionEnhancementProviders\NVDAHighlighter.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\visionEnhancementProviders\NVDAHighlighter.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\visionEnhancementProviders\NVDAHighlighter.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\visionEnhancementProviders\\NVDAHighlighter.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\visionEnhancementProviders\\NVDAHighlighter.py"
index 64e73b9..ea881f6 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\visionEnhancementProviders\\NVDAHighlighter.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\visionEnhancementProviders\\NVDAHighlighter.py"
@@ -14,6 +14,7 @@
 from vision.util import getContextRect
 from vision.visionHandlerExtensionPoints import EventExtensionPoints
 from vision import providerBase
+from winBindings import user32
 from windowUtils import CustomWindow
 import wx
 from gui.settingsDialogs import (
@@ -23,7 +24,7 @@
 )
 import api
 from ctypes import byref, WinError
-from ctypes.wintypes import COLORREF, MSG
+from ctypes.wintypes import MSG
 import winUser
 from logHandler import log
 from mouseHandler import getTotalWidthAndHeightAndMinimumPosition
@@ -31,6 +32,7 @@
 from collections import namedtuple
 import threading
 from winAPI.messageWindow import WindowMessage
+import winBindings.gdi32
 import winGDI
 import weakref
 from colors import RGB
@@ -93,7 +95,7 @@ class HighlightWindow(CustomWindow):
 	def _get__wClass(cls):
 		wClass = super()._wClass
 		wClass.style = winUser.CS_HREDRAW | winUser.CS_VREDRAW
-		wClass.hbrBackground = winGDI.gdi32.CreateSolidBrush(COLORREF(cls.transparentColor))
+		wClass.hbrBackground = winBindings.gdi32.CreateSolidBrush(cls.transparentColor)
 		return wClass
 
 	def updateLocationForDisplays(self):
@@ -109,8 +111,8 @@ def updateLocationForDisplays(self):
 		width = screenWidth
 		height = screenHeight - 1
 		self.location = RectLTWH(left, top, width, height)
-		winUser.user32.ShowWindow(self.handle, winUser.SW_HIDE)
-		if not winUser.user32.SetWindowPos(
+		user32.ShowWindow(self.handle, winUser.SW_HIDE)
+		if not user32.SetWindowPos(
 			self.handle,
 			winUser.HWND_TOPMOST,
 			left,
@@ -120,7 +122,7 @@ def updateLocationForDisplays(self):
 			winUser.SWP_NOACTIVATE,
 		):
 			raise WinError()
-		winUser.user32.ShowWindow(self.handle, winUser.SW_SHOWNA)
+		user32.ShowWindow(self.handle, winUser.SW_SHOWNA)
 
 	def __init__(self, highlighter):
 		if vision._isDebug():
@@ -139,14 +141,14 @@ def __init__(self, highlighter):
 			winUser.LWA_ALPHA | winUser.LWA_COLORKEY,
 		)
 		self.updateLocationForDisplays()
-		if not winUser.user32.UpdateWindow(self.handle):
+		if not user32.UpdateWindow(self.handle):
 			raise WinError()
 
 	def windowProc(self, hwnd, msg, wParam, lParam):
 		if msg == winUser.WM_PAINT:
 			self._paint()
 			# Ensure the window is top most
-			winUser.user32.SetWindowPos(
+			user32.SetWindowPos(
 				self.handle,
 				winUser.HWND_TOPMOST,
 				0,
@@ -156,7 +158,7 @@ def windowProc(self, hwnd, msg, wParam, lParam):
 				winUser.SWP_NOACTIVATE | winUser.SWP_NOMOVE | winUser.SWP_NOSIZE,
 			)
 		elif msg == winUser.WM_DESTROY:
-			winUser.user32.PostQuitMessage(0)
+			user32.PostQuitMessage(0)
 		elif msg == winUser.WM_TIMER:
 			self.refresh()
 		elif msg == WindowMessage.DISPLAY_CHANGE:
@@ -167,7 +169,7 @@ def _paint(self):
 		highlighter = self.highlighterRef()
 		if not highlighter:
 			# The highlighter instance died unexpectedly, kill the window as well
-			winUser.user32.PostQuitMessage(0)
+			user32.PostQuitMessage(0)
 			return
 		contextRects = {}
 		for context in highlighter.enabledContexts:
@@ -209,7 +211,7 @@ def _paint(self):
 						winGDI.gdiPlusDrawRectangle(graphicsContext, pen, *rect.toLTWH())
 
 	def refresh(self):
-		winUser.user32.InvalidateRect(self.handle, None, True)
+		user32.InvalidateRect(self.handle, None, True)
 
 
 _contextOptionLabelsWithAccelerators = {
@@ -440,7 +442,7 @@ def __init__(self):
 	def terminate(self):
 		log.debug("Terminating NVDAHighlighter")
 		if self._highlighterThread and self._window and self._window.handle:
-			if not winUser.user32.PostThreadMessageW(self._highlighterThread.ident, winUser.WM_QUIT, 0, 0):
+			if not user32.PostThreadMessage(self._highlighterThread.ident, winUser.WM_QUIT, 0, 0):
 				raise WinError()
 			else:
 				self._highlighterThread.join()
@@ -459,8 +461,8 @@ def _run(self):
 			self._highlighterRunningEvent.set()  # notify main thread that initialisation was successful
 			msg = MSG()
 			while (res := winUser.getMessage(byref(msg), None, 0, 0)) > 0:
-				winUser.user32.TranslateMessage(byref(msg))
-				winUser.user32.DispatchMessageW(byref(msg))
+				user32.TranslateMessage(byref(msg))
+				user32.DispatchMessage(byref(msg))
 			if res == -1:
 				# See the return value section of
 				# https://docs.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-getmessage

```