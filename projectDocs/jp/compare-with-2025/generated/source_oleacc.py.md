# Diff for: `source\oleacc.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\oleacc.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\oleacc.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\oleacc.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\oleacc.py"
index 7b9a8d7..1c6168d 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\oleacc.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\oleacc.py"
@@ -5,12 +5,17 @@
 
 from ctypes import *  # noqa: F403
 from ctypes.wintypes import *  # noqa: F403
+from ctypes.wintypes import HWND
 from comtypes import *  # noqa: F403
 from comtypes.automation import *  # noqa: F403
 import comtypes.client
+from winBindings import user32
 import winUser
 import typing
 
+import winBindings.oleacc
+
+
 # Include functions from oleacc.dll in the module namespace.
 m = comtypes.client.GetModule("oleacc.dll")
 globals().update((key, val) for key, val in m.__dict__.items() if not key.startswith("_"))
@@ -174,7 +179,7 @@ def LresultFromObject(wParam, obj):
 	@rtype: int
 	"""
 	objIID = obj._iid_
-	return oledll.oleacc.LresultFromObject(byref(objIID), wParam, obj)  # noqa: F405
+	return winBindings.oleacc.LresultFromObject(byref(objIID), wParam, obj)  # noqa: F405
 
 
 def ObjectFromLresult(res, wParam, interface):
@@ -191,7 +196,7 @@ def ObjectFromLresult(res, wParam, interface):
 	@rtype: COMObject
 	"""
 	p = POINTER(interface)()  # noqa: F405
-	oledll.oleacc.ObjectFromLresult(res, byref(interface._iid_), wParam, byref(p))  # noqa: F405
+	winBindings.oleacc.ObjectFromLresult(res, byref(interface._iid_), wParam, byref(p))  # noqa: F405
 	return p
 
 
@@ -211,7 +216,7 @@ def CreateStdAccessibleProxy(hwnd, className, objectID, interface=IAccessible):
 	@rtype: COMObject
 	"""
 	p = POINTER(interface)()  # noqa: F405
-	oledll.oleacc.CreateStdAccessibleProxyW(hwnd, className, objectID, byref(interface._iid_), byref(p))  # noqa: F405
+	winBindings.oleacc.CreateStdAccessibleProxy(hwnd, className, objectID, byref(interface._iid_), byref(p))  # noqa: F405
 	return p
 
 
@@ -229,7 +234,7 @@ def CreateStdAccessibleObject(hwnd, objectID, interface=IAccessible):  # noqa: F
 	@rtype: COMObject
 	"""
 	p = POINTER(interface)()  # noqa: F405
-	oledll.oleacc.CreateStdAccessibleObject(hwnd, objectID, byref(interface._iid_), byref(p))  # noqa: F405
+	winBindings.oleacc.CreateStdAccessibleObject(hwnd, objectID, byref(interface._iid_), byref(p))  # noqa: F405
 	return p
 
 
@@ -246,7 +251,7 @@ def AccessibleObjectFromWindow(hwnd, objectID, interface=IAccessible):  # noqa:
 	@rtype: COMObject
 	"""
 	p = POINTER(interface)()  # noqa: F405
-	oledll.oleacc.AccessibleObjectFromWindow(hwnd, objectID, byref(p._iid_), byref(p))  # noqa: F405
+	winBindings.oleacc.AccessibleObjectFromWindow(hwnd, objectID, byref(p._iid_), byref(p))  # noqa: F405
 	return p
 
 
@@ -255,7 +260,7 @@ def AccessibleObjectFromWindow_safe(hwnd, objectID, interface=IAccessible, timeo
 		raise ValueError("Invalid window")
 	wmResult = c_long()  # noqa: F405
 	res = (
-		windll.user32.SendMessageTimeoutW(  # noqa: F405
+		user32.SendMessageTimeout(  # noqa: F405
 			hwnd,
 			winUser.WM_GETOBJECT,
 			0,
@@ -287,7 +292,7 @@ def AccessibleObjectFromEvent(hwnd, objectID, childID):
 	"""
 	p = POINTER(IAccessible)()  # noqa: F405
 	varChild = VARIANT()  # noqa: F405
-	oledll.oleacc.AccessibleObjectFromEvent(hwnd, objectID, childID, byref(p), byref(varChild))  # noqa: F405
+	winBindings.oleacc.AccessibleObjectFromEvent(hwnd, objectID, childID, byref(p), byref(varChild))  # noqa: F405
 	if varChild.vt == VT_I4:  # noqa: F405
 		childID = varChild.value
 	return (p, childID)
