# Diff for: `source\appModules\wwahost.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\appModules\wwahost.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\appModules\wwahost.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModules\\wwahost.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\wwahost.py"
index 1a5b4b8..22c566a 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\appModules\\wwahost.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\wwahost.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2012-2020 NV Access Limited, Joseph Lee
+# Copyright (C) 2012-2025 NV Access Limited, Joseph Lee
 
 """App module host for Windows 8.x and 10 apps hosted by wwahost.exe.
 In Windows 8, apps written in Javascript are executed inside WWAHost, including some WinRT apps.
@@ -11,6 +11,7 @@
 
 import ctypes
 import appModuleHandler
+import winBindings.kernel32
 import winKernel
 
 
@@ -23,9 +24,9 @@ def getAppNameFromHost(processId):
 		processId,
 	)
 	length = ctypes.c_uint()
-	winKernel.kernel32.GetApplicationUserModelId(processHandle, ctypes.byref(length), None)
+	winBindings.kernel32.GetApplicationUserModelId(processHandle, ctypes.byref(length), None)
 	appModel = ctypes.create_unicode_buffer(length.value)
-	winKernel.kernel32.GetApplicationUserModelId(processHandle, ctypes.byref(length), appModel)
+	winBindings.kernel32.GetApplicationUserModelId(processHandle, ctypes.byref(length), appModel)
 	winKernel.closeHandle(processHandle)
 	# Sometimes app model might be empty, so raise errors and fall back to wwahost.
 	if not appModel.value:

```