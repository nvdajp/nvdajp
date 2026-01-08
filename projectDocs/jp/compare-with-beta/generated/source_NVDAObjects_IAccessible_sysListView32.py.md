# Diff for: `source\NVDAObjects\IAccessible\sysListView32.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\NVDAObjects\IAccessible\sysListView32.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAObjects\IAccessible\sysListView32.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\IAccessible\\sysListView32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\sysListView32.py"
index 3ed2abb..a62b3bd 100644
--- "a/F:\\nvda\\gh\\beta\\source\\NVDAObjects\\IAccessible\\sysListView32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\sysListView32.py"
@@ -8,7 +8,6 @@
 import ctypes
 from ctypes.wintypes import *  # noqa: F403
 from comtypes import BSTR
-from enum import IntFlag
 import NVDAHelper
 import watchdog
 import controlTypes
@@ -23,7 +22,6 @@
 from locationHelper import RectLTRB
 from logHandler import log
 from typing import Optional
-from utils import _deprecate
 
 # Window messages
 LVM_FIRST = 0x1000
@@ -68,49 +66,9 @@
 LVIS_SELECTED = 0x02
 LVIS_STATEIMAGEMASK = 0xF000
 
-
-class ListViewWindowStyle(IntFlag):
-	"""Window styles  specific to list-view controls.
-
-	.. seealso::
-		https://learn.microsoft.com/en-us/windows/win32/controls/list-view-window-styles
-	"""
-
-	REPORT = 0x0001
-	"""This style specifies report view."""
-	TYPEMASK = 0x0003
-	"""Determines the control's current window style."""
-	SINGLESEL = 0x0004
-	"""Only one item at a time can be selected.
-	By default, multiple items may be selected."""
-	OWNERDRAWFIXED = 0x0400
-	"""The owner window can paint items in report view."""
-
-
-__getattr__ = _deprecate.handleDeprecations(
-	_deprecate.MovedSymbol(
-		"LVS_REPORT",
-		__name__,
-		"ListViewWindowStyle",
-		"REPORT",
-		"value",
-	),
-	_deprecate.MovedSymbol(
-		"LVS_TYPEMASK",
-		__name__,
-		"ListViewWindowStyle",
-		"TYPEMASK",
-		"value",
-	),
-	_deprecate.MovedSymbol(
-		"LVS_OWNERDRAWFIXED",
-		__name__,
-		"ListViewWindowStyle",
-		"OWNERDRAWFIXED",
-		"value",
-	),
-)
-
+LVS_REPORT = 0x0001
+LVS_TYPEMASK = 0x0003
+LVS_OWNERDRAWFIXED = 0x0400
 
 # column mask flags
 LVCF_FMT = 1
@@ -279,7 +237,7 @@ def _get_isMultiColumn(self):
 			# #2673: This could indicate that LVM_GETVIEW is not supported (comctl32 < 6.0).
 			# Unfortunately, it could also indicate LV_VIEW_ICON.
 			# Hopefully, no one sets LVS_REPORT and then LV_VIEW_ICON.
-			return self.windowStyle & ListViewWindowStyle.TYPEMASK == ListViewWindowStyle.REPORT
+			return self.windowStyle & LVS_TYPEMASK == LVS_REPORT
 		return False
 
 	def _get_rowCount(self):
@@ -386,13 +344,6 @@ def _getMappedColumn(self, presentationIndex: int) -> Optional[int]:
 			return None
 		return columnOrderArray[presentationIndex - 1]
 
-	def _get_states(self) -> set[controlTypes.State]:
-		states = super().states
-		# The default is multi select supported unless LVS_SINGLESEL is set.
-		if not (self.windowStyle & ListViewWindowStyle.SINGLESEL):
-			states.add(controlTypes.State.MULTISELECTABLE)
-		return states
-
 
 class GroupingItem(Window):
 	def __init__(self, windowHandle=None, parentNVDAObject=None, groupInfo=None):
@@ -454,7 +405,7 @@ def initOverlayClass(self):
 
 	def _get_value(self):
 		value = super(ListItemWithoutColumnSupport, self)._get_description()
-		if (not value or value.isspace()) and self.windowStyle & ListViewWindowStyle.OWNERDRAWFIXED:
+		if (not value or value.isspace()) and self.windowStyle & LVS_OWNERDRAWFIXED:
 			value = self.displayText
 		if not value:
 			return None
@@ -796,7 +747,7 @@ def _get_name(self):
 			name = super(ListItem, self).name
 			if name:
 				return name
-			elif self.windowStyle & ListViewWindowStyle.OWNERDRAWFIXED:
+			elif self.windowStyle & LVS_OWNERDRAWFIXED:
 				return self.displayText
 			return name
 		textList = []
@@ -830,7 +781,7 @@ def _get_name(self):
 	value = None
 
 	def _get__shouldDisableMultiColumn(self):
-		if self.windowStyle & ListViewWindowStyle.OWNERDRAWFIXED:
+		if self.windowStyle & LVS_OWNERDRAWFIXED:
 			# This is owner drawn, but there may still be column content.
 			# accDescription will be empty if there is no column content,
 			# in which case multi-column support must be disabled.

```