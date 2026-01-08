# Diff for: `source\UIAHandler\_remoteOps\lowLevel.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\UIAHandler\_remoteOps\lowLevel.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\UIAHandler\_remoteOps\lowLevel.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\UIAHandler\\_remoteOps\\lowLevel.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\UIAHandler\\_remoteOps\\lowLevel.py"
index 3cdca39..6e45f4e 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\UIAHandler\\_remoteOps\\lowLevel.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\UIAHandler\\_remoteOps\\lowLevel.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2023-2024 NV Access Limited
+# Copyright (C) 2023-2025 NV Access Limited
 
 from __future__ import annotations
 from ctypes import (
@@ -13,10 +13,9 @@
 	c_bool,
 )
 from comtypes.automation import VARIANT
-import os
 import enum
+import NVDAState
 from UIAHandler import UIA
-import NVDAHelper
 
 
 """
@@ -56,7 +55,7 @@ def __repr__(self) -> str:
 		return f"RelativeOffset {self.value}"
 
 
-_dll = oledll[os.path.join(NVDAHelper.versionedLibPath, "UIARemote.dll")]
+_dll = oledll[NVDAState.ReadPaths.UIARemoteDll]
 
 
 class RemoteOperationResultSet:

```