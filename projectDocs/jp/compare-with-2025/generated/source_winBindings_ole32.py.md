# Diff for: `source\winBindings\ole32.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\winBindings\ole32.py`  
**Current**: `F:\nvda\gh\alphajp\source\winBindings\ole32.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\winBindings\\ole32.py" "b/F:\\nvda\\gh\\alphajp\\source\\winBindings\\ole32.py"
index 02a0592ac3..0beb1fbc58 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\winBindings\\ole32.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\winBindings\\ole32.py"
@@ -7,11 +7,24 @@
 
 from ctypes import (
 	c_voidp,
+	POINTER,
 	windll,
 )
 from ctypes.wintypes import (
+	DWORD,
+	LPDWORD,
+	LPHANDLE,
 	LPVOID,
+	ULONG,
 )
+from comtypes import HRESULT
+from objidl import (
+	IRunningObjectTable,
+	IBindCtx,
+)
+
+# SIZE_T is not in ctypes.wintypes, but it's equivalent to c_size_t
+from ctypes import c_size_t
 
 
 dll = windll.ole32
@@ -28,3 +41,111 @@
 CoTaskMemFree.argtypes = (
 	LPVOID,  # pv: A pointer to the memory block to be freed.
 )
+
+CoCancelCall = dll.CoCancelCall
+"""
+Requests that a call be canceled.
+
+.. seealso::
+	https://learn.microsoft.com/en-us/windows/win32/api/combaseapi/nf-combaseapi-cocancelcall
+"""
+CoCancelCall.restype = HRESULT
+CoCancelCall.argtypes = (
+	DWORD,  # dwThreadId: The identifier of the thread on which the call is to be canceled.
+	ULONG,  # ulTimeout: The number of milliseconds to wait for the call cancellation.
+)
+
+CoDisableCallCancellation = dll.CoDisableCallCancellation
+"""
+Undoes the action of a call to CoEnableCallCancellation. Disables cancellation of synchronous calls on the calling thread when all calls to CoEnableCallCancellation are balanced by calls to CoDisableCallCancellation.
+
+.. seealso::
+	https://learn.microsoft.com/en-us/windows/win32/api/combaseapi/nf-combaseapi-codisablecallcancellation
+"""
+CoDisableCallCancellation.restype = HRESULT
+CoDisableCallCancellation.argtypes = (
+	LPVOID,  # pReserved: This parameter is reserved and must be NULL.
+)
+
+CoEnableCallCancellation = dll.CoEnableCallCancellation
+"""
+Enables cancellation of synchronous calls on the calling thread.
+
+.. seealso::
+	https://learn.microsoft.com/en-us/windows/win32/api/combaseapi/nf-combaseapi-coenablecallcancellation
+"""
+CoEnableCallCancellation.restype = HRESULT
+CoEnableCallCancellation.argtypes = (
+	LPVOID,  # pReserved: This parameter is reserved and must be NULL.
+)
+
+CoInitializeEx = dll.CoInitializeEx
+"""
+Initializes the COM library for use by the calling thread, sets the thread's concurrency model, and creates a new apartment for the thread if one is required.
+
+.. seealso::
+	https://learn.microsoft.com/en-us/windows/win32/api/combaseapi/nf-combaseapi-coinitializeex
+"""
+CoInitializeEx.restype = HRESULT
+CoInitializeEx.argtypes = (
+	LPVOID,  # pvReserved: This parameter is reserved and must be NULL.
+	DWORD,  # dwCoInit: The concurrency model and initialization options for the thread.
+)
+
+CoTaskMemAlloc = dll.CoTaskMemAlloc
+"""
+Allocates a block of task memory in the same way as if IMalloc::Alloc was called.
+
+.. seealso::
+	https://learn.microsoft.com/en-us/windows/win32/api/combaseapi/nf-combaseapi-cotaskmemalloc
+"""
+CoTaskMemAlloc.restype = LPVOID
+CoTaskMemAlloc.argtypes = (
+	c_size_t,  # cb: The size of the memory block to be allocated, in bytes.
+)
+
+CoWaitForMultipleHandles = dll.CoWaitForMultipleHandles
+"""
+Waits for specified handles to be signaled or for a specified timeout period to elapse.
+
+.. seealso::
+	https://learn.microsoft.com/en-us/windows/win32/api/combaseapi/nf-combaseapi-cowaitformultiplehandles
+"""
+CoWaitForMultipleHandles.restype = HRESULT
+CoWaitForMultipleHandles.argtypes = (
+	DWORD,  # dwFlags: Indicates how the wait is to be handled.
+	DWORD,  # dwTimeout: The timeout period, in milliseconds.
+	ULONG,  # cHandles: The number of elements in the pHandles array.
+	LPHANDLE,  # pHandles: An array of handles.
+	LPDWORD,  # lpdwindex: A pointer to a variable that receives the zero-based index of the signaled handle.
+)
+
+CreateBindCtx = dll.CreateBindCtx
+"""
+Creates a new bind context object.
+
+.. seealso::
+	https://learn.microsoft.com/en-us/windows/win32/api/objbase/nf-objbase-createbindctx
+"""
+CreateBindCtx.restype = HRESULT
+CreateBindCtx.argtypes = (
+	DWORD,  # reserved: This parameter is reserved and must be 0.
+	POINTER(
+		IBindCtx,
+	),  # ppbc: The address of a pointer variable that receives the interface pointer to the new bind context object.
+)
+
+GetRunningObjectTable = dll.GetRunningObjectTable
+"""
+Retrieves a pointer to the running object table (ROT) for the current context.
+
+.. seealso::
+	https://learn.microsoft.com/en-us/windows/win32/api/objbase/nf-objbase-getrunningobjecttable
+"""
+GetRunningObjectTable.restype = HRESULT
+GetRunningObjectTable.argtypes = (
+	DWORD,  # reserved: This parameter is reserved and must be 0.
+	POINTER(
+		IRunningObjectTable,
+	),  # pprot: The address of a pointer variable that receives the interface pointer to the running object table.
+)

```