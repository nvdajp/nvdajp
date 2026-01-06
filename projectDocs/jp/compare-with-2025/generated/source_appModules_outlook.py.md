# Diff for: `source\appModules\outlook.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\appModules\outlook.py`  
**Current**: `F:\nvda\gh\alphajp\source\appModules\outlook.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModules\\outlook.py" "b/F:\\nvda\\gh\\alphajp\\source\\appModules\\outlook.py"
index e8e1ac6406..71a6682745 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModules\\outlook.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\appModules\\outlook.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2006-2021 NV Access Limited, Yogesh Kumar, Manish Agrawal, Joseph Lee, Davy Kager,
+# Copyright (C) 2006-2025 NV Access Limited, Yogesh Kumar, Manish Agrawal, Joseph Lee, Davy Kager,
 # Babbage B.V., Leonard de Ruijter
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
@@ -9,7 +9,6 @@
 import comtypes.client
 import comtypes.automation
 import ctypes
-import winVersion
 from scriptHandler import script
 import winKernel
 import comHelper
@@ -114,7 +113,7 @@ class AppModule(appModuleHandler.AppModule):
 	def isGoodUIAWindow(self, hwnd: int) -> bool:
 		windowClass = winUser.getClassName(hwnd)
 		versionMajor = int(self.productVersion.split(".")[0])
-		if versionMajor >= 16 and windowClass == "RICHEDIT60W" and winVersion.getWinVer() >= winVersion.WIN10:
+		if versionMajor >= 16 and windowClass == "RICHEDIT60W":
 			# #12726: RICHEDIT60W In Outlook 2016+ on Windows 10+
 			# has a very good UI Automation implementation,
 			# Though oddly IsServerSideProvider returns false for these windows.

```