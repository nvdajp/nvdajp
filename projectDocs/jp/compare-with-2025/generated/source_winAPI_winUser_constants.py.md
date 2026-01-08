# Diff for: `source\winAPI\winUser\constants.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\winAPI\winUser\constants.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winAPI\winUser\constants.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\winAPI\\winUser\\constants.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winAPI\\winUser\\constants.py"
index aed2a32..88ed602 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\winAPI\\winUser\\constants.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winAPI\\winUser\\constants.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2022 NV Access Limited, Cyrille Bougot
+# Copyright (C) 2022-2025 NV Access Limited, Cyrille Bougot
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -61,6 +61,13 @@ class SystemMetrics(IntEnum):
 	SM_CYVIRTUALSCREEN
 	"""
 
+	MAXIMUM_TOUCHES = 95
+	"""
+	The aggregate maximum of the maximum number of contacts supported by every digitizer in the system, or 0 if there are no digitizers in the system.
+
+	SM_MAXIMUMTOUCHES
+	"""
+
 
 class SysColorIndex(IntEnum):
 	"""

```