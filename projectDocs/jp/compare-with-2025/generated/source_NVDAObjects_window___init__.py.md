# Diff for: `source\NVDAObjects\window\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\window\__init__.py`  
**Current**: `F:\nvda\gh\alphajp\source\NVDAObjects\window\__init__.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\window\\__init__.py" "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\window\\__init__.py"
index 222281f2e3..9cb10ead33 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\window\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\window\\__init__.py"
@@ -1,11 +1,13 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2006-2023 NV Access Limited, Babbage B.V., Bill Dengler, Cyrille Bougot
+# Copyright (C) 2006-2025 NV Access Limited, Babbage B.V., Bill Dengler, Cyrille Bougot
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
 import re
 import ctypes
 import ctypes.wintypes
+from winBindings import user32
+from winBindings.user32 import _GhostWindowFromHungWindow
 import winKernel
 import winUser
 from logHandler import log  # noqa: F401
@@ -23,16 +25,11 @@
 re_WindowsForms = re.compile(r"^WindowsForms[0-9]*\.(.*)\.app\..*$")
 re_ATL = re.compile(r"^ATL:(.*)$")
 
-try:
-	GhostWindowFromHungWindow = ctypes.windll.user32.GhostWindowFromHungWindow
-except AttributeError:
-	GhostWindowFromHungWindow = None
-
 
 def isUsableWindow(windowHandle):
-	if not ctypes.windll.user32.IsWindowVisible(windowHandle):
+	if not user32.IsWindowVisible(windowHandle):
 		return False
-	if GhostWindowFromHungWindow and ctypes.windll.user32.GhostWindowFromHungWindow(windowHandle):
+	if _GhostWindowFromHungWindow is not None and _GhostWindowFromHungWindow(windowHandle):
 		return False
 	return True
 
@@ -60,14 +57,6 @@ def __del__(self):
 		winKernel.closeHandle(self.processHandle)
 
 
-# We want to work with physical points.
-try:
-	# Windows >= Vista
-	_windowFromPoint = ctypes.windll.user32.WindowFromPhysicalPoint
-except AttributeError:
-	_windowFromPoint = ctypes.windll.user32.WindowFromPoint
-
-
 class Window(NVDAObject):
 	"""
 	An NVDAObject for a window
@@ -91,7 +80,7 @@ def getPossibleAPIClasses(cls, kwargs, relation=None):
 		if windowClassName == "#32769":
 			return
 		# If this window has a ghost window its too dangerous to try any higher APIs
-		if GhostWindowFromHungWindow and GhostWindowFromHungWindow(windowHandle):
+		if _GhostWindowFromHungWindow is not None and _GhostWindowFromHungWindow(windowHandle):
 			return
 		if windowClassName == "EXCEL7" and (relation == "focus" or isinstance(relation, tuple)):
 			from . import excel
@@ -169,7 +158,7 @@ def kwargsFromSuper(cls, kwargs, relation=None):
 				if threadInfo.hwndFocus:
 					windowHandle = threadInfo.hwndFocus
 		elif isinstance(relation, tuple):
-			windowHandle = _windowFromPoint(ctypes.wintypes.POINT(relation[0], relation[1]))
+			windowHandle = user32.WindowFromPhysicalPoint(ctypes.wintypes.POINT(relation[0], relation[1]))
 		if not windowHandle:
 			return False
 		kwargs["windowHandle"] = windowHandle
@@ -207,7 +196,7 @@ def _get_windowControlID(self):
 
 	def _get_location(self):
 		r = ctypes.wintypes.RECT()
-		ctypes.windll.user32.GetWindowRect(self.windowHandle, ctypes.byref(r))
+		user32.GetWindowRect(self.windowHandle, ctypes.byref(r))
 		return RectLTWH.fromCompatibleType(r)
 
 	def _get_displayText(self):
@@ -310,7 +299,7 @@ def _get_extendedWindowStyle(self):
 
 	def _get_isWindowUnicode(self):
 		if not hasattr(self, "_isWindowUnicode"):
-			self._isWindowUnicode = bool(ctypes.windll.user32.IsWindowUnicode(self.windowHandle))
+			self._isWindowUnicode = bool(user32.IsWindowUnicode(self.windowHandle))
 		return self._isWindowUnicode
 
 	def correctAPIForRelation(self, obj, relation=None):

```