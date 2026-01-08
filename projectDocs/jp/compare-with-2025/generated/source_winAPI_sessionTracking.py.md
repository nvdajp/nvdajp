# Diff for: `source\winAPI\sessionTracking.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\winAPI\sessionTracking.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winAPI\sessionTracking.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\winAPI\\sessionTracking.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winAPI\\sessionTracking.py"
index f7b767a..aaa691a 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\winAPI\\sessionTracking.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winAPI\\sessionTracking.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2022 NV Access Limited
+# Copyright (C) 2022-2025 NV Access Limited
 # This file may be used under the terms of the GNU General Public License, version 2 or later.
 # For more details see: https://www.gnu.org/licenses/gpl-2.0.html
 
@@ -164,14 +164,6 @@ def isLockScreenModeActive() -> bool:
 		# Use secure mode instead if on the secure desktop
 		return False
 
-	import winVersion
-
-	if winVersion.getWinVer() < winVersion.WIN10:
-		# On Windows 8 and Earlier, the lock screen runs on
-		# the secure desktop.
-		# Lock screen mode is not supported on these Windows versions.
-		return False
-
 	return _isWindowsLocked()
 
 

```