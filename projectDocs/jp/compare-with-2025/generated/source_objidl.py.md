# Diff for: `source\objidl.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\objidl.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\objidl.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\objidl.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\objidl.py"
index 32d392e..71d2fa9 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\objidl.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\objidl.py"
@@ -1,13 +1,14 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2010-2021 NV Access Limited, Leonard de Ruijter, Joseph Lee
+# Copyright (C) 2010-2025 NV Access Limited, Leonard de Ruijter, Joseph Lee
 # This file may be used under the terms of the GNU General Public License, version 2 or later.
 # For more details see: https://www.gnu.org/licenses/gpl-2.0.html
 
-from ctypes import c_int, c_longlong, c_ubyte, c_ulong, c_ulonglong, c_wchar_p, POINTER, Structure, windll
+from ctypes import c_int, c_longlong, c_ubyte, c_ulong, c_ulonglong, c_wchar_p, POINTER, Structure
 from ctypes.wintypes import HWND, BOOL
 from comtypes import HRESULT, GUID, COMMETHOD, IUnknown, tagBIND_OPTS2
 from comtypes.persist import IPersist
-import winKernel
+import winBindings.ole32
+import winBindings.kernel32
 
 WSTRING = c_wchar_p
 
@@ -47,9 +48,9 @@ class tagSTATSTG(Structure):
 		("pwcsName", WSTRING),
 		("type", c_ulong),
 		("cbSize", _ULARGE_INTEGER),
-		("mtime", winKernel.FILETIME),
-		("ctime", winKernel.FILETIME),
-		("atime", winKernel.FILETIME),
+		("mtime", winBindings.kernel32.FILETIME),
+		("ctime", winBindings.kernel32.FILETIME),
+		("atime", winBindings.kernel32.FILETIME),
 		("grfMode", c_ulong),
 		("grfLocksSupported", c_ulong),
 		("clsid", GUID),
@@ -286,7 +287,7 @@ def GetDisplayName(self, pbc, pmkToLeft):
 		displayName = WSTRING()
 		self.__com_GetDisplayName(pbc, pmkToLeft, displayName)
 		ret = displayName.value
-		windll.ole32.CoTaskMemFree(displayName)
+		winBindings.ole32.CoTaskMemFree(displayName)
 		return ret
 
 
@@ -407,7 +408,7 @@ def __next__(self):
 		"GetTimeOfLastChange",
 		(["in"], POINTER(IBindCtx), "pbc"),
 		(["in"], POINTER(IMoniker), "pmkToLeft"),
-		(["out"], POINTER(winKernel.FILETIME), "pfiletime"),
+		(["out"], POINTER(winBindings.kernel32.FILETIME), "pfiletime"),
 	),
 	COMMETHOD(
 		[],
@@ -489,14 +490,14 @@ def __next__(self):
 		HRESULT,
 		"NoteChangeTime",
 		(["in"], c_ulong, "dwRegister"),
-		(["in"], POINTER(winKernel.FILETIME), "pfiletime"),
+		(["in"], POINTER(winBindings.kernel32.FILETIME), "pfiletime"),
 	),
 	COMMETHOD(
 		[],
 		HRESULT,
 		"GetTimeOfLastChange",
 		(["in"], POINTER(IMoniker), "pmkObjectName"),
-		(["out"], POINTER(winKernel.FILETIME), "pfiletime"),
+		(["out"], POINTER(winBindings.kernel32.FILETIME), "pfiletime"),
 	),
 	COMMETHOD(
 		[],

```