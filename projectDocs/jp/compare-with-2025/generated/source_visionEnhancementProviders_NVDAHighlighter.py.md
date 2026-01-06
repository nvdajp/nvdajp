# Diff for: `source\visionEnhancementProviders\NVDAHighlighter.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\visionEnhancementProviders\NVDAHighlighter.py`  
**Current**: `F:\nvda\gh\alphajp\source\visionEnhancementProviders\NVDAHighlighter.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\visionEnhancementProviders\\NVDAHighlighter.py" "b/F:\\nvda\\gh\\alphajp\\source\\visionEnhancementProviders\\NVDAHighlighter.py"
index 64e73b91d9..e8e5f4e23b 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\visionEnhancementProviders\\NVDAHighlighter.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\visionEnhancementProviders\\NVDAHighlighter.py"
@@ -14,6 +14,7 @@
 from vision.util import getContextRect
 from vision.visionHandlerExtensionPoints import EventExtensionPoints
 from vision import providerBase
+from winBindings import user32
 from windowUtils import CustomWindow
 import wx
 from gui.settingsDialogs import (
@@ -109,8 +110,8 @@ def updateLocationForDisplays(self):
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
@@ -120,7 +121,7 @@ def updateLocationForDisplays(self):
 			winUser.SWP_NOACTIVATE,
 		):
 			raise WinError()
-		winUser.user32.ShowWindow(self.handle, winUser.SW_SHOWNA)
+		user32.ShowWindow(self.handle, winUser.SW_SHOWNA)
 
 	def __init__(self, highlighter):
 		if vision._isDebug():
@@ -139,14 +140,14 @@ def __init__(self, highlighter):
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
@@ -156,7 +157,7 @@ def windowProc(self, hwnd, msg, wParam, lParam):
 				winUser.SWP_NOACTIVATE | winUser.SWP_NOMOVE | winUser.SWP_NOSIZE,
 			)
 		elif msg == winUser.WM_DESTROY:
-			winUser.user32.PostQuitMessage(0)
+			user32.PostQuitMessage(0)
 		elif msg == winUser.WM_TIMER:
 			self.refresh()
 		elif msg == WindowMessage.DISPLAY_CHANGE:
@@ -167,7 +168,7 @@ def _paint(self):
 		highlighter = self.highlighterRef()
 		if not highlighter:
 			# The highlighter instance died unexpectedly, kill the window as well
-			winUser.user32.PostQuitMessage(0)
+			user32.PostQuitMessage(0)
 			return
 		contextRects = {}
 		for context in highlighter.enabledContexts:
@@ -209,7 +210,7 @@ def _paint(self):
 						winGDI.gdiPlusDrawRectangle(graphicsContext, pen, *rect.toLTWH())
 
 	def refresh(self):
-		winUser.user32.InvalidateRect(self.handle, None, True)
+		user32.InvalidateRect(self.handle, None, True)
 
 
 _contextOptionLabelsWithAccelerators = {
@@ -440,7 +441,7 @@ def __init__(self):
 	def terminate(self):
 		log.debug("Terminating NVDAHighlighter")
 		if self._highlighterThread and self._window and self._window.handle:
-			if not winUser.user32.PostThreadMessageW(self._highlighterThread.ident, winUser.WM_QUIT, 0, 0):
+			if not user32.PostThreadMessage(self._highlighterThread.ident, winUser.WM_QUIT, 0, 0):
 				raise WinError()
 			else:
 				self._highlighterThread.join()
@@ -459,8 +460,8 @@ def _run(self):
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