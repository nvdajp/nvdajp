# Diff for: `source\winBindings\oleaut32.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\oleaut32.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\oleaut32.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\oleaut32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\oleaut32.py"
index a596c52..7c5e352 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\oleaut32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\oleaut32.py"
@@ -6,7 +6,6 @@
 """Functions exported by oleaut32.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	windll,
 )
 from comtypes import BSTR
@@ -15,7 +14,7 @@
 dll = windll.oleaut32
 
 
-SysFreeString = WINFUNCTYPE(None)(("SysFreeString", dll))
+SysFreeString = dll.SysFreeString
 """
 Frees a string allocated previously by the SysAllocString, SysAllocStringLen, SysAlloc
 StringByteLen, or SysReAllocString functions.

```