# Diff for: `source\winAPI\_wtsApi32.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\winAPI\_wtsApi32.py`  
**Current**: `F:\nvda\gh\alphajp\source\winAPI\_wtsApi32.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\winAPI\\_wtsApi32.py" "b/F:\\nvda\\gh\\alphajp\\source\\winAPI\\_wtsApi32.py"
index 2dbe73dd3f..775931618c 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\winAPI\\_wtsApi32.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\winAPI\\_wtsApi32.py"
@@ -16,7 +16,6 @@
 from typing import Callable
 import ctypes  # Use for ctypes.Union to prevent name collision with typing.Union
 from ctypes import (
-	windll,
 	c_void_p,
 	c_wchar,
 	c_int,
@@ -29,9 +28,8 @@
 	LONG,
 	LARGE_INTEGER,
 	LPWSTR,
-	BOOL,
 )
-
+import winBindings.wtsapi32
 
 WTS_CURRENT_SERVER_HANDLE = HANDLE(0)
 """ WTS_CURRENT_SERVER_HANDLE WtsApi32.h#L36
@@ -44,12 +42,7 @@
 
 # WTSFreeMemory Definition
 WTSFreeMemoryT = Callable[[c_void_p], None]
-WTSFreeMemory: WTSFreeMemoryT = windll.wtsapi32.WTSFreeMemory
-"""WtsApi32.h#L1245"""
-WTSFreeMemory.argtypes = (
-	c_void_p,  # [in] PVOID pMemory
-)
-WTSFreeMemory.restype = None
+WTSFreeMemory: WTSFreeMemoryT = winBindings.wtsapi32.WTSFreeMemory
 
 
 class WTS_INFO_CLASS(IntEnum):
@@ -168,15 +161,7 @@ class WTSINFOEXW(ctypes.Structure):
 	],
 	bool,
 ]
-WTSQuerySessionInformation: WTSQuerySessionInformationT = windll.wtsapi32.WTSQuerySessionInformationW
-WTSQuerySessionInformation.argtypes = (
-	HANDLE,  # [in] HANDLE hServer
-	DWORD,  # [ in] DWORD SessionId
-	c_int,  # [ in]  WTS_INFO_CLASS WTSInfoClass,
-	POINTER(LPWSTR),  # [out] LPWSTR * ppBuffer,
-	POINTER(DWORD),  # [out] DWORD * pBytesReturned
-)
-WTSQuerySessionInformation.restype = BOOL  # On Failure, the return value is zero.
+WTSQuerySessionInformation: WTSQuerySessionInformationT = winBindings.wtsapi32.WTSQuerySessionInformation
 
 
 class _WTS_LockState(IntEnum):

```