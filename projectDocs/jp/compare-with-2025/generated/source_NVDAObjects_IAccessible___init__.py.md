# Diff for: `source\NVDAObjects\IAccessible\__init__.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\IAccessible\__init__.py`  
**Current**: `F:\nvda\gh\alphajp\source\NVDAObjects\IAccessible\__init__.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\IAccessible\\__init__.py" "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\IAccessible\\__init__.py"
index 50b2d0d545..827371345c 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\IAccessible\\__init__.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\IAccessible\\__init__.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2006-2024 NV Access Limited, Babbage B.V., Cyrille Bougot
+# Copyright (C) 2006-2025 NV Access Limited, Babbage B.V., Cyrille Bougot
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -40,6 +40,8 @@
 import IAccessibleHandler
 import oleacc
 import JABHandler
+from winBindings import user32
+import winBindings.ole32
 import winUser
 import globalVars  # noqa: F401
 from logHandler import log
@@ -298,12 +300,12 @@ def expand(self, unit):
 			try:
 				# Shrink the start to the nearest embedded object before our origin.
 				self._startOffset = textStart + text.rindex(textUtils.OBJ_REPLACEMENT_CHAR, 0, relativeOrigin)
-			except (ValueError, AttributeError):
+			except ValueError:
 				pass
 			try:
 				# Shrink the end to the nearest embedded object after our origin.
 				self._endOffset = textStart + text.index(textUtils.OBJ_REPLACEMENT_CHAR, relativeOrigin)
-			except (ValueError, AttributeError):
+			except ValueError:
 				pass
 
 	def _getCaretOffset(self):
@@ -511,6 +513,10 @@ class IAccessible(Window):
 	@type IAccessibleChildID: int
 	"""
 
+	# For Windowless RichEdit.
+	# https://learn.microsoft.com/en-us/windows/win32/api/textserv/nl-textserv-itextservices
+	IID_ITextServices = GUID("{8D33F740-CF58-11CE-A89D-00AA006CADC5}")
+
 	IAccessibleTableUsesTableCellIndexAttrib = (
 		False  #: Should the table-cell-index IAccessible2 object attribute be used rather than indexInParent?
 	)
@@ -714,6 +720,10 @@ def findOverlayClasses(self, clsList):
 			from . import webKit
 
 			webKit.findExtraOverlayClasses(self, clsList)
+		elif windowClassName == "wxWindowNR":
+			from . import wx as wxObjects
+
+			wxObjects.findExtraOverlayClasses(self, clsList)
 		elif windowClassName.startswith("Chrome_"):
 			from . import chromium
 
@@ -724,15 +734,6 @@ def findOverlayClasses(self, clsList):
 			winConsole.findExtraOverlayClasses(self, clsList)
 
 		# Support for Windowless richEdit
-		if not hasattr(IAccessible, "IID_ITextServices"):
-			try:
-				IAccessible.IID_ITextServices = ctypes.cast(
-					ctypes.windll.msftedit.IID_ITextServices,
-					ctypes.POINTER(GUID),
-				).contents
-			except WindowsError:
-				log.debugWarning("msftedit not available, couldn't retrieve IID_ITextServices")
-				IAccessible.IID_ITextServices = None
 		if IAccessible.IID_ITextServices:
 			try:
 				pDoc = self.IAccessibleObject.QueryInterface(IServiceProvider).QueryService(
@@ -813,7 +814,7 @@ def __init__(  # noqa: C901
 			log.debugWarning("Resorting to WindowFromPoint on accLocation")
 			try:
 				left, top, width, height = IAccessibleObject.accLocation(0)
-				windowHandle = winUser.user32.WindowFromPoint(winUser.POINT(left, top))
+				windowHandle = user32.WindowFromPoint(winUser.POINT(left, top))
 			except COMError as e:
 				log.debugWarning("accLocation failed: %s" % e)
 		if not windowHandle:
@@ -1084,15 +1085,15 @@ def _get_IAccessibleStates(self) -> int:
 			return 0
 		return res if isinstance(res, int) else 0
 
-	states: typing.Set[controlTypes.State]
+	states: set[controlTypes.State]
 	"""Type info for auto property: _get_states
 	"""
 
 	# C901 '_get_states' is too complex. Look for opportunities to break this method down.
-	def _get_states(self) -> typing.Set[controlTypes.State]:  # noqa: C901
+	def _get_states(self) -> set[controlTypes.State]:  # noqa: C901
 		states = set()
 		if self.event_objectID in (winUser.OBJID_CLIENT, winUser.OBJID_WINDOW) and self.event_childID == 0:
-			states.update(super(IAccessible, self).states)
+			states.update(super().states)
 		try:
 			IAccessibleStates = self.IAccessibleStates
 		except COMError:
@@ -1644,7 +1645,7 @@ def _tableHeaderTextHelper(self, axis):
 				ret.append(text)
 			return "\n".join(ret)
 		finally:
-			ctypes.windll.ole32.CoTaskMemFree(headers)
+			winBindings.ole32.CoTaskMemFree(headers)
 
 	def _get_rowHeaderText(self):
 		return self._tableHeaderTextHelper("row")
@@ -2438,6 +2439,12 @@ class List(IAccessible):
 	def _get_role(self):
 		return controlTypes.Role.LIST
 
+	def _get_states(self) -> set[controlTypes.State]:
+		states = super().states
+		if self.windowStyle & winUser.LBS_EXTENDEDSEL:
+			states.add(controlTypes.State.MULTISELECTABLE)
+		return states
+
 
 class SysLinkClient(IAccessible):
 	def reportFocus(self):

```