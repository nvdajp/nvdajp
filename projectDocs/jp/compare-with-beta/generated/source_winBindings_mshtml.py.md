# Diff for: `source\winBindings\mshtml.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\mshtml.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\mshtml.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\mshtml.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\mshtml.py"
index 8870286..bf2d735 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\mshtml.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\mshtml.py"
@@ -6,7 +6,6 @@
 """Functions exported by mshtml.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	windll,
 	POINTER,
 )
@@ -23,7 +22,7 @@
 dll = windll.mshtml
 
 
-ShowHTMLDialogEx = WINFUNCTYPE(None)(("ShowHTMLDialogEx", dll))
+ShowHTMLDialogEx = dll.ShowHTMLDialogEx
 """
 Creates a modeless HTML dialog box.
 

```