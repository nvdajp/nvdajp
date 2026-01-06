# Diff for: `source\NVDAObjects\IAccessible\sysListView32.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\NVDAObjects\IAccessible\sysListView32.py`  
**Current**: `F:\nvda\gh\alphajp\source\NVDAObjects\IAccessible\sysListView32.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\IAccessible\\sysListView32.py" "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\IAccessible\\sysListView32.py"
index 7d327b030e..a62b3bd25f 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\NVDAObjects\\IAccessible\\sysListView32.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\NVDAObjects\\IAccessible\\sysListView32.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2006-2022 NV Access Limited, Peter Vágner, Leonard de Ruijter, Cyrille Bougot
+# Copyright (C) 2006-2025 NV Access Limited, Peter Vágner, Leonard de Ruijter, Cyrille Bougot
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -95,7 +95,10 @@ class LVITEM(Structure):  # noqa: F405
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
@@ -133,7 +136,10 @@ class LVCOLUMN(Structure):  # noqa: F405
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

```