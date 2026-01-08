# Diff for: `source\IAccessibleHandler\__init__.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\IAccessibleHandler\__init__.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\IAccessibleHandler\__init__.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\IAccessibleHandler\\__init__.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\IAccessibleHandler\\__init__.py"
index dba8e98..8e7e93b 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\IAccessibleHandler\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\IAccessibleHandler\\__init__.py"
@@ -1,10 +1,12 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2006-2022 NV Access Limited, Łukasz Golonka, Leonard de Ruijter
+# Copyright (C) 2006-2025 NV Access Limited, Łukasz Golonka, Leonard de Ruijter
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
 import typing
 
+from winBindings import user32
+
 # F401 imported but unused. RelationType should be exposed from IAccessibleHandler, in future __all__
 # should be used to export it.
 from .types import RelationType  # noqa: F401
@@ -21,7 +23,6 @@
 import weakref
 from ctypes import (
 	wintypes,
-	windll,
 	byref,
 	c_void_p,
 	c_char,
@@ -33,6 +34,8 @@
 from ctypes.wintypes import HANDLE
 from comtypes import IUnknown, IServiceProvider, COMError
 import comtypes.client
+import winBindings.kernel32
+import winBindings.ole32
 import oleacc
 import JABHandler
 import UIAHandler
@@ -228,6 +231,7 @@
 	oleacc.STATE_SYSTEM_PROTECTED: controlTypes.State.PROTECTED,
 	oleacc.STATE_SYSTEM_SELECTABLE: controlTypes.State.SELECTABLE,
 	oleacc.STATE_SYSTEM_FOCUSABLE: controlTypes.State.FOCUSABLE,
+	oleacc.STATE_SYSTEM_MULTISELECTABLE: controlTypes.State.MULTISELECTABLE,
 }
 
 IAccessible2StatesToNVDAStates = {
@@ -365,10 +369,11 @@ def accessibleObjectFromPoint(x, y):
 	return normalizeIAccessible(pacc, child), child
 
 
-def windowFromAccessibleObject(ia):
+def windowFromAccessibleObject(ia) -> int:
 	try:
 		return oleacc.WindowFromAccessibleObject(ia)
-	except:  # noqa: E722 Bare except
+	except WindowsError:
+		log.debugWarning("windowFromAccessibleObject failed", exc_info=True)
 		return 0
 
 
@@ -549,7 +554,7 @@ def winEventToNVDAEvent(  # noqa: C901
 			)
 		return None
 	# Make sure this window does not have a ghost window if possible
-	if NVDAObjects.window.GhostWindowFromHungWindow and NVDAObjects.window.GhostWindowFromHungWindow(window):
+	if user32._GhostWindowFromHungWindow is not None and user32._GhostWindowFromHungWindow(window):
 		if isMSAADebugLoggingEnabled():
 			log.debug(
 				f"Ghosted hung window. Dropping winEvent {getWinEventLogInfo(window, objectID, childID, eventID)}",
@@ -597,20 +602,15 @@ def winEventToNVDAEvent(  # noqa: C901
 	return (NVDAEventName, obj)
 
 
-def processGenericWinEvent(eventID, window, objectID, childID):
+def processGenericWinEvent(eventID: int, window: int, objectID: int, childID: int) -> bool:
 	"""Converts the win event to an NVDA event,
 	Checks to see if this NVDAObject  equals the current focus.
 	If all goes well, then the event is queued and we return True
-	@param eventID: a win event ID (type)
-	@type eventID: integer
-	@param window: a win event's window handle
-	@type window: integer
-	@param objectID: a win event's object ID
-	@type objectID: integer
-	@param childID: a win event's child ID
-	@type childID: integer
-	@returns: True if the event was processed, False otherwise.
-	@rtype: boolean
+	:param eventID: a win event ID (type)
+	:param window: a win event's window handle
+	:param objectID: a win event's object ID
+	:param childID: a win event's child ID
+	:return: True if the event was processed, False otherwise.
 	"""
 	if isMSAADebugLoggingEnabled():
 		log.debug(
@@ -676,19 +676,15 @@ def processGenericWinEvent(eventID, window, objectID, childID):
 	return True
 
 
-def processFocusWinEvent(window, objectID, childID, force=False):
+def processFocusWinEvent(window: int, objectID: int, childID: int, force: bool = False) -> bool:
 	"""checks to see if the focus win event is not the same as the existing focus,
 	then converts the win event to an NVDA event (instantiating an NVDA Object) then calls
 	processFocusNVDAEvent. If all is ok it returns True.
-	@type window: integer
-	@param objectID: a win event's object ID
-	@type objectID: integer
-	@param childID: a win event's child ID
-	@type childID: integer
-	@param force: If True, the shouldAllowIAccessibleFocusEvent property of the object is ignored.
-	@type force: boolean
-	@returns: True if the focus is valid and was handled, False otherwise.
-	@rtype: boolean
+	:param window: a win event's window handle
+	:param objectID: a win event's object ID
+	:param childID: a win event's child ID
+	:param force: If True, the shouldAllowIAccessibleFocusEvent property of the object is ignored.
+	:return: True if the focus is valid and was handled, False otherwise.
 	"""
 	if isMSAADebugLoggingEnabled():
 		log.debug(
@@ -774,20 +770,20 @@ def processFocusNVDAEvent(obj, force=False):
 	return True
 
 
-def processDesktopSwitchWinEvent(window, objectID, childID):
+def processDesktopSwitchWinEvent(window: int, objectID: int, childID: int) -> None:
 	from winAPI.secureDesktop import _handleSecureDesktopChange
 
 	if isMSAADebugLoggingEnabled():
 		log.debug(
 			f"Processing desktopSwitch winEvent: {getWinEventLogInfo(window, objectID, childID)}",
 		)
-	hDesk = windll.user32.OpenInputDesktop(0, False, 0)
-	if hDesk != 0:
-		windll.user32.CloseDesktop(hDesk)
+	hDesk = user32.OpenInputDesktop(0, False, 0)
+	if hDesk is not None:
+		user32.CloseDesktop(hDesk)
 		core.callLater(200, _handleUserDesktop)
 	else:
-		# When hDesk == 0, the active desktop has changed.
-		# This is usually means the secure desktop has been launched,
+		# When hDesk == None, the active desktop has changed.
+		# This usually means the secure desktop has been launched,
 		# but the new desktop can also be a secondary desktop created through the Windows API.
 		# https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-createdesktopa
 		# This secondary desktop has some bugs, and as such is not properly supported (#14395).
@@ -1022,7 +1018,9 @@ def pumpAll():  # noqa: C901
 		alwaysAllowedObjects.append((focus.event_windowHandle, focus.event_objectID, focus.event_childID))
 
 	# Receive all the winEvents from the limiter for this cycle
-	winEvents = internalWinEventHandler.winEventLimiter.flushEvents(alwaysAllowedObjects)
+	winEvents: list[tuple[int, int, int, int]] = internalWinEventHandler.winEventLimiter.flushEvents(
+		alwaysAllowedObjects,
+	)
 
 	for winEvent in winEvents:
 		isEventOnCaret = winEvent[2] == winUser.OBJID_CARET
@@ -1120,7 +1118,7 @@ def getIAccIdentity(pacc, childID):
 			d["windowHandle"] = fields[1]
 		return d
 	finally:
-		windll.ole32.CoTaskMemFree(stringPtr)
+		winBindings.ole32.CoTaskMemFree(stringPtr)
 
 
 def findGroupboxObject(obj):
@@ -1302,6 +1300,6 @@ def isMarshalledIAccessible(IAccessibleObject):
 		.contents.value
 	)
 	handle = HANDLE()
-	windll.kernel32.GetModuleHandleExW(6, addr, byref(handle))
-	windll.kernel32.GetModuleFileNameW(handle, buf, 1024)
+	winBindings.kernel32.GetModuleHandleEx(6, addr, byref(handle))
+	winBindings.kernel32.GetModuleFileName(handle, buf, 1024)
 	return not buf.value.lower().endswith("oleacc.dll")

```