# Diff for: `source\winUser.py`

**Source**: `F:\nvda\gh\beta\source\winUser.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winUser.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winUser.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winUser.py"
index 17ae727..2ade928 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winUser.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winUser.py"
@@ -275,7 +275,15 @@ class NMHdrStruct(Structure):
 VK_MENU = 18
 VK_PAUSE = 19
 VK_CAPITAL = 20
+# BEGIN JP PATCH
+# nvdajp: IME ON/OFF virtual key codes for Japanese IME support
+VK_IME_ON = 0x16
+# END JP PATCH
 VK_FINAL = 0x18
+# BEGIN JP PATCH
+# nvdajp: IME OFF virtual key code
+VK_IME_OFF = 0x1A
+# END JP PATCH
 VK_ESCAPE = 0x1B
 VK_CONVERT = 0x1C
 VK_NONCONVERT = 0x1D
@@ -554,8 +562,7 @@ def isDescendantWindow(parentHwnd, childHwnd):
 
 
 def getForegroundWindow() -> HWNDVal:
-	hwnd = _user32.GetForegroundWindow()
-	return hwnd or 0
+	return _user32.GetForegroundWindow()
 
 
 def setForegroundWindow(hwnd):
@@ -567,8 +574,7 @@ def setFocus(hwnd):
 
 
 def getDesktopWindow() -> HWNDVal:
-	hwnd = _user32.GetDesktopWindow()
-	return hwnd or 0
+	return _user32.GetDesktopWindow()
 
 
 def getControlID(hwnd):
@@ -620,8 +626,7 @@ def mouse_event(*args):
 
 
 def getAncestor(hwnd: HWNDVal, flags: int) -> HWNDVal:
-	hwnd = _user32.GetAncestor(hwnd, flags)
-	return hwnd or 0
+	return _user32.GetAncestor(hwnd, flags)
 
 
 def setCursorPos(x, y):
@@ -641,8 +646,7 @@ def getCaretPos():
 
 
 def getTopWindow(hwnd: HWNDVal) -> HWNDVal:
-	hwnd = _user32.GetTopWindow(hwnd)
-	return hwnd or 0
+	return _user32.GetTopWindow(hwnd)
 
 
 def getWindowText(hwnd):
@@ -652,8 +656,7 @@ def getWindowText(hwnd):
 
 
 def getWindow(window: HWNDVal, relation: int) -> HWNDVal:
-	hwnd = _user32.GetWindow(window, relation)
-	return hwnd or 0
+	return _user32.GetWindow(window, relation)
 
 
 def isWindowVisible(window):
@@ -688,10 +691,9 @@ def SetLayeredWindowAttributes(hwnd, key, alpha, flags):
 
 def getPreviousWindow(hwnd: HWNDVal) -> HWNDVal:
 	try:
-		hwnd = _user32.GetWindow(hwnd, GW_HWNDPREV)
+		return _user32.GetWindow(hwnd, GW_HWNDPREV)
 	except WindowsError:
 		return 0
-	return hwnd or 0
 
 
 def getKeyboardLayout(idThread=0):

```