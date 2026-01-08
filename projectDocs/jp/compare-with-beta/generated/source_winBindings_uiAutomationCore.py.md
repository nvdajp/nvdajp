# Diff for: `source\winBindings\uiAutomationCore.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\uiAutomationCore.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\uiAutomationCore.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\uiAutomationCore.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\uiAutomationCore.py"
index 444d12e..db16b1e 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\uiAutomationCore.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\uiAutomationCore.py"
@@ -5,10 +5,7 @@
 
 """Functions exported by UIAutomationCore.dll, and supporting data structures and enumerations."""
 
-from ctypes import (
-	WINFUNCTYPE,
-	windll,
-)
+from ctypes import windll
 from ctypes.wintypes import (
 	BOOL,
 	HWND,
@@ -19,7 +16,7 @@
 
 dll = windll.UIAutomationCore
 
-UiaHasServerSideProvider = WINFUNCTYPE(None)(("UiaHasServerSideProvider", dll))
+UiaHasServerSideProvider = dll.UiaHasServerSideProvider
 """
 Returns a Boolean value that indicates whether a window has a Microsoft UI Automation server-side provider.
 

```