# Diff for: `source\windowUtils.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\windowUtils.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\windowUtils.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\windowUtils.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\windowUtils.py"
index f1776cb..59f5cd5 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\windowUtils.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\windowUtils.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2013-2023 NV Access Limited, Bill Dengler
+# Copyright (C) 2013-2025 NV Access Limited, Bill Dengler
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -10,13 +10,19 @@
 """
 
 import ctypes
+import ctypes.wintypes
 import weakref
+import winBindings.kernel32
+import winBindings.user32
+import winBindings.gdi32
 import winUser
-from winUser import WNDCLASSEXW, WNDPROC
+from winBindings.user32 import WNDCLASSEXW, WNDPROC
 from logHandler import log
 from abc import abstractmethod
 from baseObject import AutoPropertyObject
 from typing import Optional
+from winBindings import user32
+
 
 WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.wintypes.BOOL, ctypes.wintypes.HWND, ctypes.wintypes.LPARAM)
 
@@ -49,28 +55,13 @@ def callback(window, data):
 			return False
 		return True
 
-	ctypes.windll.user32.EnumChildWindows(parent, callback, 0)
+	user32.EnumChildWindows(parent, callback, 0)
 	try:
 		return result[0]
 	except IndexError:
 		raise LookupError("No matching descendant window found")
 
 
-try:
-	# Windows >= 8.1
-	_logicalToPhysicalPoint = ctypes.windll.user32.LogicalToPhysicalPointForPerMonitorDPI
-	_physicalToLogicalPoint = ctypes.windll.user32.PhysicalToLogicalPointForPerMonitorDPI
-except AttributeError:
-	try:
-		# Windows Vista..Windows 8
-		_logicalToPhysicalPoint = ctypes.windll.user32.LogicalToPhysicalPoint
-		_physicalToLogicalPoint = ctypes.windll.user32.PhysicalToLogicalPoint
-	except AttributeError:
-		# Windows <= XP
-		_logicalToPhysicalPoint = None
-		_physicalToLogicalPoint = None
-
-
 def logicalToPhysicalPoint(window, x, y):
 	"""Converts the logical coordinates of a point in a window to physical coordinates.
 	This should be used when points are received directly from a window that is not DPI aware.
@@ -82,10 +73,8 @@ def logicalToPhysicalPoint(window, x, y):
 	@return: The physical x and y coordinates.
 	@rtype: tuple of (int, int)
 	"""
-	if not _logicalToPhysicalPoint:
-		return x, y
 	point = ctypes.wintypes.POINT(x, y)
-	_logicalToPhysicalPoint(window, ctypes.byref(point))
+	user32.LogicalToPhysicalPointForPerMonitorDPI(window, ctypes.byref(point))
 	return point.x, point.y
 
 
@@ -100,10 +89,8 @@ def physicalToLogicalPoint(window, x, y):
 	@return: The logical x and y coordinates.
 	@rtype: tuple of (int, int)
 	"""
-	if not _physicalToLogicalPoint:
-		return x, y
 	point = ctypes.wintypes.POINT(x, y)
-	_physicalToLogicalPoint(window, ctypes.byref(point))
+	user32.PhysicalToLogicalPointForPerMonitorDPI(window, ctypes.byref(point))
 	return point.x, point.y
 
 
@@ -119,13 +106,12 @@ def getWindowScalingFactor(window: int) -> int:
 	percentage in the windows display settings. 100% is typically 96 DPI, 150% is typically 144 DPI.
 	@param window: a native Windows window handle (hWnd)
 	@returns the logical scaling factor. EG. 1.0 if the window DPI level is 96, 1.5 if the window DPI level is 144"""
-	user32 = ctypes.windll.user32
 	try:
 		winDpi: int = user32.GetDpiForWindow(window)
 	except:  # noqa: E722
 		log.debug("GetDpiForWindow failed, using GetDeviceCaps instead")
 		dc = user32.GetDC(window)
-		winDpi: int = ctypes.windll.gdi32.GetDeviceCaps(dc, LOGPIXELSX)
+		winDpi: int = winBindings.gdi32.GetDeviceCaps(dc, LOGPIXELSX)
 		ret = user32.ReleaseDC(window, dc)
 		if ret != 1:
 			log.error("Unable to release the device context.")
@@ -144,7 +130,7 @@ def getWindowScalingFactor(window: int) -> int:
 	return round(winDpi / DEFAULT_DPI_LEVEL)
 
 
-appInstance = ctypes.windll.kernel32.GetModuleHandleW(None)
+appInstance = winBindings.kernel32.GetModuleHandle(None)
 
 
 class CustomWindow(AutoPropertyObject):
@@ -212,12 +198,13 @@ def __init__(
 			raise TypeError("extendedWindowStyle must be an integer")
 		if parent and not isinstance(parent, int):
 			raise TypeError("parent must be an integer")
-		res = self._classAtom = ctypes.windll.user32.RegisterClassExW(ctypes.byref(self._wClass))
+		res = self._classAtom = winBindings.user32.RegisterClassEx(ctypes.byref(self._wClass))
 		if res == 0:
 			raise ctypes.WinError()
-		res = ctypes.windll.user32.CreateWindowExW(
+		res = winBindings.user32.CreateWindowEx(
 			extendedWindowStyle,
-			self._classAtom,
+			# The class atom should be stored as the low word of the class name string pointer.
+			ctypes.cast(ctypes.c_void_p(self._classAtom), ctypes.wintypes.LPCWSTR),
 			windowName or self.className,
 			windowStyle,
 			0,
@@ -240,13 +227,17 @@ def destroy(self):
 		This will be called automatically when this instance is deleted,
 		but you may wish to call it earlier.
 		"""
-		if not ctypes.windll.user32.DestroyWindow(self.handle):
+		if not user32.DestroyWindow(self.handle):
 			log.error(
 				f"Error destroying window for {self.__class__.__qualname__}",
 				exc_info=ctypes.WinError(),
 			)
 		self.handle = None
-		if not ctypes.windll.user32.UnregisterClassW(self._classAtom, appInstance):
+		if not winBindings.user32.UnregisterClass(
+			# The class atom should be stored as the low word of the class name string pointer.
+			ctypes.cast(ctypes.c_void_p(self._classAtom), ctypes.wintypes.LPCWSTR),
+			appInstance,
+		):
 			log.error(
 				f"Error unregistering window class for {self.__class__.__qualname__}",
 				exc_info=ctypes.WinError(),
@@ -281,11 +272,11 @@ def _rawWindowProc(hwnd, msg, wParam, lParam):
 			inst = CustomWindow._hwndsToInstances[hwnd]
 		except KeyError:
 			log.debug("CustomWindow rawWindowProc called for unknown window %d" % hwnd)
-			return ctypes.windll.user32.DefWindowProcW(hwnd, msg, wParam, lParam)
+			return user32.DefWindowProc(hwnd, msg, wParam, lParam)
 		try:
 			res = inst.windowProc(hwnd, msg, wParam, lParam)
 			if res is not None:
 				return res
 		except:  # noqa: E722
 			log.exception("Error in wndProc")
-		return ctypes.windll.user32.DefWindowProcW(hwnd, msg, wParam, lParam)
+		return user32.DefWindowProc(hwnd, msg, wParam, lParam)

```