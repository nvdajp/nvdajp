# Diff for: `source\winBindings\kernel32.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\winBindings\kernel32.py`  
**Current**: `F:\nvda\gh\alphajp\source\winBindings\kernel32.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\winBindings\\kernel32.py" "b/F:\\nvda\\gh\\alphajp\\source\\winBindings\\kernel32.py"
index 6373c7593f..153d356829 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\winBindings\\kernel32.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\winBindings\\kernel32.py"
@@ -6,6 +6,8 @@
 """Functions exported by kernel32.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
+	WINFUNCTYPE,
+	c_void_p,
 	c_wchar_p,
 	windll,
 	POINTER,
@@ -25,6 +27,8 @@
 __all__ = (
 	"GetModuleHandle",
 	"GetModuleFileName",
+	"CopyFile",
+	"OpenThread",
 )
 
 
@@ -118,6 +122,19 @@
 )
 OpenProcess.restype = HANDLE
 
+OpenThread = dll.OpenThread
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
 VirtualAllocEx = dll.VirtualAllocEx
 """
 Allocates memory in the virtual address space of a specified process.
@@ -239,3 +256,42 @@
 	HGLOBAL,  # hMem
 )
 GlobalUnlock.restype = BOOL
+
+GetCurrentProcess = dll.GetCurrentProcess
+"""
+Retrieves a pseudo handle for the current process.
+.. seealso::
+	https://learn.microsoft.com/en-us/windows/win32/api/processthreadsapi/nf-processthreadsapi-getcurrentprocess
+"""
+GetCurrentProcess.argtypes = ()
+GetCurrentProcess.restype = HANDLE
+
+UnhandledExceptionFilter = WINFUNCTYPE(
+	c_void_p,  # lpTopLevelExceptionFilter: The pointer to the old unhandled exception filter function.
+	c_void_p,  # lpTopLevelExceptionFilter: A pointer to the new unhandled exception filter function.
+)
+
+SetUnhandledExceptionFilter = dll.SetUnhandledExceptionFilter
+"""
+Sets a new unhandled exception filter function for the current process.
+.. seealso::
+	https://learn.microsoft.com/en-us/windows/win32/api/errhandlingapi/nf-errhandlingapi-setunhandledexceptionfilter
+"""
+SetUnhandledExceptionFilter.argtypes = (
+	UnhandledExceptionFilter,  # lpTopLevelExceptionFilter: A pointer to the new unhandled exception filter function.
+)
+SetUnhandledExceptionFilter.restype = UnhandledExceptionFilter
+
+CopyFile = dll.CopyFileW
+"""
+Copies an existing file to a new file.
+
+.. seealso::
+	https://learn.microsoft.com/en-us/windows/win32/api/winbase/nf-winbase-copyfilew
+"""
+CopyFile.argtypes = (
+	LPCWSTR,  # lpExistingFileName
+	LPCWSTR,  # lpNewFileName
+	BOOL,  # bFailIfExists
+)
+CopyFile.restype = BOOL

```