# Diff for: `source\shlobj.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\shlobj.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\shlobj.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\shlobj.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\shlobj.py"
index b27adb1..b3cffc6 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\shlobj.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\shlobj.py"
@@ -18,6 +18,10 @@
 from typing import Optional, Union
 
 
+import winBindings.shell32
+import winBindings.ole32
+
+
 class FolderId(str, Enum):
 	"""Contains guids of known folders from Knownfolders.h. Full list is availabe at:
 	https://docs.microsoft.com/en-us/windows/win32/shell/knownfolderid"""
@@ -51,7 +55,7 @@ def SHGetKnownFolderPath(
 	guid = comtypes.GUID(folderGuid)
 
 	pathPointer = ctypes.c_wchar_p()
-	res = ctypes.windll.shell32.SHGetKnownFolderPath(
+	res = winBindings.shell32.SHGetKnownFolderPath(
 		comtypes.byref(guid),
 		dwFlags,
 		hToken,
@@ -60,5 +64,5 @@ def SHGetKnownFolderPath(
 	if res != 0:
 		raise RuntimeError(f"SHGetKnownFolderPath failed with error code {res}")
 	path = pathPointer.value
-	ctypes.windll.ole32.CoTaskMemFree(pathPointer)
+	winBindings.ole32.CoTaskMemFree(pathPointer)
 	return path

```