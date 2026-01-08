# Diff for: `source\winBindings\user32.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\user32.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\user32.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\user32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\user32.py"
index 3fc6462..8771860 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\user32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\user32.py"
@@ -19,6 +19,7 @@
 	windll,
 	POINTER,
 )
+from enum import IntEnum, IntFlag
 from ctypes.wintypes import (
 	BOOL,
 	COLORREF,
@@ -57,7 +58,6 @@
 	WPARAM,
 	ATOM,
 )
-from enum import IntEnum, IntFlag
 
 UINT_PTR = c_size_t
 ULONG_PTR = c_size_t

```