@@ -308,24 +313,23 @@ def AccessibleObjectFromEvent_safe(hwnd, objectID, childID, timeout=2):
 	return (obj, childID)
 
 
-def WindowFromAccessibleObject(pacc):
+def WindowFromAccessibleObject(pacc) -> int:
 	"""
-	Retreaves the handle of the window this IAccessible object belongs to.
-	@param pacc: the IAccessible object who's window you want to fetch.
-	@type pacc: POINTER(IAccessible)
-	@return: the window handle.
-	@rtype: int
+	Retrieves the handle of the window this IAccessible object belongs to.
+	:param pacc: the IAccessible object who's window you want to fetch.
+	:type pacc: POINTER(IAccessible)
+	:return: the window handle.
 	"""
-	hwnd = c_int()  # noqa: F405
-	oledll.oleacc.WindowFromAccessibleObject(pacc, byref(hwnd))  # noqa: F405
-	return hwnd.value
+	hwnd = HWND()
+	winBindings.oleacc.WindowFromAccessibleObject(pacc, byref(hwnd))  # noqa: F405
+	return hwnd.value or 0
 
 
 def AccessibleObjectFromPoint(x, y):
 	point = POINT(x, y)  # noqa: F405
 	pacc = POINTER(IAccessible)()  # noqa: F405
 	varChild = VARIANT()  # noqa: F405
-	oledll.oleacc.AccessibleObjectFromPoint(point, byref(pacc), byref(varChild))  # noqa: F405
+	winBindings.oleacc.AccessibleObjectFromPoint(point, byref(pacc), byref(varChild))  # noqa: F405
 	if not isinstance(varChild.value, int):
 		child = 0
 	else:
@@ -336,36 +340,34 @@ def AccessibleObjectFromPoint(x, y):
 def AccessibleChildren(pacc, iChildStart, cChildren):
 	varChildren = (VARIANT * cChildren)()  # noqa: F405
 	pcObtained = c_int()  # noqa: F405
-	oledll.oleacc.AccessibleChildren(pacc, iChildStart, cChildren, byref(varChildren), byref(pcObtained))  # noqa: F405
+	winBindings.oleacc.AccessibleChildren(pacc, iChildStart, cChildren, varChildren, byref(pcObtained))  # noqa: F405
 	return [x.value for x in varChildren[0 : pcObtained.value]]
 
 
-def GetProcessHandleFromHwnd(windowHandle):
+def GetProcessHandleFromHwnd(windowHandle: int) -> int:
 	"""Retrieves a process handle of the process who owns the window.
 	This uses GetProcessHandleFromHwnd found in oleacc.dll which allows a client with UIAccess to open a process that is elevated.
-	@param windowHandle: a window of a process you wish to retreave a process handle for
-	@type windowHandle: integer
-	@returns: a process handle with read, write and operation access
-	@rtype: integer
+	:param windowHandle: a window of a process you wish to retrieve a process handle for
+	:returns: a process handle with read, write and operation access
 	"""
-	return oledll.oleacc.GetProcessHandleFromHwnd(windowHandle)  # noqa: F405
+	return winBindings.oleacc.GetProcessHandleFromHwnd(windowHandle) or 0
 
 
 def GetRoleText(role):
-	textLen = oledll.oleacc.GetRoleTextW(role, 0, 0)  # noqa: F405
+	textLen = winBindings.oleacc.GetRoleText(role, 0, 0)
 	if textLen:
 		buf = create_unicode_buffer(textLen + 2)  # noqa: F405
-		oledll.oleacc.GetRoleTextW(role, buf, textLen + 1)  # noqa: F405
+		winBindings.oleacc.GetRoleText(role, buf, textLen + 1)
 		return buf.value
 	else:
 		return None
 
 
 def GetStateText(state):
-	textLen = oledll.oleacc.GetStateTextW(state, 0, 0)  # noqa: F405
+	textLen = winBindings.oleacc.GetStateText(state, 0, 0)
 	if textLen:
 		buf = create_unicode_buffer(textLen + 2)  # noqa: F405
-		oledll.oleacc.GetStateTextW(state, buf, textLen + 1)  # noqa: F405
+		winBindings.oleacc.GetStateText(state, buf, textLen + 1)
 		return buf.value
 	else:
 		return None

```