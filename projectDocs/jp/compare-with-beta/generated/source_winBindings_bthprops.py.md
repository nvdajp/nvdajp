# Diff for: `source\winBindings\bthprops.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\bthprops.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\bthprops.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\bthprops.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\bthprops.py"
index 89349e8..d615a9f 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\bthprops.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\bthprops.py"
@@ -14,7 +14,7 @@
 )
 from ctypes.wintypes import BOOL, DWORD, HANDLE, ULONG, WCHAR
 
-from winBindings.kernel32 import SYSTEMTIME
+from winKernel import SYSTEMTIME
 
 cpl = windll["bthprops.cpl"]
 

```