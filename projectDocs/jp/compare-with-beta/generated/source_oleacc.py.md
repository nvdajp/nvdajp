# Diff for: `source\oleacc.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\oleacc.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\oleacc.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\oleacc.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\oleacc.py"
index 1c6168d..c1457e9 100644
--- "a/F:\\nvda\\gh\\beta\\source\\oleacc.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\oleacc.py"
@@ -5,7 +5,6 @@
 
 from ctypes import *  # noqa: F403
 from ctypes.wintypes import *  # noqa: F403
-from ctypes.wintypes import HWND
 from comtypes import *  # noqa: F403
 from comtypes.automation import *  # noqa: F403
 import comtypes.client
@@ -313,16 +312,17 @@ def AccessibleObjectFromEvent_safe(hwnd, objectID, childID, timeout=2):
 	return (obj, childID)
 
 
-def WindowFromAccessibleObject(pacc) -> int:
+def WindowFromAccessibleObject(pacc):
 	"""
-	Retrieves the handle of the window this IAccessible object belongs to.
-	:param pacc: the IAccessible object who's window you want to fetch.
-	:type pacc: POINTER(IAccessible)
-	:return: the window handle.
+	Retreaves the handle of the window this IAccessible object belongs to.
+	@param pacc: the IAccessible object who's window you want to fetch.
+	@type pacc: POINTER(IAccessible)
+	@return: the window handle.
+	@rtype: int
 	"""
-	hwnd = HWND()
+	hwnd = c_int()  # noqa: F405
 	winBindings.oleacc.WindowFromAccessibleObject(pacc, byref(hwnd))  # noqa: F405
-	return hwnd.value or 0
+	return hwnd.value
 
 
 def AccessibleObjectFromPoint(x, y):

```