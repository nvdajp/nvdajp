# Diff for: `source\appModules\excel.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\appModules\excel.py`  
**Current**: `F:\nvda\gh\alphajp\source\appModules\excel.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModules\\excel.py" "b/F:\\nvda\\gh\\alphajp\\source\\appModules\\excel.py"
index fa8430afc6..150a4f1c24 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModules\\excel.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\appModules\\excel.py"
@@ -1,6 +1,6 @@
 # -*- coding: UTF-8 -*-
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2018 NV Access Limited, Łukasz Golonka
+# Copyright (C) 2018-2025 NV Access Limited, Łukasz Golonka
 # This file may be used under the terms of the GNU General Public License, version 2 or later.
 # For more details see: https://www.gnu.org/licenses/gpl-2.0.html
 
@@ -13,7 +13,6 @@
 from NVDAObjects import NVDAObject
 from NVDAObjects.UIA import UIA
 import winUser
-import winVersion
 import controlTypes
 import appModuleHandler
 from scriptHandler import script
@@ -111,7 +110,7 @@ def isGoodUIAWindow(self, hwnd: int) -> bool:
 			return True
 		windowClass = winUser.getClassName(hwnd)
 		versionMajor = int(self.productVersion.split(".")[0])
-		if versionMajor >= 16 and windowClass == "RICHEDIT60W" and winVersion.getWinVer() >= winVersion.WIN10:
+		if versionMajor >= 16 and windowClass == "RICHEDIT60W":
 			# RICHEDIT60W In Excel 2016+ on Windows 10+
 			# has a very good UI Automation implementation,
 			# Though oddly IsServerSideProvider returns false for these windows.

```