# Diff for: `source\winBindings\sas.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\sas.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\sas.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\sas.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\sas.py"
index e32406e..39c047c 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\sas.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\sas.py"
@@ -6,7 +6,6 @@
 """Functions exported by sas.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	windll,
 )
 from ctypes.wintypes import (
@@ -17,7 +16,7 @@
 dll = windll.sas
 
 
-SendSAS = WINFUNCTYPE(None)(("SendSAS", dll))
+SendSAS = dll.SendSAS
 """
 Simulates a secure attention sequence (SAS).
 

```