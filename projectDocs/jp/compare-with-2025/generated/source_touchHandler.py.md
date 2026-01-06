# Diff for: `source\touchHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\touchHandler.py`  
**Current**: `F:\nvda\gh\alphajp\source\touchHandler.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\touchHandler.py" "b/F:\\nvda\\gh\\alphajp\\source\\touchHandler.py"
index 05ccd4ee87..8859368502 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\touchHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\touchHandler.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2012-2023 NV Access Limited, Joseph Lee, Babbage B.V.
+# Copyright (C) 2012-2025 NV Access Limited, Joseph Lee, Babbage B.V.
 
 """handles touchscreen interaction.
 Used to provide input gestures for touchscreens, touch modes and other support facilities.
@@ -10,11 +10,16 @@
 
 import threading
 from ctypes import *  # noqa: F403
-from ctypes import windll
+from ctypes import cast
 from ctypes.wintypes import *  # noqa: F403
+from ctypes.wintypes import LPCWSTR
 import re
+from winAPI.winUser.constants import SystemMetrics
+import winBindings.kernel32
+from winBindings import user32
 import gui
 import config
+import winBindings.oleacc
 import winUser
 import inputCore
 import screenExplorer
@@ -22,6 +27,16 @@
 import touchTracker
 import core
 import systemUtils
+from utils import _deprecate
+
+__getattr__ = _deprecate.handleDeprecations(
+	_deprecate.MovedSymbol(
+		"SM_MAXIMUMTOUCHES",
+		"winAPI.winUser.constants",
+		"SystemMetrics",
+		"MAXIMUM_TOUCHES",
+	),
+)
 
 
 availableTouchModes = ["text", "object"]
@@ -31,7 +46,6 @@
 	"object": _("object mode"),
 }
 
-SM_MAXIMUMTOUCHES = 95
 HWND_MESSAGE = -3
 
 WM_QUIT = 18
@@ -229,13 +243,13 @@ def __init__(self):
 			raise self.threadExc
 
 	def terminate(self):
-		windll.user32.PostThreadMessageW(self.ident, WM_QUIT, 0, 0)
+		user32.PostThreadMessage(self.ident, WM_QUIT, 0, 0)
 		self.join()
 		self.pendingEmitsTimer.Stop()
 
 	def run(self):
 		try:
-			self._appInstance = windll.kernel32.GetModuleHandleW(None)
+			self._appInstance = winBindings.kernel32.GetModuleHandle(None)
 			self._cInputTouchWindowProc = winUser.WNDPROC(self.inputTouchWndProc)
 			self._wc = winUser.WNDCLASSEXW(
 				cbSize=sizeof(winUser.WNDCLASSEXW),  # noqa: F405
@@ -243,10 +257,10 @@ def run(self):
 				hInstance=self._appInstance,
 				lpszClassName="inputTouchWindowClass",
 			)  # noqa: F405
-			self._wca = windll.user32.RegisterClassExW(byref(self._wc))  # noqa: F405
-			self._touchWindow = windll.user32.CreateWindowExW(
+			self._wca = winBindings.user32.RegisterClassEx(byref(self._wc))  # noqa: F405
+			self._touchWindow = winBindings.user32.CreateWindowEx(
 				0,
-				self._wca,
+				cast(self._wca, LPCWSTR),
 				"NVDA touch input",
 				0,
 				0,
@@ -258,8 +272,8 @@ def run(self):
 				self._appInstance,
 				None,
 			)
-			windll.user32.RegisterPointerInputTarget(self._touchWindow, PT_TOUCH)
-			oledll.oleacc.AccSetRunningUtilityState(  # noqa: F405
+			user32.RegisterPointerInputTarget(self._touchWindow, PT_TOUCH)
+			winBindings.oleacc.AccSetRunningUtilityState(  # noqa: F405
 				self._touchWindow,
 				ANRUS_TOUCH_MODIFICATION_ACTIVE,
 				ANRUS_TOUCH_MODIFICATION_ACTIVE,
@@ -272,13 +286,13 @@ def run(self):
 		finally:
 			self.initializedEvent.set()
 		msg = MSG()  # noqa: F405
-		while windll.user32.GetMessageW(byref(msg), None, 0, 0):  # noqa: F405
-			windll.user32.TranslateMessage(byref(msg))  # noqa: F405
-			windll.user32.DispatchMessageW(byref(msg))  # noqa: F405
-		oledll.oleacc.AccSetRunningUtilityState(self._touchWindow, ANRUS_TOUCH_MODIFICATION_ACTIVE, 0)  # noqa: F405
-		windll.user32.UnregisterPointerInputTarget(self._touchWindow, PT_TOUCH)
-		windll.user32.DestroyWindow(self._touchWindow)
-		windll.user32.UnregisterClassW(self._wca, self._appInstance)
+		while winBindings.user32.GetMessage(byref(msg), None, 0, 0):  # noqa: F405
+			user32.TranslateMessage(byref(msg))  # noqa: F405
+			user32.DispatchMessage(byref(msg))  # noqa: F405
+		winBindings.oleacc.AccSetRunningUtilityState(self._touchWindow, ANRUS_TOUCH_MODIFICATION_ACTIVE, 0)  # noqa: F405
+		user32.UnregisterPointerInputTarget(self._touchWindow, PT_TOUCH)
+		user32.DestroyWindow(self._touchWindow)
+		winBindings.user32.UnregisterClass(self._wca, self._appInstance)
 
 	def inputTouchWndProc(self, hwnd, msg, wParam, lParam):
 		if msg >= _WM_POINTER_FIRST and msg <= _WM_POINTER_LAST:
@@ -294,7 +308,7 @@ def inputTouchWndProc(self, hwnd, msg, wParam, lParam):
 				self.trackerManager.update(ID, x, y, True)
 				core.requestPump()
 			return 0
-		return windll.user32.DefWindowProcW(hwnd, msg, wParam, lParam)
+		return winBindings.user32.DefWindowProc(hwnd, msg, wParam, lParam)
 
 	def setMode(self, mode):
 		if mode not in availableTouchModes:
@@ -322,7 +336,7 @@ def notifyInteraction(self, obj):
 		@param obj: The NVDAObject with which the user is interacting.
 		@type obj: L{NVDAObjects.NVDAObject}
 		"""
-		oledll.oleacc.AccNotifyTouchInteraction(  # noqa: F405
+		winBindings.oleacc.AccNotifyTouchInteraction(  # noqa: F405
 			gui.mainFrame.Handle,
 			obj.windowHandle,  # noqa: F405
 			obj.location.center.toPOINT(),
@@ -340,7 +354,7 @@ def touchSupported(debugLog: bool = False) -> bool:
 		if debugLog:
 			log.debugWarning("Touch only supported on installed copies")
 		return False
-	maxTouches = windll.user32.GetSystemMetrics(SM_MAXIMUMTOUCHES)
+	maxTouches = user32.GetSystemMetrics(SystemMetrics.MAXIMUM_TOUCHES)
 	if maxTouches <= 0:
 		if debugLog:
 			log.debugWarning("No touch devices found")
@@ -374,7 +388,8 @@ def initialize():
 	if not touchSupported(debugLog=True):
 		raise NotImplementedError
 	log.debug(
-		"Touchscreen detected, maximum touch inputs: %d" % winUser.user32.GetSystemMetrics(SM_MAXIMUMTOUCHES),
+		"Touchscreen detected, maximum touch inputs: %d"
+		% user32.GetSystemMetrics(SystemMetrics.MAXIMUM_TOUCHES),
 	)
 	config.post_configProfileSwitch.register(handlePostConfigProfileSwitch)
 	setTouchSupport(config.conf["touch"]["enabled"])

```