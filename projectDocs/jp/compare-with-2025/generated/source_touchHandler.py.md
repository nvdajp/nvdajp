# Diff for: `source\touchHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\touchHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\touchHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\touchHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\touchHandler.py"
index 05ccd4e..df15267 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\touchHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\touchHandler.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2012-2023 NV Access Limited, Joseph Lee, Babbage B.V.
+# Copyright (C) 2012-2025 NV Access Limited, Joseph Lee, Babbage B.V.
 
 """handles touchscreen interaction.
 Used to provide input gestures for touchscreens, touch modes and other support facilities.
@@ -9,12 +9,32 @@
 """
 
 import threading
-from ctypes import *  # noqa: F403
-from ctypes import windll
-from ctypes.wintypes import *  # noqa: F403
+from ctypes import (
+	byref,
+	Structure,
+	c_void_p,
+	sizeof,
+	cast,
+	c_int,
+	c_uint32,
+	c_uint64,
+)
+from ctypes.wintypes import (
+	LPCWSTR,
+	HANDLE,
+	HWND,
+	DWORD,
+	POINT,
+	MSG,
+	RECT,
+)
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
@@ -22,6 +42,16 @@
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
@@ -31,7 +61,6 @@
 	"object": _("object mode"),
 }
 
-SM_MAXIMUMTOUCHES = 95
 HWND_MESSAGE = -3
 
 WM_QUIT = 18
@@ -66,35 +95,35 @@
 POINTER_MESSAGE_FLAG_CANCELED = 0x400
 
 
-class POINTER_INFO(Structure):  # noqa: F405
+class POINTER_INFO(Structure):
 	_fields_ = [
-		("pointerType", DWORD),  # noqa: F405
-		("pointerId", c_uint32),  # noqa: F405
-		("frameId", c_uint32),  # noqa: F405
-		("pointerFlags", c_uint32),  # noqa: F405
-		("sourceDevice", HANDLE),  # noqa: F405
-		("hwndTarget", HWND),  # noqa: F405
-		("ptPixelLocation", POINT),  # noqa: F405
-		("ptHimetricLocation", POINT),  # noqa: F405
-		("ptPixelLocationRaw", POINT),  # noqa: F405
-		("ptHimetricLocationRaw", POINT),  # noqa: F405
-		("dwTime", DWORD),  # noqa: F405
-		("historyCount", c_uint32),  # noqa: F405
-		("inputData", c_int),  # noqa: F405
-		("dwKeyStates", DWORD),  # noqa: F405
-		("PerformanceCount", c_uint64),  # noqa: F405
+		("pointerType", DWORD),
+		("pointerId", c_uint32),
+		("frameId", c_uint32),
+		("pointerFlags", c_uint32),
+		("sourceDevice", HANDLE),
+		("hwndTarget", HWND),
+		("ptPixelLocation", POINT),
+		("ptHimetricLocation", POINT),
+		("ptPixelLocationRaw", POINT),
+		("ptHimetricLocationRaw", POINT),
+		("dwTime", DWORD),
+		("historyCount", c_uint32),
+		("inputData", c_int),
+		("dwKeyStates", DWORD),
+		("PerformanceCount", c_uint64),
 	]
 
 
-class POINTER_TOUCH_INFO(Structure):  # noqa: F405
+class POINTER_TOUCH_INFO(Structure):
 	_fields_ = [
 		("pointerInfo", POINTER_INFO),
-		("touchFlags", c_uint32),  # noqa: F405
-		("touchMask", c_uint32),  # noqa: F405
-		("rcContact", RECT),  # noqa: F405
-		("rcContactRaw", RECT),  # noqa: F405
-		("orientation", c_uint32),  # noqa: F405
-		("pressure", c_uint32),  # noqa: F405
+		("touchFlags", c_uint32),
+		("touchMask", c_uint32),
+		("rcContact", RECT),
+		("rcContactRaw", RECT),
+		("orientation", c_uint32),
+		("pressure", c_uint32),
 	]
 
 
