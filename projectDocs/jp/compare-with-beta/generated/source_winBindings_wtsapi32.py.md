# Diff for: `source\winBindings\wtsapi32.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\wtsapi32.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\wtsapi32.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\wtsapi32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\wtsapi32.py"
index 8208a38..25fdd3a 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\wtsapi32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\wtsapi32.py"
@@ -6,7 +6,6 @@
 """Functions exported by wtsapi32.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	POINTER,
 	c_int,
 	c_void_p,
@@ -23,7 +22,7 @@
 dll = windll.wtsapi32
 
 
-WTSFreeMemory = WINFUNCTYPE(None)(("WTSFreeMemory", dll))
+WTSFreeMemory = dll.WTSFreeMemory
 """
 Frees memory allocated by a Windows Terminal Services function.
 
@@ -35,7 +34,7 @@
 	c_void_p,  # pMemory: Pointer to the memory to free
 )
 
-WTSQuerySessionInformation = WINFUNCTYPE(None)(("WTSQuerySessionInformationW", dll))
+WTSQuerySessionInformation = dll.WTSQuerySessionInformationW
 """
 Retrieves session information for the specified session on the specified Remote Desktop Session Host server.
 

```