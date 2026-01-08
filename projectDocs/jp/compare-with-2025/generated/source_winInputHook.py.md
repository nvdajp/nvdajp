# Diff for: `source\winInputHook.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\winInputHook.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winInputHook.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\winInputHook.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winInputHook.py"
index 306c8c2..dccfb54 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\winInputHook.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winInputHook.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2006-2019 NV Access Limited
+# Copyright (C) 2006-2025 NV Access Limited
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -8,10 +8,22 @@
 """
 
 import threading
-from ctypes import *  # noqa: F403
-from ctypes.wintypes import *  # noqa: F403
+from ctypes import (
+	Structure,
+	byref,
+	c_void_p,
+)
+from ctypes.wintypes import (
+	MSG,
+	DWORD,
+	POINT,
+)
+
+import winBindings.user32
 import watchdog
 import winUser
+from winBindings import user32, kernel32
+
 
 # Some Windows constants
 HC_ACTION = 0
@@ -43,15 +55,18 @@ class MSLLHOOKSTRUCT(Structure):  # noqa: F405
 	]
 
 
+LRESULT = c_void_p
+
+
 keyDownCallback = None
 keyUpCallback = None
 mouseCallback = None
 
 
-@WINFUNCTYPE(c_long, c_int, WPARAM, LPARAM)  # noqa: F405
+@user32.HOOKPROC
 def keyboardHook(code, wParam, lParam):
 	if code != HC_ACTION:
-		return windll.user32.CallNextHookEx(0, code, wParam, lParam)  # noqa: F405
+		return user32.CallNextHookEx(0, code, wParam, lParam)  # noqa: F405
 	kbd = KBDLLHOOKSTRUCT.from_address(lParam)
 	if keyUpCallback and kbd.flags & LLKHF_UP:
 		if not keyUpCallback(
@@ -69,18 +84,18 @@ def keyboardHook(code, wParam, lParam):
 			bool(kbd.flags & LLKHF_INJECTED),
 		):
 			return 1
-	return windll.user32.CallNextHookEx(0, code, wParam, lParam)  # noqa: F405
+	return user32.CallNextHookEx(0, code, wParam, lParam)  # noqa: F405
 
 
-@WINFUNCTYPE(c_long, c_int, WPARAM, LPARAM)  # noqa: F405
+@user32.HOOKPROC
 def mouseHook(code, wParam, lParam):
 	if watchdog.isAttemptingRecovery or code != HC_ACTION:
-		return windll.user32.CallNextHookEx(0, code, wParam, lParam)  # noqa: F405
+		return user32.CallNextHookEx(0, code, wParam, lParam)  # noqa: F405
 	msll = MSLLHOOKSTRUCT.from_address(lParam)
 	if mouseCallback:
 		if not mouseCallback(wParam, msll.pt.x, msll.pt.y, msll.flags & LLMHF_INJECTED):
 			return 1
-	return windll.user32.CallNextHookEx(0, code, wParam, lParam)  # noqa: F405
+	return user32.CallNextHookEx(0, code, wParam, lParam)  # noqa: F405
 
 
 hookThread = None
@@ -88,28 +103,28 @@ def mouseHook(code, wParam, lParam):
 
 
 def hookThreadFunc():
-	keyHookID = windll.user32.SetWindowsHookExW(  # noqa: F405
+	keyHookID = user32.SetWindowsHookEx(  # noqa: F405
 		WH_KEYBOARD_LL,
 		keyboardHook,
-		windll.kernel32.GetModuleHandleW(None),  # noqa: F405
+		kernel32.GetModuleHandle(None),  # noqa: F405
 		0,  # noqa: F405
 	)  # noqa: F405
 	if keyHookID == 0:
 		raise OSError("Could not register keyboard hook")
-	mouseHookID = windll.user32.SetWindowsHookExW(  # noqa: F405
+	mouseHookID = user32.SetWindowsHookEx(  # noqa: F405
 		WH_MOUSE_LL,
 		mouseHook,
-		windll.kernel32.GetModuleHandleW(None),  # noqa: F405
+		kernel32.GetModuleHandle(None),  # noqa: F405
 		0,  # noqa: F405
 	)  # noqa: F405
 	if mouseHookID == 0:
 		raise OSError("Could not register mouse hook")
 	msg = MSG()  # noqa: F405
-	while windll.user32.GetMessageW(byref(msg), None, 0, 0):  # noqa: F405
+	while winBindings.user32.GetMessage(byref(msg), None, 0, 0):  # noqa: F405
 		pass
-	if windll.user32.UnhookWindowsHookEx(keyHookID) == 0:  # noqa: F405
+	if user32.UnhookWindowsHookEx(keyHookID) == 0:  # noqa: F405
 		raise OSError("could not unregister key hook %s" % keyHookID)
-	if windll.user32.UnhookWindowsHookEx(mouseHookID) == 0:  # noqa: F405
+	if user32.UnhookWindowsHookEx(mouseHookID) == 0:  # noqa: F405
 		raise OSError("could not unregister mouse hook %s" % mouseHookID)
 
 
@@ -141,6 +156,6 @@ def terminate():
 		raise RuntimeError("winInputHook not running")
 	hookThreadRefCount -= 1
 	if hookThreadRefCount == 0:
-		windll.user32.PostThreadMessageW(hookThread.ident, winUser.WM_QUIT, 0, 0)  # noqa: F405
+		user32.PostThreadMessage(hookThread.ident, winUser.WM_QUIT, 0, 0)  # noqa: F405
 		hookThread.join()
 		hookThread = None

```