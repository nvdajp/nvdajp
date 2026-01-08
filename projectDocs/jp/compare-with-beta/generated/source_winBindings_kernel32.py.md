# Diff for: `source\winBindings\kernel32.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\kernel32.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\kernel32.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\kernel32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\kernel32.py"
index 64c7f7a..63cb580 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\kernel32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\kernel32.py"
@@ -222,6 +222,19 @@
 )
 OpenProcess.restype = HANDLE
 
+OpenThread = WINFUNCTYPE(None)(("OpenThread", dll))
+"""
+Opens an existing thread object.
+.. seealso::
+	https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-openthread
+"""
+OpenThread.argtypes = (
+	DWORD,  # dwDesiredAccess
+	BOOL,  # bInheritHandle
+	DWORD,  # dwThreadId
+)
+OpenThread.restype = HANDLE
+
 VirtualAllocEx = WINFUNCTYPE(None)(("VirtualAllocEx", dll))
 """
 Allocates memory in the virtual address space of a specified process.
@@ -369,7 +382,6 @@
 )
 SetUnhandledExceptionFilter.restype = UnhandledExceptionFilter
 
-
 GetCurrentThreadId = WINFUNCTYPE(None)(("GetCurrentThreadId", dll))
 """
 Retrieves the thread identifier of the calling thread.

```