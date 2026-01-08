# Diff for: `source\winBindings\ole32.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\ole32.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\ole32.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\ole32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\ole32.py"
index 5409dc9..0beb1fb 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\ole32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\ole32.py"
@@ -6,7 +6,6 @@
 """Functions exported by ole32.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	c_voidp,
 	POINTER,
 	windll,
@@ -31,7 +30,7 @@
 dll = windll.ole32
 
 
-CoTaskMemFree = WINFUNCTYPE(None)(("CoTaskMemFree", dll))
+CoTaskMemFree = dll.CoTaskMemFree
 """
 Frees a block of task memory previously allocated through a call to the CoTaskMemAlloc or CoTaskMemRealloc function.
 
@@ -43,7 +42,7 @@
 	LPVOID,  # pv: A pointer to the memory block to be freed.
 )
 
-CoCancelCall = WINFUNCTYPE(None)(("CoCancelCall", dll))
+CoCancelCall = dll.CoCancelCall
 """
 Requests that a call be canceled.
 
@@ -56,7 +55,7 @@
 	ULONG,  # ulTimeout: The number of milliseconds to wait for the call cancellation.
 )
 
-CoDisableCallCancellation = WINFUNCTYPE(None)(("CoDisableCallCancellation", dll))
+CoDisableCallCancellation = dll.CoDisableCallCancellation
 """
 Undoes the action of a call to CoEnableCallCancellation. Disables cancellation of synchronous calls on the calling thread when all calls to CoEnableCallCancellation are balanced by calls to CoDisableCallCancellation.
 
@@ -68,7 +67,7 @@
 	LPVOID,  # pReserved: This parameter is reserved and must be NULL.
 )
 
-CoEnableCallCancellation = WINFUNCTYPE(None)(("CoEnableCallCancellation", dll))
+CoEnableCallCancellation = dll.CoEnableCallCancellation
 """
 Enables cancellation of synchronous calls on the calling thread.
 
@@ -80,7 +79,7 @@
 	LPVOID,  # pReserved: This parameter is reserved and must be NULL.
 )
 
-CoInitializeEx = WINFUNCTYPE(None)(("CoInitializeEx", dll))
+CoInitializeEx = dll.CoInitializeEx
 """
 Initializes the COM library for use by the calling thread, sets the thread's concurrency model, and creates a new apartment for the thread if one is required.
 
@@ -93,7 +92,7 @@
 	DWORD,  # dwCoInit: The concurrency model and initialization options for the thread.
 )
 
-CoTaskMemAlloc = WINFUNCTYPE(None)(("CoTaskMemAlloc", dll))
+CoTaskMemAlloc = dll.CoTaskMemAlloc
 """
 Allocates a block of task memory in the same way as if IMalloc::Alloc was called.
 
@@ -105,7 +104,7 @@
 	c_size_t,  # cb: The size of the memory block to be allocated, in bytes.
 )
 
-CoWaitForMultipleHandles = WINFUNCTYPE(None)(("CoWaitForMultipleHandles", dll))
+CoWaitForMultipleHandles = dll.CoWaitForMultipleHandles
 """
 Waits for specified handles to be signaled or for a specified timeout period to elapse.
 
@@ -121,7 +120,7 @@
 	LPDWORD,  # lpdwindex: A pointer to a variable that receives the zero-based index of the signaled handle.
 )
 
-CreateBindCtx = WINFUNCTYPE(None)(("CreateBindCtx", dll))
+CreateBindCtx = dll.CreateBindCtx
 """
 Creates a new bind context object.
 
@@ -136,7 +135,7 @@
 	),  # ppbc: The address of a pointer variable that receives the interface pointer to the new bind context object.
 )
 
-GetRunningObjectTable = WINFUNCTYPE(None)(("GetRunningObjectTable", dll))
+GetRunningObjectTable = dll.GetRunningObjectTable
 """
 Retrieves a pointer to the running object table (ROT) for the current context.
 

```