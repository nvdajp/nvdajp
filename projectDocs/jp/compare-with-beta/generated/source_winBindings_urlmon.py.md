# Diff for: `source\winBindings\urlmon.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\urlmon.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\urlmon.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\urlmon.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\urlmon.py"
index f53efd7..6caefa8 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\urlmon.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\urlmon.py"
@@ -6,7 +6,6 @@
 """Functions exported by urlmon.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	windll,
 	POINTER,
 )
@@ -21,7 +20,7 @@
 dll = windll.urlmon
 
 
-CreateURLMonikerEx = WINFUNCTYPE(None)(("CreateURLMonikerEx", dll))
+CreateURLMonikerEx = dll.CreateURLMonikerEx
 """
 Creates a URL moniker from a full or partial URL string.
 

```