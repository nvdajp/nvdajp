# Diff for: `source\winBindings\setupapi.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\setupapi.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\setupapi.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\setupapi.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\setupapi.py"
index 1ecb7c3..84d1d78 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\setupapi.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\setupapi.py"
@@ -5,16 +5,7 @@
 
 """Functions exported by setupapi.dll, and supporting data structures and enumerations."""
 
-from ctypes import (
-	WINFUNCTYPE,
-	POINTER,
-	Structure,
-	WinError,
-	c_void_p,
-	c_wchar_p,
-	sizeof,
-	windll,
-)
+from ctypes import POINTER, Structure, WinError, c_void_p, c_wchar_p, sizeof, windll
 from ctypes.wintypes import BOOL, DWORD, HKEY, HWND, PDWORD, PULONG, ULONG, WCHAR
 from enum import IntEnum
 
@@ -166,7 +157,7 @@ class _Dummy(Structure):
 PSP_DEVICE_INTERFACE_DETAIL_DATA = c_void_p
 
 
-SetupDiDestroyDeviceInfoList = WINFUNCTYPE(None)(("SetupDiDestroyDeviceInfoList", dll))
+SetupDiDestroyDeviceInfoList = dll.SetupDiDestroyDeviceInfoList
 """
 Deletes a device information set and frees all associated memory.
 
@@ -185,7 +176,7 @@ def _validHandle_errcheck(res, func, args):
 	return res
 
 
-SetupDiGetClassDevs = WINFUNCTYPE(None)(("SetupDiGetClassDevsW", dll))
+SetupDiGetClassDevs = dll.SetupDiGetClassDevsW
 """
 Returns a handle to a device information set that contains requested device information elements for a local computer.
 
@@ -201,7 +192,7 @@ def _validHandle_errcheck(res, func, args):
 SetupDiGetClassDevs.restype = HDEVINFO
 SetupDiGetClassDevs.errcheck = _validHandle_errcheck  # HDEVINFO
 
-SetupDiGetDeviceProperty = WINFUNCTYPE(None)(("SetupDiGetDevicePropertyW", dll))
+SetupDiGetDeviceProperty = dll.SetupDiGetDevicePropertyW
 """
 The SetupDiGetDeviceProperty function retrieves a device instance property.
 
@@ -220,7 +211,7 @@ def _validHandle_errcheck(res, func, args):
 )
 SetupDiGetDeviceProperty.restype = BOOL
 
-SetupDiEnumDeviceInterfaces = WINFUNCTYPE(None)(("SetupDiEnumDeviceInterfaces", dll))
+SetupDiEnumDeviceInterfaces = dll.SetupDiEnumDeviceInterfaces
 """
 Enumerates the device interfaces that are contained in a device information set.
 
@@ -236,7 +227,7 @@ def _validHandle_errcheck(res, func, args):
 )
 SetupDiEnumDeviceInterfaces.restype = BOOL
 
-SetupDiGetDeviceInterfaceDetail = WINFUNCTYPE(None)(("SetupDiGetDeviceInterfaceDetailW", dll))
+SetupDiGetDeviceInterfaceDetail = dll.SetupDiGetDeviceInterfaceDetailW
 """
 Returns details about a device interface.
 
@@ -253,7 +244,7 @@ def _validHandle_errcheck(res, func, args):
 )
 SetupDiGetDeviceInterfaceDetail.restype = BOOL
 
-SetupDiGetDeviceRegistryProperty = WINFUNCTYPE(None)(("SetupDiGetDeviceRegistryPropertyW", dll))
+SetupDiGetDeviceRegistryProperty = dll.SetupDiGetDeviceRegistryPropertyW
 """
 Retrieves a specified Plug and Play device property.
 
@@ -271,7 +262,7 @@ def _validHandle_errcheck(res, func, args):
 )
 SetupDiGetDeviceRegistryProperty.restype = BOOL
 
-SetupDiEnumDeviceInfo = WINFUNCTYPE(None)(("SetupDiEnumDeviceInfo", dll))
+SetupDiEnumDeviceInfo = dll.SetupDiEnumDeviceInfo
 """
 Returns a SP_DEVINFO_DATA structure that specifies a device information element in a device information set.
 
@@ -285,7 +276,7 @@ def _validHandle_errcheck(res, func, args):
 )
 SetupDiEnumDeviceInfo.restype = BOOL
 
-SetupDiOpenDevRegKey = WINFUNCTYPE(None)(("SetupDiOpenDevRegKey", dll))
+SetupDiOpenDevRegKey = dll.SetupDiOpenDevRegKey
 """
 Opens a registry key for device-specific configuration information.
 

```