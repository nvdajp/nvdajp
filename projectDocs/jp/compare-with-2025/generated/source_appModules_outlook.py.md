# Diff for: `source\appModules\outlook.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\appModules\outlook.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\appModules\outlook.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModules\\outlook.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\outlook.py"
index e8e1ac6..09e46f8 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModules\\outlook.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\outlook.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2006-2021 NV Access Limited, Yogesh Kumar, Manish Agrawal, Joseph Lee, Davy Kager,
+# Copyright (C) 2006-2025 NV Access Limited, Yogesh Kumar, Manish Agrawal, Joseph Lee, Davy Kager,
 # Babbage B.V., Leonard de Ruijter
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
@@ -9,8 +9,8 @@
 import comtypes.client
 import comtypes.automation
 import ctypes
-import winVersion
 from scriptHandler import script
+import winBindings.kernel32
 import winKernel
 import comHelper
 import NVDAHelper
@@ -114,7 +114,7 @@ class AppModule(appModuleHandler.AppModule):
 	def isGoodUIAWindow(self, hwnd: int) -> bool:
 		windowClass = winUser.getClassName(hwnd)
 		versionMajor = int(self.productVersion.split(".")[0])
-		if versionMajor >= 16 and windowClass == "RICHEDIT60W" and winVersion.getWinVer() >= winVersion.WIN10:
+		if versionMajor >= 16 and windowClass == "RICHEDIT60W":
 			# #12726: RICHEDIT60W In Outlook 2016+ on Windows 10+
 			# has a very good UI Automation implementation,
 			# Though oddly IsServerSideProvider returns false for these windows.
@@ -342,7 +342,7 @@ def event_valueChange(self):
 		"""Set focus back to the edit field when an auto-complete list item is confirmed."""
 		if vision.handler:
 			vision.handler.handleGainFocus(self)
-		api.setNavigatorObject(self)
+			api.setNavigatorObject(self, isFocus=True)
 		super().event_valueChange()
 
 
@@ -431,7 +431,7 @@ def _generateCategoriesText(appointment):
 		bufLength = 4
 		separatorBuf = ctypes.create_unicode_buffer(bufLength)
 		if (
-			ctypes.windll.kernel32.GetLocaleInfoW(
+			winBindings.kernel32.GetLocaleInfo(
 				languageHandler.LOCALE_USER_DEFAULT,
 				languageHandler.LOCALE.SLIST,
 				separatorBuf,

```