@@ -115,7 +144,7 @@ class TouchInputGesture(inputCore.InputGesture):
 	* Hover: a finger is still touching the screen, and may be moving around. Only the most recent finger to be hovering causes these gestures.
 	* Hover up: a finger that was classed as a hover, releases contact with the screen.
 	All actions accept for Hover down, Hover and Hover up, can be made up of multiple fingers. It is possible to have things such as a 3-finger tap, or a 2-finger Tap and Hold, or a 4 finger Flick right.
-	Taps maybe pluralized (I.e. a tap very quickly followed by another tap of the same number of fingers will be represented by a double tap, rather than two separate taps). Currently double, tripple and quadruple plural taps are detected.
+	Taps maybe pluralized (I.e. a tap very quickly followed by another tap of the same number of fingers will be represented by a double tap, rather than two separate taps). Currently double, triple and quadruple plural taps are detected.
 	Tap and holds can be pluralized also (E.g. a double tap and hold means that there were two taps before the hold).
 	Actions also communicate if other fingers are currently held while performing the action. E.g. a hold+tap is when a finger touches the screen long enough to become a hover, and a tap with another finger is performed, while the first finger remains on the screen. Holds themselves also can be made of multiple fingers.
 	Based on all of this, gestures could be as complicated as a 5-finger hold + 5-finger quadruple tap and hold.
