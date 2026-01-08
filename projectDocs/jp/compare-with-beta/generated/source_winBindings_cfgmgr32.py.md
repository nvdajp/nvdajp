# Diff for: `source\winBindings\cfgmgr32.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\cfgmgr32.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\cfgmgr32.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\cfgmgr32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\cfgmgr32.py"
index faf7d36..56d1ac2 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\cfgmgr32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\cfgmgr32.py"
@@ -5,11 +5,7 @@
 
 """Functions exported by cfgmgr32.dll, and supporting data structures and enumerations."""
 
-from ctypes import (
-	WINFUNCTYPE,
-	c_wchar_p,
-	windll,
-)
+from ctypes import c_wchar_p, windll
 from ctypes.wintypes import DWORD, ULONG
 
 dll = windll.cfgmgr32
@@ -17,7 +13,7 @@
 CR_SUCCESS = 0
 MAX_DEVICE_ID_LEN = 200
 
-CM_Get_Device_ID = WINFUNCTYPE(None)(("CM_Get_Device_IDW", dll))
+CM_Get_Device_ID = dll.CM_Get_Device_IDW
 """
 Retrieves the device instance ID for a specified device instance on the local machine.
 

```