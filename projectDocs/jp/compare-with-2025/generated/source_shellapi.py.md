# Diff for: `source\shellapi.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\shellapi.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\shellapi.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\shellapi.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\shellapi.py"
index 9b3de6f..1660e6b 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\shellapi.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\shellapi.py"
@@ -6,36 +6,16 @@
 from ctypes import *  # noqa: F403
 from ctypes.wintypes import *  # noqa: F403
 from typing import Optional
+import winBindings.shell32
+from utils import _deprecate
 
 
-shell32 = windll.shell32  # noqa: F405
-
-
-class SHELLEXECUTEINFOW(Structure):  # noqa: F405
-	_fields_ = (
-		("cbSize", DWORD),  # noqa: F405
-		("fMask", ULONG),  # noqa: F405
-		("hwnd", HWND),  # noqa: F405
-		("lpVerb", LPCWSTR),  # noqa: F405
-		("lpFile", LPCWSTR),  # noqa: F405
-		("lpParameters", LPCWSTR),  # noqa: F405
-		("lpDirectory", LPCWSTR),  # noqa: F405
-		("nShow", c_int),  # noqa: F405
-		("hInstApp", HINSTANCE),  # noqa: F405
-		("lpIDList", LPVOID),  # noqa: F405
-		("lpClass", LPCWSTR),  # noqa: F405
-		("hkeyClass", HKEY),  # noqa: F405
-		("dwHotKey", DWORD),  # noqa: F405
-		("hIconOrMonitor", HANDLE),  # noqa: F405
-		("hProcess", HANDLE),  # noqa: F405
+__getattr__ = _deprecate.handleDeprecations(
+	_deprecate.MovedSymbol("SHELLEXECUTEINFO", "winBindings.shell32"),
+	_deprecate.MovedSymbol("SHELLEXECUTEINFOW", "winBindings.shell32"),
+	_deprecate.MovedSymbol("shell32", "winBindings.shell32", "dll"),
 )
 
-	def __init__(self, **kwargs):
-		super(SHELLEXECUTEINFOW, self).__init__(cbSize=sizeof(self), **kwargs)  # noqa: F405
-
-
-SHELLEXECUTEINFO = SHELLEXECUTEINFOW
-
 SEE_MASK_NOCLOSEPROCESS = 0x00000040
 
 
@@ -49,12 +29,12 @@ def ShellExecute(
 ) -> None:
 	if not file:
 		raise RuntimeError("file cannot be None")
-	if shell32.ShellExecuteW(hwnd, operation, file, parameters, directory, showCmd) <= 32:
+	if winBindings.shell32.ShellExecute(hwnd, operation, file, parameters, directory, showCmd) <= 32:
 		raise WinError()  # noqa: F405
 
 
 def ShellExecuteEx(execInfo):
-	if not shell32.ShellExecuteExW(byref(execInfo)):  # noqa: F405
+	if not winBindings.shell32.ShellExecuteEx(byref(execInfo)):  # noqa: F405
 		raise WinError()  # noqa: F405
 
 
@@ -83,9 +63,7 @@ class SHFILEOPSTRUCT(Structure):  # noqa: F405
 
 SHCNE_ASSOCCHANGED = 0x08000000
 SHCNF_IDLIST = 0x0
-shell32.SHChangeNotify.argtypes = [c_long, c_uint, c_void_p, c_void_p]  # noqa: F405
-shell32.SHChangeNotify.restype = None
 
 
 def SHChangeNotify(wEventId, uFlags, dwItem1, dwItem2):
-	shell32.SHChangeNotify(wEventId, uFlags, dwItem1, dwItem2)
+	winBindings.shell32.SHChangeNotify(wEventId, uFlags, dwItem1, dwItem2)

```