# Diff for: `source\ui.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\ui.py`  
**Current**: `F:\nvda\gh\alphajp\source\ui.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\ui.py" "b/F:\\nvda\\gh\\alphajp\\source\\ui.py"
index 91526cdc16..7ee9f3b5f2 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\ui.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\ui.py"
@@ -12,15 +12,16 @@
 
 import os
 from ctypes import (
-	windll,
 	byref,
 	POINTER,
 )
 import comtypes.client
-from comtypes import IUnknown
 from comtypes import automation
 from comtypes import COMError
 from html import escape
+import winBindings.mshtml
+import winBindings.urlmon
+from objidl import IMoniker
 
 import nh3
 from logHandler import log
@@ -169,9 +170,9 @@ def browseableMessage(
 		_warnBrowsableMessageComponentFailure(title)
 		raise LookupError(htmlFileName)
 
-	moniker = POINTER(IUnknown)()
+	moniker = POINTER(IMoniker)()
 	try:
-		windll.urlmon.CreateURLMonikerEx(0, htmlFileName, byref(moniker), URL_MK_UNIFORM)
+		winBindings.urlmon.CreateURLMonikerEx(None, htmlFileName, byref(moniker), URL_MK_UNIFORM)
 	except OSError as e:
 		log.error(f"OS error during URL moniker creation: {e}")
 		_warnBrowsableMessageComponentFailure(title)
@@ -219,7 +220,7 @@ def browseableMessage(
 	dialogArgsVar = automation.VARIANT(d)
 	gui.mainFrame.prePopup()
 	try:
-		windll.mshtml.ShowHTMLDialogEx(
+		winBindings.mshtml.ShowHTMLDialogEx(
 			gui.mainFrame.Handle,
 			moniker,
 			HTMLDLG_MODELESS,

```