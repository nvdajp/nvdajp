# Diff for: `source\winBindings\rpcrt4.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\rpcrt4.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\rpcrt4.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\rpcrt4.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\rpcrt4.py"
index ea12165..af1a264 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\rpcrt4.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\rpcrt4.py"
@@ -6,7 +6,6 @@
 """Functions exported by rpcrt4.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	c_long,
 	c_ulong,
 	c_void_p,
@@ -21,7 +20,7 @@
 RPC_BINDING_HANDLE = c_void_p
 
 
-I_RpcBindingInqLocalClientPID = WINFUNCTYPE(None)(("I_RpcBindingInqLocalClientPID", dll))
+I_RpcBindingInqLocalClientPID = dll.I_RpcBindingInqLocalClientPID
 """
 Obtains the process identifier (PID) of the local client process that made the remote procedure call.
 
@@ -34,7 +33,7 @@
 	POINTER(c_long),  # ClientPID: Pointer to receive the client process ID
 )
 
-RpcBindingFree = WINFUNCTYPE(None)(("RpcBindingFree", dll))
+RpcBindingFree = dll.RpcBindingFree
 """
 Releases binding handle resources.
 
@@ -46,7 +45,7 @@
 	POINTER(RPC_BINDING_HANDLE),  # Binding: Pointer to the binding handle to free
 )
 
-RpcSsDestroyClientContext = WINFUNCTYPE(None)(("RpcSsDestroyClientContext", dll))
+RpcSsDestroyClientContext = dll.RpcSsDestroyClientContext
 """
 Destroys a client context handle and releases associated resources.
 

```