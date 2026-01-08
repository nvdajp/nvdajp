# Diff for: `source\winBindings\shell32.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\shell32.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\shell32.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\shell32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\shell32.py"
index 6d22b27..e30c65c 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\shell32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\shell32.py"
@@ -6,7 +6,6 @@
 """Functions exported by shell32.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	POINTER,
 	sizeof,
 	Structure,
@@ -39,7 +38,7 @@
 dll = windll.shell32
 
 
-IsUserAnAdmin = WINFUNCTYPE(None)(("IsUserAnAdmin", dll))
+IsUserAnAdmin = dll.IsUserAnAdmin
 """
 Tests whether the current user is a member of the Administrator's group.
 
@@ -49,7 +48,7 @@
 IsUserAnAdmin.restype = BOOL
 IsUserAnAdmin.argtypes = ()
 
-SHGetKnownFolderPath = WINFUNCTYPE(None)(("SHGetKnownFolderPath", dll))
+SHGetKnownFolderPath = dll.SHGetKnownFolderPath
 """
 Retrieves the full path of a known folder identified by the folder's KNOWNFOLDERID.
 
@@ -64,7 +63,7 @@
 	POINTER(c_wchar_p),  # ppszPath: Address of a pointer to a null-terminated Unicode string
 )
 
-ShellExecute = WINFUNCTYPE(None)(("ShellExecuteW", dll))
+ShellExecute = dll.ShellExecuteW
 """
 Performs an operation on a specified file.
 
@@ -114,7 +113,7 @@ def __init__(self, **kwargs):
 
 SHELLEXECUTEINFO = SHELLEXECUTEINFOW
 
-ShellExecuteEx = WINFUNCTYPE(None)(("ShellExecuteExW", dll))
+ShellExecuteEx = dll.ShellExecuteExW
 """
 Performs an operation on a specified file with extended options.
 
@@ -126,7 +125,7 @@ def __init__(self, **kwargs):
 	POINTER(SHELLEXECUTEINFOW),  # pExecInfo: Pointer to a SHELLEXECUTEINFO structure
 )
 
-SHChangeNotify = WINFUNCTYPE(None)(("SHChangeNotify", dll))
+SHChangeNotify = dll.SHChangeNotify
 """
 Notifies the system of an event that an application has performed.
 

```