# Diff for: `source\winBindings\shlwapi.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\shlwapi.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\shlwapi.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\shlwapi.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\shlwapi.py"
index 378765c..b83e1b1 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\shlwapi.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\shlwapi.py"
@@ -6,7 +6,6 @@
 """Functions exported by shlwapi.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	c_uint,
 	c_void_p,
 	c_wchar_p,
@@ -20,7 +19,7 @@
 dll = windll.shlwapi
 
 
-SHLoadIndirectString = WINFUNCTYPE(None)(("SHLoadIndirectString", dll))
+SHLoadIndirectString = dll.SHLoadIndirectString
 """
 Extracts a specified text resource when given an indirect string.
 

```