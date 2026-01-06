# Diff for: `source\objbase.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\objbase.py`  
**Current**: `F:\nvda\gh\alphajp\source\objbase.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\objbase.py" "b/F:\\nvda\\gh\\alphajp\\source\\objbase.py"
index 2e7c4ea6c3..6643505116 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\objbase.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\objbase.py"
@@ -4,16 +4,18 @@
 # See the file COPYING for more details.
 
 from ctypes import *  # noqa: F403
+from ctypes import byref
 import objidl
+import winBindings.ole32
 
 
 def GetRunningObjectTable():
 	rot = POINTER(objidl.IRunningObjectTable)()  # noqa: F405
-	oledll.ole32.GetRunningObjectTable(0, byref(rot))  # noqa: F405
+	winBindings.ole32.GetRunningObjectTable(0, byref(rot))
 	return rot
 
 
 def CreateBindCtx():
 	bctx = POINTER(objidl.IBindCtx)()  # noqa: F405
-	oledll.ole32.CreateBindCtx(0, byref(bctx))  # noqa: F405
+	winBindings.ole32.CreateBindCtx(0, byref(bctx))
 	return bctx

```