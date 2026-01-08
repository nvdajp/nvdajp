# Diff for: `source\winBindings\version.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\version.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\version.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\version.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\version.py"
index 110f385..2263476 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\version.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\version.py"
@@ -6,7 +6,6 @@
 """Functions exported by version.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	POINTER,
 	windll,
 )
@@ -24,7 +23,7 @@
 dll = windll.version
 
 
-GetFileVersionInfoSize = WINFUNCTYPE(None)(("GetFileVersionInfoSizeW", dll))
+GetFileVersionInfoSize = dll.GetFileVersionInfoSizeW
 """
 Determines whether the operating system can retrieve version information for a specified file.
 
@@ -37,7 +36,7 @@
 	LPDWORD,  # lpdwHandle: Pointer to a variable that the function sets to zero (can be NULL)
 )
 
-GetFileVersionInfo = WINFUNCTYPE(None)(("GetFileVersionInfoW", dll))
+GetFileVersionInfo = dll.GetFileVersionInfoW
 """
 Retrieves version information for the specified file.
 
@@ -52,7 +51,7 @@
 	LPVOID,  # lpData: Pointer to a buffer that receives the file-version information
 )
 
-VerQueryValue = WINFUNCTYPE(None)(("VerQueryValueW", dll))
+VerQueryValue = dll.VerQueryValueW
 """
 Retrieves specified version information from the specified version-information resource.
 

```