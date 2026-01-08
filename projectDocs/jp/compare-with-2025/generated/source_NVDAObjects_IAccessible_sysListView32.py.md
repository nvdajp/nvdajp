# Diff for: `source\NVDAObjects\IAccessible\sysListView32.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\IAccessible\sysListView32.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\NVDAObjects\IAccessible\sysListView32.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\IAccessible\\sysListView32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\sysListView32.py"
index 7d327b0..3ed2abb 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\IAccessible\\sysListView32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\NVDAObjects\\IAccessible\\sysListView32.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2006-2022 NV Access Limited, Peter Vágner, Leonard de Ruijter, Cyrille Bougot
+# Copyright (C) 2006-2025 NV Access Limited, Peter Vágner, Leonard de Ruijter, Cyrille Bougot
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -8,6 +8,7 @@
 import ctypes
 from ctypes.wintypes import *  # noqa: F403
 from comtypes import BSTR
+from enum import IntFlag
 import NVDAHelper
 import watchdog
 import controlTypes
@@ -22,6 +23,7 @@
 from locationHelper import RectLTRB
 from logHandler import log
 from typing import Optional
+from utils import _deprecate
 
 # Window messages
 LVM_FIRST = 0x1000
@@ -66,9 +68,49 @@
 LVIS_SELECTED = 0x02
 LVIS_STATEIMAGEMASK = 0xF000
 
-LVS_REPORT = 0x0001
-LVS_TYPEMASK = 0x0003
-LVS_OWNERDRAWFIXED = 0x0400
+
+class ListViewWindowStyle(IntFlag):
+	"""Window styles  specific to list-view controls.
+
+	.. seealso::
+		https://learn.microsoft.com/en-us/windows/win32/controls/list-view-window-styles
+	"""
+
+	REPORT = 0x0001
+	"""This style specifies report view."""
+	TYPEMASK = 0x0003
+	"""Determines the control's current window style."""
+	SINGLESEL = 0x0004
+	"""Only one item at a time can be selected.
+	By default, multiple items may be selected."""
+	OWNERDRAWFIXED = 0x0400
+	"""The owner window can paint items in report view."""
+
+
+__getattr__ = _deprecate.handleDeprecations(
+	_deprecate.MovedSymbol(
+		"LVS_REPORT",
+		__name__,
+		"ListViewWindowStyle",
+		"REPORT",
+		"value",
+	),
+	_deprecate.MovedSymbol(
+		"LVS_TYPEMASK",
+		__name__,
+		"ListViewWindowStyle",
+		"TYPEMASK",
+		"value",
+	),
+	_deprecate.MovedSymbol(
+		"LVS_OWNERDRAWFIXED",
+		__name__,
+		"ListViewWindowStyle",
+		"OWNERDRAWFIXED",
+		"value",
+	),
+)
+
 
 # column mask flags
 LVCF_FMT = 1
@@ -95,7 +137,10 @@ class LVITEM(Structure):  # noqa: F405
 		("iSubItem", c_int),  # noqa: F405
 		("state", c_uint),  # noqa: F405
 		("stateMask", c_uint),  # noqa: F405
-		("pszText", c_void_p),  # noqa: F405
+		# A pointer to a buffer containing the text of the item.
+		# #18706: note that the pointer size is dictated by the architecture of the process that
+		# hosts the list item, not the process that fetches the list item information.
+		("pszText", c_ulong),  # noqa: F405
 		("cchTextMax", c_int),  # noqa: F405
 		("iImage", c_int),  # noqa: F405
 		("lParam", LPARAM),  # noqa: F405
@@ -133,7 +178,10 @@ class LVCOLUMN(Structure):  # noqa: F405
 		("mask", c_uint),  # noqa: F405
 		("fmt", c_int),  # noqa: F405
 		("cx", c_int),  # noqa: F405
-		("pszText", c_void_p),  # noqa: F405
+		# A pointer to a buffer containing the column text.
+		# #18706: note that the pointer size is dictated by the architecture of the process that
+		# hosts the list item, not the process that fetches the list item information.
+		("pszText", c_ulong),  # noqa: F405
 		("cchTextMax", c_int),  # noqa: F405
 		("iSubItem", c_int),  # noqa: F405
 		("iImage", c_int),  # noqa: F405
@@ -231,7 +279,7 @@ def _get_isMultiColumn(self):
 			# #2673: This could indicate that LVM_GETVIEW is not supported (comctl32 < 6.0).
 			# Unfortunately, it could also indicate LV_VIEW_ICON.
 			# Hopefully, no one sets LVS_REPORT and then LV_VIEW_ICON.
-			return self.windowStyle & LVS_TYPEMASK == LVS_REPORT
+			return self.windowStyle & ListViewWindowStyle.TYPEMASK == ListViewWindowStyle.REPORT
 		return False
 
 	def _get_rowCount(self):
@@ -338,6 +386,13 @@ def _getMappedColumn(self, presentationIndex: int) -> Optional[int]:
 			return None
 		return columnOrderArray[presentationIndex - 1]
 
+	def _get_states(self) -> set[controlTypes.State]:
+		states = super().states
+		# The default is multi select supported unless LVS_SINGLESEL is set.
+		if not (self.windowStyle & ListViewWindowStyle.SINGLESEL):
+			states.add(controlTypes.State.MULTISELECTABLE)
+		return states
+
 
 class GroupingItem(Window):
 	def __init__(self, windowHandle=None, parentNVDAObject=None, groupInfo=None):
@@ -399,7 +454,7 @@ def initOverlayClass(self):
 
 	def _get_value(self):
 		value = super(ListItemWithoutColumnSupport, self)._get_description()
-		if (not value or value.isspace()) and self.windowStyle & LVS_OWNERDRAWFIXED:
+		if (not value or value.isspace()) and self.windowStyle & ListViewWindowStyle.OWNERDRAWFIXED:
 			value = self.displayText
 		if not value:
 			return None
@@ -741,7 +796,7 @@ def _get_name(self):
 			name = super(ListItem, self).name
 			if name:
 				return name
-			elif self.windowStyle & LVS_OWNERDRAWFIXED:
+			elif self.windowStyle & ListViewWindowStyle.OWNERDRAWFIXED:
 				return self.displayText
 			return name
 		textList = []
@@ -775,7 +830,7 @@ def _get_name(self):
 	value = None
 
 	def _get__shouldDisableMultiColumn(self):
-		if self.windowStyle & LVS_OWNERDRAWFIXED:
+		if self.windowStyle & ListViewWindowStyle.OWNERDRAWFIXED:
 			# This is owner drawn, but there may still be column content.
 			# accDescription will be empty if there is no column content,
 			# in which case multi-column support must be disabled.

```