# Diff for: `source\winBindings\dbgHelp.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\dbgHelp.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\dbgHelp.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\dbgHelp.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\dbgHelp.py"
index b41b016..7b13700 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\dbgHelp.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\dbgHelp.py"
@@ -6,7 +6,6 @@
 """Functions exported by dbgHelp.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	c_void_p,
 	POINTER,
 	Structure,
@@ -38,7 +37,7 @@ class MINIDUMP_EXCEPTION_INFORMATION(Structure):
 dll = windll.dbgHelp
 
 
-MiniDumpWriteDump = WINFUNCTYPE(None)(("MiniDumpWriteDump", dll))
+MiniDumpWriteDump = dll.MiniDumpWriteDump
 """
 Writes a memory dump of the specified process to a file.
 .. seealso::

```