@@ -124,7 +153,7 @@ class TouchInputGesture(inputCore.InputGesture):
 	See touchHandler.MultitouchTracker for definitions of the available properties.
 	"""
 
-	counterNames = ["single", "double", "tripple", "quodruple"]
+	counterNames = ["single", "double", "triple", "quadruple"]
 
 	pluralActionLabels = {
 		# Translators: a touch screen action performed once
@@ -132,9 +161,9 @@ class TouchInputGesture(inputCore.InputGesture):
 		# Translators: a touch screen action performed twice
 		"double": _("double {action}"),
 		# Translators: a touch screen action performed 3 times
-		"tripple": _("tripple {action}"),
+		"triple": _("triple {action}"),
 		# Translators: a touch screen action performed 4 times
-		"quodruple": _("quadruple {action}"),
+		"quadruple": _("quadruple {action}"),
 	}
 
 	def _get_speechEffectWhenExecuted(self):
@@ -229,24 +258,24 @@ def __init__(self):
 			raise self.threadExc
 
 	def terminate(self):
-		windll.user32.PostThreadMessageW(self.ident, WM_QUIT, 0, 0)
+		user32.PostThreadMessage(self.ident, WM_QUIT, 0, 0)
 		self.join()
 		self.pendingEmitsTimer.Stop()
 
 	def run(self):
 		try:
-			self._appInstance = windll.kernel32.GetModuleHandleW(None)
-			self._cInputTouchWindowProc = winUser.WNDPROC(self.inputTouchWndProc)
-			self._wc = winUser.WNDCLASSEXW(
-				cbSize=sizeof(winUser.WNDCLASSEXW),  # noqa: F405
+			self._appInstance = winBindings.kernel32.GetModuleHandle(None)
+			self._cInputTouchWindowProc = user32.WNDPROC(self.inputTouchWndProc)
+			self._wc = user32.WNDCLASSEXW(
+				cbSize=sizeof(user32.WNDCLASSEXW),
 				lpfnWndProc=self._cInputTouchWindowProc,
 				hInstance=self._appInstance,
 				lpszClassName="inputTouchWindowClass",
-			)  # noqa: F405
-			self._wca = windll.user32.RegisterClassExW(byref(self._wc))  # noqa: F405
-			self._touchWindow = windll.user32.CreateWindowExW(
+			)
+			self._wca = user32.RegisterClassEx(byref(self._wc))
+			self._touchWindow = user32.CreateWindowEx(
 				0,
-				self._wca,
+				cast(self._wca, LPCWSTR),
 				"NVDA touch input",
 				0,
 				0,
@@ -258,12 +287,12 @@ def run(self):
 				self._appInstance,
 				None,
 			)
-			windll.user32.RegisterPointerInputTarget(self._touchWindow, PT_TOUCH)
-			oledll.oleacc.AccSetRunningUtilityState(  # noqa: F405
+			user32.RegisterPointerInputTarget(self._touchWindow, PT_TOUCH)
+			winBindings.oleacc.AccSetRunningUtilityState(
 				self._touchWindow,
 				ANRUS_TOUCH_MODIFICATION_ACTIVE,
 				ANRUS_TOUCH_MODIFICATION_ACTIVE,
-			)  # noqa: F405
+			)
 			self.trackerManager = touchTracker.TrackerManager()
 			self.screenExplorer = screenExplorer.ScreenExplorer()
 			self.screenExplorer.updateReview = True
@@ -271,14 +300,15 @@ def run(self):
 			self.threadExc = e
 		finally:
 			self.initializedEvent.set()
-		msg = MSG()  # noqa: F405
-		while windll.user32.GetMessageW(byref(msg), None, 0, 0):  # noqa: F405
-			windll.user32.TranslateMessage(byref(msg))  # noqa: F405
-			windll.user32.DispatchMessageW(byref(msg))  # noqa: F405
-		oledll.oleacc.AccSetRunningUtilityState(self._touchWindow, ANRUS_TOUCH_MODIFICATION_ACTIVE, 0)  # noqa: F405
-		windll.user32.UnregisterPointerInputTarget(self._touchWindow, PT_TOUCH)
-		windll.user32.DestroyWindow(self._touchWindow)
-		windll.user32.UnregisterClassW(self._wca, self._appInstance)
+		msg = MSG()
+		while user32.GetMessage(byref(msg), None, 0, 0):
+			user32.TranslateMessage(byref(msg))
+			user32.DispatchMessage(byref(msg))
+		winBindings.oleacc.AccSetRunningUtilityState(self._touchWindow, ANRUS_TOUCH_MODIFICATION_ACTIVE, 0)
+		user32.UnregisterPointerInputTarget(self._touchWindow, PT_TOUCH)
+		user32.DestroyWindow(self._touchWindow)
+		# The class atom should be stored as the low word of the class name string pointer.
+		user32.UnregisterClass(cast(c_void_p(self._wca), LPCWSTR), self._appInstance)
 
 	def inputTouchWndProc(self, hwnd, msg, wParam, lParam):
 		if msg >= _WM_POINTER_FIRST and msg <= _WM_POINTER_LAST:
@@ -294,7 +324,7 @@ def inputTouchWndProc(self, hwnd, msg, wParam, lParam):
 				self.trackerManager.update(ID, x, y, True)
 				core.requestPump()
 			return 0
-		return windll.user32.DefWindowProcW(hwnd, msg, wParam, lParam)
+		return user32.DefWindowProc(hwnd, msg, wParam, lParam)
 
 	def setMode(self, mode):
 		if mode not in availableTouchModes:
@@ -322,7 +352,7 @@ def notifyInteraction(self, obj):
 		@param obj: The NVDAObject with which the user is interacting.
 		@type obj: L{NVDAObjects.NVDAObject}
 		"""
-		oledll.oleacc.AccNotifyTouchInteraction(  # noqa: F405
+		winBindings.oleacc.AccNotifyTouchInteraction(
 			gui.mainFrame.Handle,
 			obj.windowHandle,  # noqa: F405
 			obj.location.center.toPOINT(),
@@ -340,7 +370,7 @@ def touchSupported(debugLog: bool = False) -> bool:
 		if debugLog:
 			log.debugWarning("Touch only supported on installed copies")
 		return False
-	maxTouches = windll.user32.GetSystemMetrics(SM_MAXIMUMTOUCHES)
+	maxTouches = user32.GetSystemMetrics(SystemMetrics.MAXIMUM_TOUCHES)
 	if maxTouches <= 0:
 		if debugLog:
 			log.debugWarning("No touch devices found")
@@ -374,7 +404,8 @@ def initialize():
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