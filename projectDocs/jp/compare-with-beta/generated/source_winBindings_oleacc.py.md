# Diff for: `source\winBindings\oleacc.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\oleacc.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\oleacc.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\oleacc.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\oleacc.py"
index 3259f54..38372ca 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\oleacc.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\oleacc.py"
@@ -6,7 +6,6 @@
 """Functions exported by oleacc.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	HRESULT,
 	windll,
 	POINTER,
@@ -30,7 +29,7 @@
 
 dll = windll.oleacc
 
-GetProcessHandleFromHwnd = WINFUNCTYPE(None)(("GetProcessHandleFromHwnd", dll))
+GetProcessHandleFromHwnd = dll.GetProcessHandleFromHwnd
 """
 Retrieves a process handle from a window handle.
 .. seealso::
@@ -41,7 +40,7 @@
 )
 GetProcessHandleFromHwnd.restype = HANDLE
 
-AccNotifyTouchInteraction = WINFUNCTYPE(None)(("AccNotifyTouchInteraction", dll))
+AccNotifyTouchInteraction = dll.AccNotifyTouchInteraction
 """
 Notifies the system that a touch interaction has occurred.
 .. seealso::
@@ -54,7 +53,7 @@
 )
 AccNotifyTouchInteraction.restype = HRESULT
 
-AccSetRunningUtilityState = WINFUNCTYPE(None)(("AccSetRunningUtilityState", dll))
+AccSetRunningUtilityState = dll.AccSetRunningUtilityState
 """
 Sets the running utility state for accessibility.
 .. seealso::
@@ -67,7 +66,7 @@
 )
 AccSetRunningUtilityState.restype = HRESULT
 
-AccessibleChildren = WINFUNCTYPE(None)(("AccessibleChildren", dll))
+AccessibleChildren = dll.AccessibleChildren
 """
 Retrieves the specified children of an accessible object.
 .. seealso::
@@ -82,7 +81,7 @@
 )
 AccessibleChildren.restype = HRESULT
 
-AccessibleObjectFromEvent = WINFUNCTYPE(None)(("AccessibleObjectFromEvent", dll))
+AccessibleObjectFromEvent = dll.AccessibleObjectFromEvent
 """
 Retrieves the address of the IAccessible interface for the object that generated the event and the child ID.
 .. seealso::
@@ -97,7 +96,7 @@
 )
 AccessibleObjectFromEvent.restype = HRESULT
 
-AccessibleObjectFromPoint = WINFUNCTYPE(None)(("AccessibleObjectFromPoint", dll))
+AccessibleObjectFromPoint = dll.AccessibleObjectFromPoint
 """
 Retrieves the address of the IAccessible interface pointer for the object displayed at a specified point on the screen.
 .. seealso::
@@ -110,7 +109,7 @@
 )
 AccessibleObjectFromPoint.restype = HRESULT
 
-AccessibleObjectFromWindow = WINFUNCTYPE(None)(("AccessibleObjectFromWindow", dll))
+AccessibleObjectFromWindow = dll.AccessibleObjectFromWindow
 """
 Retrieves the address of the IAccessible interface for the object associated with the specified window.
 .. seealso::
@@ -124,7 +123,7 @@
 )
 AccessibleObjectFromWindow.restype = HRESULT
 
-CreateStdAccessibleObject = WINFUNCTYPE(None)(("CreateStdAccessibleObject", dll))
+CreateStdAccessibleObject = dll.CreateStdAccessibleObject
 """
 Creates a standard object that exposes an IAccessible interface.
 .. seealso::
@@ -138,7 +137,7 @@
 )
 CreateStdAccessibleObject.restype = HRESULT
 
-CreateStdAccessibleProxy = WINFUNCTYPE(None)(("CreateStdAccessibleProxyW", dll))
+CreateStdAccessibleProxy = dll.CreateStdAccessibleProxyW
 """
 Creates a proxy accessible object for a window.
 .. seealso::
@@ -153,7 +152,7 @@
 )
 CreateStdAccessibleProxy.restype = HRESULT
 
-GetRoleText = WINFUNCTYPE(None)(("GetRoleTextW", dll))
+GetRoleText = dll.GetRoleTextW
 """
 Retrieves a localized string that describes an object's role for the specified role value.
 .. seealso::
@@ -166,7 +165,7 @@
 )
 GetRoleText.restype = c_uint
 
-GetStateText = WINFUNCTYPE(None)(("GetStateTextW", dll))
+GetStateText = dll.GetStateTextW
 """
 Retrieves a localized string that describes an object's state for the specified state value.
 .. seealso::
@@ -179,7 +178,7 @@
 )
 GetStateText.restype = c_uint
 
-LresultFromObject = WINFUNCTYPE(None)(("LresultFromObject", dll))
+LresultFromObject = dll.LresultFromObject
 """
 Creates an LRESULT value containing a pointer to a COM interface.
 .. seealso::
@@ -192,7 +191,7 @@
 )
 LresultFromObject.restype = LRESULT
 
-ObjectFromLresult = WINFUNCTYPE(None)(("ObjectFromLresult", dll))
+ObjectFromLresult = dll.ObjectFromLresult
 """
 Retrieves a COM interface pointer from an LRESULT value.
 .. seealso::
@@ -206,7 +205,7 @@
 )
 ObjectFromLresult.restype = HRESULT
 
-WindowFromAccessibleObject = WINFUNCTYPE(None)(("WindowFromAccessibleObject", dll))
+WindowFromAccessibleObject = dll.WindowFromAccessibleObject
 """
 Retrieves the window handle for the window that contains the specified accessible object.
 .. seealso::

```