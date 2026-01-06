# Diff for: `source\winAPI\_displayTracking.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\winAPI\_displayTracking.py`  
**Current**: `F:\nvda\gh\alphajp\source\winAPI\_displayTracking.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\winAPI\\_displayTracking.py" "b/F:\\nvda\\gh\\alphajp\\source\\winAPI\\_displayTracking.py"
index cb03dcf5df..4c1776347d 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\winAPI\\_displayTracking.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\winAPI\\_displayTracking.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2022–2024 NV Access Limited, Bill Dengler
+# Copyright (C) 2022-2025 NV Access Limited, Bill Dengler
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -10,7 +10,6 @@
 and we notify the user of changes to the orientation.
 """
 
-from ctypes import windll
 from dataclasses import dataclass
 import enum
 from typing import (
@@ -22,6 +21,7 @@
 import winUser
 
 from .winUser.constants import SystemMetrics
+from winBindings import user32
 
 
 class Orientation(enum.Enum):
@@ -51,12 +51,12 @@ def initialize():
 
 
 def getPrimaryDisplayOrientation() -> OrientationState:
-	width = windll.user32.GetSystemMetrics(SystemMetrics.CX_SCREEN)
+	width = user32.GetSystemMetrics(SystemMetrics.CX_SCREEN)
 	if width == 0:
 		# If the function fails, the return value is 0.
 		# GetLastError does not provide extended error information.
 		log.error("Failed to get primary display width")
-	height = windll.user32.GetSystemMetrics(SystemMetrics.CY_SCREEN)
+	height = user32.GetSystemMetrics(SystemMetrics.CY_SCREEN)
 	if height == 0:
 		# If the function fails, the return value is 0.
 		# GetLastError does not provide extended error information.

```