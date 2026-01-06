# Diff for: `source\IAccessibleHandler\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\IAccessibleHandler\__init__.py`  
**Current**: `F:\nvda\gh\alphajp\source\IAccessibleHandler\__init__.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\IAccessibleHandler\\__init__.py" "b/F:\\nvda\\gh\\alphajp\\source\\IAccessibleHandler\\__init__.py"
index dba8e98fbd..e9884e4290 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\IAccessibleHandler\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\IAccessibleHandler\\__init__.py"
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
@@ -33,6 +35,8 @@
 from ctypes.wintypes import HANDLE
 from comtypes import IUnknown, IServiceProvider, COMError
 import comtypes.client
+import winBindings.kernel32
+import winBindings.ole32
 import oleacc
 import JABHandler
 import UIAHandler
@@ -228,6 +232,7 @@
 	oleacc.STATE_SYSTEM_PROTECTED: controlTypes.State.PROTECTED,
 	oleacc.STATE_SYSTEM_SELECTABLE: controlTypes.State.SELECTABLE,
 	oleacc.STATE_SYSTEM_FOCUSABLE: controlTypes.State.FOCUSABLE,
+	oleacc.STATE_SYSTEM_MULTISELECTABLE: controlTypes.State.MULTISELECTABLE,
 }
 
 IAccessible2StatesToNVDAStates = {
@@ -549,7 +554,7 @@ def winEventToNVDAEvent(  # noqa: C901
 			)
 		return None
 	# Make sure this window does not have a ghost window if possible
-	if NVDAObjects.window.GhostWindowFromHungWindow and NVDAObjects.window.GhostWindowFromHungWindow(window):
+	if user32._GhostWindowFromHungWindow is not None and user32._GhostWindowFromHungWindow(window):
 		if isMSAADebugLoggingEnabled():
 			log.debug(
 				f"Ghosted hung window. Dropping winEvent {getWinEventLogInfo(window, objectID, childID, eventID)}",
@@ -781,9 +786,9 @@ def processDesktopSwitchWinEvent(window, objectID, childID):
 		log.debug(
 			f"Processing desktopSwitch winEvent: {getWinEventLogInfo(window, objectID, childID)}",
 		)
-	hDesk = windll.user32.OpenInputDesktop(0, False, 0)
+	hDesk = user32.OpenInputDesktop(0, False, 0)
 	if hDesk != 0:
-		windll.user32.CloseDesktop(hDesk)
+		user32.CloseDesktop(hDesk)
 		core.callLater(200, _handleUserDesktop)
 	else:
 		# When hDesk == 0, the active desktop has changed.
@@ -1120,7 +1125,7 @@ def getIAccIdentity(pacc, childID):
 			d["windowHandle"] = fields[1]
 		return d
 	finally:
-		windll.ole32.CoTaskMemFree(stringPtr)
+		winBindings.ole32.CoTaskMemFree(stringPtr)
 
 
 def findGroupboxObject(obj):
@@ -1303,5 +1308,5 @@ def isMarshalledIAccessible(IAccessibleObject):
 	)
 	handle = HANDLE()
 	windll.kernel32.GetModuleHandleExW(6, addr, byref(handle))
-	windll.kernel32.GetModuleFileNameW(handle, buf, 1024)
+	winBindings.kernel32.GetModuleFileName(handle, buf, 1024)
 	return not buf.value.lower().endswith("oleacc.dll")

```