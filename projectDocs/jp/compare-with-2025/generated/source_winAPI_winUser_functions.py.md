# Diff for: `source\winAPI\winUser\functions.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\winAPI\winUser\functions.py`  
**Current**: `F:\nvda\gh\alphajp\source\winAPI\winUser\functions.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\winAPI\\winUser\\functions.py" "b/F:\\nvda\\gh\\alphajp\\source\\winAPI\\winUser\\functions.py"
index 94d3a8ae12..b849507fcf 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\winAPI\\winUser\\functions.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\winAPI\\winUser\\functions.py"
@@ -1,15 +1,17 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2022 NV Access Limited, Cyrille Bougot
+# Copyright (C) 2022-2025 NV Access Limited, Cyrille Bougot
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
-from ctypes import windll
-from .constants import SysColorIndex
 
+from winBindings import user32 as _user32
+from .constants import SysColorIndex
+from utils import _deprecate
 
-# dll handles
-user32 = windll.user32
+_deprecate.handleDeprecations(
+	_deprecate.MovedSymbol("user32", "winBindings.user32", "dll"),
+)
 
 
 def GetSysColor(index: SysColorIndex):
-	return user32.GetSysColor(index)
+	return _user32.GetSysColor(index)

```