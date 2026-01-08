# Diff for: `source\winBindings\shcore.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\shcore.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\shcore.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\shcore.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\shcore.py"
index 14daa06..ae7df18 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\shcore.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\shcore.py"
@@ -6,7 +6,6 @@
 """Functions exported by shcore.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	c_long,
 	windll,
 )
@@ -16,7 +15,7 @@
 dll = windll.shcore
 
 
-SetProcessDpiAwareness = WINFUNCTYPE(None)(("SetProcessDpiAwareness", dll))
+SetProcessDpiAwareness = dll.SetProcessDpiAwareness
 """
 Sets the current process to a specified dots per inch (DPI) awareness level. The DPI awareness levels are from the PROCESS_DPI_AWARENESS enumeration.
 

```