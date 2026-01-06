# Diff for: `source\winUser.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\winUser.py`  
**Current**: `F:\nvda\gh\alphajp\source\winUser.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\winUser.py" "b/F:\\nvda\\gh\\alphajp\\source\\winUser.py"
index b257590e2c..b13e989af1 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\winUser.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\winUser.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2006-2022 NV Access Limited, Babbage B.V.
+# Copyright (C) 2006-2025 NV Access Limited, Babbage B.V.
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -11,30 +11,120 @@
 
 import contextlib
 import ctypes
-from ctypes import *  # noqa: F403
-from ctypes import byref, WinError, Structure, c_int, c_char
-from ctypes.wintypes import *  # noqa: F403
-from ctypes.wintypes import HWND, RECT, DWORD
-from typing import (
-	Any,
-	Tuple,
+from ctypes import (
+	byref,
+	WinError,
+	Structure,
+	c_long,
+	c_short,
+	c_uint,
+	c_wchar,
+	create_unicode_buffer,
+	sizeof,
+	wstring_at,
+)
+from ctypes.wintypes import (
+	BOOL,
+	HWND,
+	POINT,
+	RECT,
+	DWORD,
+	WCHAR,
 )
 
+import winBindings.user32
+from winBindings import user32 as _user32
+from winBindings.user32 import (
+	WNDENUMPROC as _WNDENUMPROC,
+	PAINTSTRUCT as _PAINTSTRUCT,
+	GUITHREADINFO as _GUITHREADINFO,
+	INPUT,
+)
 import winKernel
+from collections.abc import Callable
 from textUtils import WCHAR_ENCODING
 import enum
-import NVDAState
-from logHandler import log
-
-# dll handles
-user32 = windll.user32  # noqa: F405
+from utils import _deprecate
+
+
+__getattr__ = _deprecate.handleDeprecations(
+	_deprecate.MovedSymbol(
+		"WNDCLASSEXW",
+		"winBindings.user32",
+	),
+	_deprecate.MovedSymbol(
+		"WNDPROC",
+		"winBindings.user32",
+	),
+	_deprecate.MovedSymbol(
+		"PAINTSTRUCT",
+		"winBindings.user32",
+	),
+	_deprecate.MovedSymbol(
+		"SM_CXSCREEN",
+		"winAPI.winUser.constants",
+		"SystemMetrics",
+		"CX_SCREEN",
+	),
+	_deprecate.MovedSymbol(
+		"SM_CYSCREEN",
+		"winAPI.winUser.constants",
+		"SystemMetrics",
+		"CY_SCREEN",
+	),
+	_deprecate.MovedSymbol(
+		"SM_SWAPBUTTON",
+		"winAPI.winUser.constants",
+		"SystemMetrics",
+		"SWAP_BUTTON",
+	),
+	_deprecate.MovedSymbol(
+		"SM_XVIRTUALSCREEN",
+		"winAPI.winUser.constants",
+		"SystemMetrics",
+		"X_VIRTUAL_SCREEN",
+	),
+	_deprecate.MovedSymbol(
+		"SM_YVIRTUALSCREEN",
+		"winAPI.winUser.constants",
+		"SystemMetrics",
+		"Y_VIRTUAL_SCREEN",
+	),
+	_deprecate.MovedSymbol(
+		"SM_CXVIRTUALSCREEN",
+		"winAPI.winUser.constants",
+		"SystemMetrics",
+		"CX_VIRTUAL_SCREEN",
+	),
+	_deprecate.MovedSymbol(
+		"SM_CYVIRTUALSCREEN",
+		"winAPI.winUser.constants",
+		"SystemMetrics",
+		"CY_VIRTUAL_SCREEN",
+	),
+	_deprecate.MovedSymbol(
+		"HWINEVENTHOOK",
+		"winBindings.user32",
+	),
+	_deprecate.MovedSymbol(
+		"WINEVENTPROC",
+		"winBindings.user32",
+	),
+	_deprecate.MovedSymbol("user32", "winBindings.user32", "dll"),
+	_deprecate.MovedSymbol("GUITHREADINFO", "winBindings.user32"),
+	_deprecate.MovedSymbol("Input", "winBindings.user32", "INPUT"),
+	_deprecate.MovedSymbol("KeyBdInput", "winBindings.user32", "KEYBDINPUT"),
+	_deprecate.MovedSymbol("HardwareInput", "winBindings.user32", "HARDWAREINPUT"),
+	_deprecate.MovedSymbol("MouseInput", "winBindings.user32", "MOUSEINPUT"),
+)
+"""Module __getattr__ to handle backward compatibility."""
 
 # rather than using the ctypes.c_void_p type, which may encourage attempting to dereference
 # what may be an invalid or illegal pointer, we'll treat it as an opaque value.
 HWNDVal = int
 
-LRESULT = c_long  # noqa: F405
-HCURSOR = c_long  # noqa: F405
+LRESULT = c_long
+HCURSOR = c_long
 
 # Standard window class stuff
 #: Redraws the entire window if a movement or size adjustment changes the width of the client area.
@@ -42,68 +132,12 @@
 #: Redraws the entire window if a movement or size adjustment changes the height of the client area.
 CS_VREDRAW = 0x0001
 
-WNDPROC = WINFUNCTYPE(LRESULT, HWND, c_uint, WPARAM, LPARAM)  # noqa: F405
-
-
-def __getattr__(attrName: str) -> Any:
-	"""Module level `__getattr__` used to preserve backward compatibility."""
-	from winAPI.winUser.constants import SystemMetrics
-
-	_deprecatedConstantsMap = {
-		"SM_CXSCREEN": SystemMetrics.CX_SCREEN,
-		"SM_CYSCREEN": SystemMetrics.CY_SCREEN,
-		"SM_SWAPBUTTON": SystemMetrics.SWAP_BUTTON,
-		"SM_XVIRTUALSCREEN": SystemMetrics.X_VIRTUAL_SCREEN,
-		"SM_YVIRTUALSCREEN": SystemMetrics.Y_VIRTUAL_SCREEN,
-		"SM_CXVIRTUALSCREEN": SystemMetrics.CX_VIRTUAL_SCREEN,
-		"SM_CYVIRTUALSCREEN": SystemMetrics.CY_VIRTUAL_SCREEN,
-	}
-	if attrName in _deprecatedConstantsMap and NVDAState._allowDeprecatedAPI():
-		replacementSymbol = _deprecatedConstantsMap[attrName]
-		log.warning(
-			f"Importing {attrName} from here is deprecated. "
-			f"Import {replacementSymbol.name} from winAPI.winUser.constants instead. ",
-		)
-		return replacementSymbol
-	raise AttributeError(f"module {repr(__name__)} has no attribute {repr(attrName)}")
-
-
-class WNDCLASSEXW(Structure):
-	_fields_ = [
-		("cbSize", c_uint),  # noqa: F405
-		("style", c_uint),  # noqa: F405
-		("lpfnWndProc", WNDPROC),
-		("cbClsExtra", c_int),
-		("cbWndExtra", c_int),
-		("hInstance", HINSTANCE),  # noqa: F405
-		("hIcon", HICON),  # noqa: F405
-		("HCURSOR", HCURSOR),
-		("hbrBackground", HBRUSH),  # noqa: F405
-		("lpszMenuName", LPWSTR),  # noqa: F405
-		("lpszClassName", LPWSTR),  # noqa: F405
-		("hIconSm", HICON),  # noqa: F405
-	]
-
 
 class NMHdrStruct(Structure):
 	_fields_ = [
 		("hwndFrom", HWND),
-		("idFrom", c_uint),  # noqa: F405
-		("code", c_uint),  # noqa: F405
-	]
-
-
-class GUITHREADINFO(Structure):
-	_fields_ = [
-		("cbSize", DWORD),
-		("flags", DWORD),
-		("hwndActive", HWND),
-		("hwndFocus", HWND),
-		("hwndCapture", HWND),
-		("hwndMenuOwner", HWND),
-		("hwndMoveSize", HWND),
-		("hwndCaret", HWND),
-		("rcCaret", RECT),
+		("idFrom", c_uint),
+		("code", c_uint),
 	]
 
 
@@ -154,6 +188,7 @@ class GUITHREADINFO(Structure):
 LBS_OWNERDRAWFIXED = 0x0010
 LBS_OWNERDRAWVARIABLE = 0x0020
 LBS_HASSTRINGS = 0x0040
+LBS_EXTENDEDSEL = 0x0800
 CBS_OWNERDRAWFIXED = 0x0010
 CBS_OWNERDRAWVARIABLE = 0x0020
 CBS_HASSTRINGS = 0x00200
@@ -428,12 +463,12 @@ class MSGFLT(enum.IntEnum):
 
 
 def setSystemScreenReaderFlag(val):
-	user32.SystemParametersInfoW(SPI_SETSCREENREADER, val, 0, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
+	_user32.SystemParametersInfo(SPI_SETSCREENREADER, val, 0, SPIF_UPDATEINIFILE | SPIF_SENDCHANGE)
 
 
 def getSystemScreenReaderFlag():
-	val = BOOL()  # noqa: F405
-	user32.SystemParametersInfoW(SPI_GETSCREENREADER, 0, byref(val), 0)
+	val = BOOL()
+	_user32.SystemParametersInfo(SPI_GETSCREENREADER, 0, byref(val), 0)
 	return bool(val.value)
 
 
@@ -458,11 +493,11 @@ def HIWORD(long):
 
 
 def GET_X_LPARAM(lp):
-	return c_short(LOWORD(lp)).value  # noqa: F405
+	return c_short(LOWORD(lp)).value
 
 
 def GET_Y_LPARAM(lp):
-	return c_short(HIWORD(lp)).value  # noqa: F405
+	return c_short(HIWORD(lp)).value
 
 
 def MAKELONG(lo, hi):
@@ -470,111 +505,106 @@ def MAKELONG(lo, hi):
 
 
 def waitMessage():
-	return user32.WaitMessage()
+	return _user32.WaitMessage()
 
 
 def getMessage(*args) -> int:
-	return user32.GetMessageW(*args)
+	return winBindings.user32.GetMessage(*args)
 
 
 def translateMessage(*args):
-	return user32.TranslateMessage(*args)
+	return _user32.TranslateMessage(*args)
 
 
 def dispatchMessage(*args):
-	return user32.DispatchMessageW(*args)
+	return _user32.DispatchMessage(*args)
 
 
 def peekMessage(*args):
 	try:
-		res = user32.PeekMessageW(*args)
+		res = _user32.PeekMessage(*args)
 	except:  # noqa: E722
 		res = 0
 	return res
 
 
 def registerWindowMessage(name):
-	return user32.RegisterWindowMessageW(name)
+	return _user32.RegisterWindowMessage(name)
 
 
 def getAsyncKeyState(v):
-	return user32.GetAsyncKeyState(v)
+	return _user32.GetAsyncKeyState(v)
 
 
 def getKeyState(v):
-	return user32.GetKeyState(v)
+	return _user32.GetKeyState(v)
 
 
 def isWindow(hwnd):
-	return user32.IsWindow(hwnd)
+	return _user32.IsWindow(hwnd)
 
 
 def isDescendantWindow(parentHwnd, childHwnd):
-	if (parentHwnd == childHwnd) or user32.IsChild(parentHwnd, childHwnd):
+	if (parentHwnd == childHwnd) or _user32.IsChild(parentHwnd, childHwnd):
 		return True
 	else:
 		return False
 
 
 def getForegroundWindow() -> HWNDVal:
-	return user32.GetForegroundWindow()
+	return _user32.GetForegroundWindow()
 
 
 def setForegroundWindow(hwnd):
-	user32.SetForegroundWindow(hwnd)
+	_user32.SetForegroundWindow(hwnd)
 
 
 def setFocus(hwnd):
-	user32.SetFocus(hwnd)
+	_user32.SetFocus(hwnd)
 
 
 def getDesktopWindow() -> HWNDVal:
-	return user32.GetDesktopWindow()
+	return _user32.GetDesktopWindow()
 
 
 def getControlID(hwnd):
-	return user32.GetWindowLongW(hwnd, GWL_ID)
+	return _user32.GetWindowLong(hwnd, GWL_ID)
 
 
 def getClientRect(hwnd):
 	r = RECT()
-	if not user32.GetClientRect(hwnd, byref(r)):
+	if not _user32.GetClientRect(hwnd, byref(r)):
 		raise WinError()
 	return r
 
 
-HWINEVENTHOOK = HANDLE  # noqa: F405
-
-WINEVENTPROC = WINFUNCTYPE(None, HWINEVENTHOOK, DWORD, HWND, c_long, c_long, DWORD, DWORD)  # noqa: F405
-
-
 def setWinEventHook(*args):
-	return user32.SetWinEventHook(*args)
+	return _user32.SetWinEventHook(*args)
 
 
 def unhookWinEvent(*args):
-	return user32.UnhookWinEvent(*args)
+	return _user32.UnhookWinEvent(*args)
 
 
 def sendMessage(hwnd, msg, param1, param2):
-	return user32.SendMessageW(hwnd, msg, param1, param2)
+	return _user32.SendMessage(hwnd, msg, param1, param2)
 
 
-def getWindowThreadProcessID(hwnd: HWNDVal) -> Tuple[int, int]:
+def getWindowThreadProcessID(hwnd: HWNDVal) -> tuple[int, int]:
 	"""Returns a tuple of (processID, threadID)"""
-	processID = c_int()
-	threadID = user32.GetWindowThreadProcessId(hwnd, byref(processID))
+	processID = DWORD()
+	threadID = _user32.GetWindowThreadProcessId(hwnd, byref(processID))
 	return (processID.value, threadID)
 
 
 def getClassName(window: HWNDVal) -> str:
-	buf = create_unicode_buffer(256)  # noqa: F405
-	user32.GetClassNameW(window, buf, 255)
+	buf = create_unicode_buffer(256)
+	_user32.GetClassName(window, buf, 255)
 	return buf.value
 
 
 def keybd_event(*args):
-	return user32.keybd_event(*args)
+	return _user32.keybd_event(*args)
 
 
 def mouse_event(*args):
@@ -582,105 +612,96 @@ def mouse_event(*args):
 	# i.e. events generated by calling this wrapper aren't ignored by NVDA.
 	# To generate mouse events that are ignored by NVDA,
 	# call L{mouseHandler.executeMouseEvent} instead.
-	return user32.mouse_event(*args)
+	return _user32.mouse_event(*args)
 
 
 def getAncestor(hwnd, flags):
-	return user32.GetAncestor(hwnd, flags)
-
-
-try:
-	# Windows >= Vista
-	_getCursorPos = user32.GetPhysicalCursorPos
-	_setCursorPos = user32.SetPhysicalCursorPos
-except AttributeError:
-	_getCursorPos = user32.GetCursorPos
-	_setCursorPos = user32.SetCursorPos
+	return _user32.GetAncestor(hwnd, flags)
 
 
 def setCursorPos(x, y):
-	_setCursorPos(x, y)
+	_user32.SetPhysicalCursorPos(x, y)
 
 
 def getCursorPos():
-	point = POINT()  # noqa: F405
-	_getCursorPos(byref(point))
+	point = POINT()
+	_user32.GetPhysicalCursorPos(byref(point))
 	return [point.x, point.y]
 
 
 def getCaretPos():
-	point = POINT()  # noqa: F405
-	user32.GetCaretPos(byref(point))
+	point = POINT()
+	_user32.GetCaretPos(byref(point))
 	return [point.x, point.y]
 
 
 def getTopWindow(hwnd):
-	return user32.GetTopWindow(hwnd)
+	return _user32.GetTopWindow(hwnd)
 
 
 def getWindowText(hwnd):
-	buf = create_unicode_buffer(1024)  # noqa: F405
-	user32.InternalGetWindowText(hwnd, buf, 1023)
+	buf = create_unicode_buffer(1024)
+	_user32.InternalGetWindowText(hwnd, buf, 1023)
 	return buf.value
 
 
 def getWindow(window, relation):
-	return user32.GetWindow(window, relation)
+	return _user32.GetWindow(window, relation)
 
 
 def isWindowVisible(window):
-	return bool(user32.IsWindowVisible(window))
+	return bool(_user32.IsWindowVisible(window))
 
 
 def isWindowEnabled(window):
-	return bool(user32.IsWindowEnabled(window))
+	return bool(_user32.IsWindowEnabled(window))
 
 
 def getGUIThreadInfo(threadID):
-	info = GUITHREADINFO(cbSize=sizeof(GUITHREADINFO))  # noqa: F405
-	user32.GetGUIThreadInfo(threadID, byref(info))
+	info = _GUITHREADINFO(cbSize=sizeof(_GUITHREADINFO))
+	_user32.GetGUIThreadInfo(threadID, byref(info))
 	return info
 
 
 def getWindowStyle(hwnd):
-	return user32.GetWindowLongW(hwnd, GWL_STYLE)
+	return _user32.GetWindowLong(hwnd, GWL_STYLE)
 
 
 def getExtendedWindowStyle(hwnd):
-	return user32.GetWindowLongW(hwnd, GWL_EXSTYLE)
+	return _user32.GetWindowLong(hwnd, GWL_EXSTYLE)
 
 
 def setExtendedWindowStyle(hwnd, exstyle):
-	return user32.SetWindowLongW(hwnd, GWL_EXSTYLE, exstyle)
+	return _user32.SetWindowLong(hwnd, GWL_EXSTYLE, exstyle)
 
 
 def SetLayeredWindowAttributes(hwnd, key, alpha, flags):
-	return user32.SetLayeredWindowAttributes(hwnd, key, alpha, flags)
+	return _user32.SetLayeredWindowAttributes(hwnd, key, alpha, flags)
 
 
 def getPreviousWindow(hwnd):
 	try:
-		return user32.GetWindow(hwnd, GW_HWNDPREV)
+		return _user32.GetWindow(hwnd, GW_HWNDPREV)
 	except WindowsError:
 		return 0
 
 
 def getKeyboardLayout(idThread=0):
-	return user32.GetKeyboardLayout(idThread)
+	return _user32.GetKeyboardLayout(idThread)
 
 
 def RedrawWindow(hwnd, rcUpdate, rgnUpdate, flags):
-	return user32.RedrawWindow(hwnd, byref(rcUpdate), rgnUpdate, flags)
+	return _user32.RedrawWindow(hwnd, byref(rcUpdate), rgnUpdate, flags)
 
 
 def getKeyNameText(scanCode, extended):
-	buf = create_unicode_buffer(32)  # noqa: F405
-	user32.GetKeyNameTextW((scanCode << 16) | (extended << 24), buf, 31)
+	buf = create_unicode_buffer(32)
+	_user32.GetKeyNameText((scanCode << 16) | (extended << 24), buf, 31)
 	return buf.value
 
 
 def FindWindow(className, windowName):
-	res = user32.FindWindowW(className, windowName)
+	res = _user32.FindWindow(className, windowName)
 	if res == 0:
 		raise WinError()
 	return res
@@ -695,41 +716,38 @@ def FindWindow(className, windowName):
 
 
 def MessageBox(hwnd, text, caption, type):
-	res = user32.MessageBoxW(hwnd, text, caption, type)
+	res = _user32.MessageBox(hwnd, text, caption, type)
 	if res == 0:
 		raise WinError()
 	return res
 
 
 def PostMessage(hwnd, msg, wParam, lParam):
-	if not user32.PostMessageW(hwnd, msg, wParam, lParam):
+	if not _user32.PostMessage(hwnd, msg, wParam, lParam):
 		raise WinError()
 
 
-user32.VkKeyScanExW.restype = SHORT  # noqa: F405
-
-
 def VkKeyScanEx(ch, hkl):
-	res = user32.VkKeyScanExW(WCHAR(ch), hkl)  # noqa: F405
+	res = _user32.VkKeyScanEx(WCHAR(ch), hkl)
 	if res == -1:
 		raise LookupError
 	return res >> 8, res & 0xFF
 
 
 def ScreenToClient(hwnd, x, y):
-	point = POINT(x, y)  # noqa: F405
-	user32.ScreenToClient(hwnd, byref(point))
+	point = POINT(x, y)
+	_user32.ScreenToClient(hwnd, byref(point))
 	return point.x, point.y
 
 
 def ClientToScreen(hwnd, x, y):
-	point = POINT(x, y)  # noqa: F405
-	user32.ClientToScreen(hwnd, byref(point))
+	point = POINT(x, y)
+	_user32.ClientToScreen(hwnd, byref(point))
 	return point.x, point.y
 
 
 def NotifyWinEvent(event, hwnd, idObject, idChild):
-	user32.NotifyWinEvent(event, hwnd, idObject, idChild)
+	_user32.NotifyWinEvent(event, hwnd, idObject, idChild)
 
 
 class STICKYKEYS(Structure):
@@ -739,7 +757,7 @@ class STICKYKEYS(Structure):
 	)
 
 	def __init__(self, **kwargs):
-		super(STICKYKEYS, self).__init__(cbSize=sizeof(self), **kwargs)  # noqa: F405
+		super(STICKYKEYS, self).__init__(cbSize=sizeof(self), **kwargs)
 
 
 SKF_STICKYKEYSON = 0x00000001
@@ -750,58 +768,11 @@ def __init__(self, **kwargs):
 
 def getSystemStickyKeys():
 	sk = STICKYKEYS()
-	user32.SystemParametersInfoW(SPI_GETSTICKYKEYS, 0, byref(sk), 0)
+	_user32.SystemParametersInfo(SPI_GETSTICKYKEYS, 0, byref(sk), 0)
 	return sk
 
 
 # START SENDINPUT TYPE DECLARATIONS
-PUL = POINTER(c_ulong)  # noqa: F405
-
-
-class KeyBdInput(Structure):
-	_fields_ = [
-		("wVk", c_ushort),  # noqa: F405
-		("wScan", c_ushort),  # noqa: F405
-		("dwFlags", c_ulong),  # noqa: F405
-		("time", c_ulong),  # noqa: F405
-		("dwExtraInfo", PUL),
-	]
-
-
-class HardwareInput(Structure):
-	_fields_ = [
-		("uMsg", c_ulong),  # noqa: F405
-		("wParamL", c_short),  # noqa: F405
-		("wParamH", c_ushort),  # noqa: F405
-	]  # noqa: F405
-
-
-class MouseInput(Structure):
-	_fields_ = [
-		("dx", c_long),  # noqa: F405
-		("dy", c_long),  # noqa: F405
-		("mouseData", c_ulong),  # noqa: F405
-		("dwFlags", c_ulong),  # noqa: F405
-		("time", c_ulong),  # noqa: F405
-		("dwExtraInfo", PUL),
-	]
-
-
-class Input_I(Union):  # noqa: F405
-	_fields_ = [
-		("ki", KeyBdInput),
-		("mi", MouseInput),
-		("hi", HardwareInput),
-	]
-
-
-class Input(Structure):
-	_fields_ = [
-		("type", c_ulong),  # noqa: F405
-		("ii", Input_I),
-	]
-
-
 INPUT_MOUSE = 0  # The event is a mouse event. Use the mi structure of the union.
 INPUT_KEYBOARD = 1  # The event is a keyboard event. Use the ki structure of the union.
 KEYEVENTF_KEYUP = 0x0002
@@ -811,39 +782,28 @@ class Input(Structure):
 
 def SendInput(inputs):
 	n = len(inputs)
-	arr = (Input * n)(*inputs)
-	user32.SendInput(n, arr, sizeof(Input))  # noqa: F405
-
-
-class PAINTSTRUCT(Structure):
-	_fields_ = [
-		("hdc", c_int),
-		("fErase", c_int),
-		("rcPaint", RECT),
-		("fRestore", c_int),
-		("fIncUpdate", c_int),
-		("rgbReserved", c_char * 32),
-	]
+	arr = (INPUT * n)(*inputs)
+	_user32.SendInput(n, arr, sizeof(INPUT))
 
 
 @contextlib.contextmanager
-def paint(hwnd: int, paintStruct: PAINTSTRUCT | None = None):
+def paint(hwnd: int, paintStruct: _PAINTSTRUCT | None = None):
 	"""
 	Context manager that wraps BeginPaint and EndPaint.
 	:param painStruct: The paint structure used in the call to BeginPaint.
 		if None (default), an empty structure is provided.
 	"""
 	if paintStruct is None:
-		paintStruct = PAINTSTRUCT()
-	elif not isinstance(paintStruct, PAINTSTRUCT):
+		paintStruct = _PAINTSTRUCT()
+	elif not isinstance(paintStruct, _PAINTSTRUCT):
 		raise TypeError("Provided paintStruct is not of type PAINTSTRUCT")
-	hdc = user32.BeginPaint(hwnd, byref(paintStruct))
+	hdc = winBindings.user32.BeginPaint(hwnd, byref(paintStruct))
 	if hdc == 0:
 		raise WinError()
 	try:
 		yield hdc
 	finally:
-		user32.EndPaint(hwnd, byref(paintStruct))
+		winBindings.user32.EndPaint(hwnd, byref(paintStruct))
 
 
 class WinTimer(object):
@@ -860,8 +820,15 @@ def __init__(self, hwnd, idEvent, elapse, timerFunc=None):
 		self.hwnd = hwnd
 		self.idEvent = idEvent
 		self.elapse = elapse
-		self.timerFunc = timerFunc
-		self.ident = user32.SetTimer(hwnd, idEvent, elapse, timerFunc)
+		# ensure timerFunc is a TIMERPROC, or is converted to a TIMERPROC,
+		# and ensuring that None is handled as the correctly typed null function pointer.
+		if isinstance(timerFunc, winBindings.user32.TIMERPROC):
+			self.timerFunc = timerFunc
+		elif timerFunc is None:
+			self.timerFunc = winBindings.user32.TIMERPROC(0)
+		else:
+			self.timerFunc = winBindings.user32.TIMERPROC(timerFunc)
+		self.ident = _user32.SetTimer(hwnd, idEvent, elapse, self.timerFunc)
 		if self.ident == 0:
 			raise WinError()
 		if not hwnd:
@@ -874,7 +841,7 @@ def terminate(self):
 		"""Terminates the timer.
 		This should be called from the thread that initiated the timer.
 		"""
-		if not user32.KillTimer(self.hwnd, self.idEvent):
+		if not _user32.KillTimer(self.hwnd, self.idEvent):
 			raise WinError()
 
 
@@ -888,17 +855,17 @@ def openClipboard(hwndOwner=None):
 	A context manager version of OpenClipboard from user32.
 	Use as the expression of a 'with' statement, and CloseClipboard will automatically be called at the end.
 	"""
-	if not windll.user32.OpenClipboard(hwndOwner):  # noqa: F405
-		raise ctypes.WinError()  # noqa: F405
+	if not winBindings.user32.OpenClipboard(hwndOwner):
+		raise ctypes.WinError()
 	try:
 		yield
 	finally:
-		windll.user32.CloseClipboard()  # noqa: F405
+		winBindings.user32.CloseClipboard()
 
 
 def emptyClipboard():
-	if not windll.user32.EmptyClipboard():  # noqa: F405
-		raise ctypes.WinError()  # noqa: F405
+	if not _user32.EmptyClipboard():
+		raise ctypes.WinError()
 
 
 def getClipboardData(format):
@@ -906,15 +873,15 @@ def getClipboardData(format):
 	if format != CF_UNICODETEXT:
 		raise ValueError("Unsupported format")
 	# Fetch the data from the clipboard as a global memory handle
-	h = windll.user32.GetClipboardData(format)  # noqa: F405
+	h = winBindings.user32.GetClipboardData(format)
 	if not h:
-		raise ctypes.WinError()  # noqa: F405
+		raise ctypes.WinError()
 	# Lock the global memory  while we fetch the unicode string
 	# But make sure not to free the memory accidentally -- it is not ours
 	h = winKernel.HGLOBAL(h, autoFree=False)
 	with h.lock() as addr:
 		# Read the string from the local memory address
-		return wstring_at(addr)  # noqa: F405
+		return wstring_at(addr)
 
 
 def setClipboardData(format, data):
@@ -928,10 +895,45 @@ def setClipboardData(format, data):
 	# Acquire a lock to the global memory receiving a local memory address
 	with h.lock() as addr:
 		# Write the text into the allocated memory
-		buf = (c_wchar * bufLen).from_address(addr)  # noqa: F405
+		buf = (c_wchar * bufLen).from_address(addr)
 		buf.value = text
 	# Set the clipboard data with the global memory
-	if not windll.user32.SetClipboardData(format, h):  # noqa: F405
-		raise ctypes.WinError()  # noqa: F405
+	if not winBindings.user32.SetClipboardData(format, h):
+		raise ctypes.WinError()
 	# NULL the global memory handle so that it is not freed at the end of scope as the clipboard now has it.
 	h.forget()
+
+
+def findTopLevelWindow(predicate: Callable[[int], bool]) -> int | None:
+	"""
+	Find the first top-level window that matches the given predicate.
+
+	:param predicate: A callable that takes a window handle (hWnd) as an integer
+		and returns True if the window matches the search criteria, False otherwise
+	:returns: The handle of the first matching top-level window, or None if no
+		matching window is found
+	:raises ctypes.WinError: If the Windows API call fails
+	"""
+	found = None
+
+	@_WNDENUMPROC
+	def enumWindowsProc(hWnd: int, _lParam: int) -> int:
+		"""
+		Callback function for enumerating windows.
+
+		This function is called for each top-level window on the screen during enumeration.
+		It checks if the window matches the predicate criteria and stops enumeration when found.
+
+		:param hWnd: Handle to the window being enumerated
+		:param _lParam: Application-defined value passed to the enumeration function (unused)
+		:return: 0 to stop enumeration when window is found, 1 to continue enumeration
+		"""
+		if predicate(hWnd):
+			nonlocal found
+			found = hWnd
+			return 0
+		return 1
+
+	if not winBindings.user32.EnumWindows(enumWindowsProc, 0) and (error := ctypes.get_last_error()):
+		raise ctypes.WinError(error)
+	return found

```