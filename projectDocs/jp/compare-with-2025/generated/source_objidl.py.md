# Diff for: `source\objidl.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\objidl.py`  
**Current**: `F:\nvda\gh\alphajp\source\objidl.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\objidl.py" "b/F:\\nvda\\gh\\alphajp\\source\\objidl.py"
index 32d392e889..566b5a8478 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\objidl.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\objidl.py"
@@ -3,10 +3,11 @@
 # This file may be used under the terms of the GNU General Public License, version 2 or later.
 # For more details see: https://www.gnu.org/licenses/gpl-2.0.html
 
-from ctypes import c_int, c_longlong, c_ubyte, c_ulong, c_ulonglong, c_wchar_p, POINTER, Structure, windll
+from ctypes import c_int, c_longlong, c_ubyte, c_ulong, c_ulonglong, c_wchar_p, POINTER, Structure
 from ctypes.wintypes import HWND, BOOL
 from comtypes import HRESULT, GUID, COMMETHOD, IUnknown, tagBIND_OPTS2
 from comtypes.persist import IPersist
+import winBindings.ole32
 import winKernel
 
 WSTRING = c_wchar_p
@@ -286,7 +287,7 @@ def GetDisplayName(self, pbc, pmkToLeft):
 		displayName = WSTRING()
 		self.__com_GetDisplayName(pbc, pmkToLeft, displayName)
 		ret = displayName.value
-		windll.ole32.CoTaskMemFree(displayName)
+		winBindings.ole32.CoTaskMemFree(displayName)
 		return ret
 
 

```