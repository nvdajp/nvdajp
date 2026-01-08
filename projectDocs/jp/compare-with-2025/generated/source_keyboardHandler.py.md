# Diff for: `source\keyboardHandler.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\keyboardHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\keyboardHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\keyboardHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\keyboardHandler.py"
index 2d075a4..a52ae1f 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\keyboardHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\keyboardHandler.py"
@@ -1,4 +1,3 @@
-# -*- coding: UTF-8 -*-
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
@@ -15,7 +14,6 @@
 	List,
 	Optional,
 	Any,
-	TypeAlias,
 )
 
 import winVersion
@@ -36,7 +34,9 @@
 import NVDAState
 from contextlib import contextmanager
 import threading
+import winBindings.kernel32
 import winKernel
+from winBindings import user32
 
 if typing.TYPE_CHECKING:
 	from NVDAObjects import NVDAObject  # noqa: F401
@@ -46,7 +46,7 @@
 ignoreInjected = False
 _lastInjectedKeyUp: tuple[int, int] | None = None
 _injectionDoneEvent: int | None = None
-_ModifierT: TypeAlias = tuple[int, bool]
+type _ModifierT = tuple[int, bool]
 
 # Fake vk codes.
 # These constants should be assigned to the name that NVDA will use for the key.
@@ -308,14 +308,14 @@ def internal_keyDownEvent(vkCode, scanCode, extended, injected):
 			and not isNVDAModifierKey(vkCode, extended)
 			and vkCode not in KeyboardInputGesture.NORMAL_MODIFIER_KEYS
 		):
-			keyStates = (ctypes.c_byte * 256)()
+			keyStates = (ctypes.c_ubyte * 256)()
 			for k in range(256):
-				keyStates[k] = ctypes.windll.user32.GetKeyState(k)
+				keyStates[k] = user32.GetKeyState(k)
 			charBuf = ctypes.create_unicode_buffer(5)
-			hkl = ctypes.windll.user32.GetKeyboardLayout(focus.windowThreadID)
+			hkl = user32.GetKeyboardLayout(focus.windowThreadID)
 			# In previous Windows builds, calling ToUnicodeEx would destroy keyboard buffer state and therefore cause the app to not produce the right WM_CHAR message.
 			# However, ToUnicodeEx now can take a new flag of 0x4, which stops it from destroying keyboard state, thus allowing us to safely call it here.
-			res = ctypes.windll.user32.ToUnicodeEx(
+			res = user32.ToUnicodeEx(
 				vkCode,
 				scanCode,
 				keyStates,
@@ -360,7 +360,7 @@ def internal_keyUpEvent(vkCode, scanCode, extended, injected):
 				return True
 			if ignoreInjected:
 				if keyCode == _lastInjectedKeyUp:
-					winKernel.kernel32.SetEvent(_injectionDoneEvent)
+					winBindings.kernel32.SetEvent(_injectionDoneEvent)
 				return True
 
 		if passKeyThroughCount >= 1:
@@ -418,7 +418,7 @@ def getInputHkl():
 		thread = focus.windowThreadID
 	else:
 		thread = 0
-	return winUser.user32.GetKeyboardLayout(thread)
+	return user32.GetKeyboardLayout(thread)
 
 
 def canModifiersPerformAction(modifiers):
@@ -544,7 +544,7 @@ def _get_mainKeyName(self):
 		if self.vkCode == vkCodes.VK_PACKET:
 			# Unicode character from non-keyboard input.
 			return chr(self.scanCode)
-		vkChar = winUser.user32.MapVirtualKeyExW(self.vkCode, winUser.MAPVK_VK_TO_CHAR, getInputHkl())
+		vkChar = user32.MapVirtualKeyEx(self.vkCode, winUser.MAPVK_VK_TO_CHAR, getInputHkl())
 		if vkChar > 0:
 			if vkChar == 43:  # "+"
 				# A gesture identifier can't include "+" except as a separator.
@@ -661,7 +661,7 @@ def executeScript(self, script):
 			# it is already too late.
 			with ignoreInjection():
 				winUser.keybd_event(winUser.VK_NONE, 0, 0, 0)
-				winUser.keybd_event(winUser.VK_NONE, 0, winUser.KEYEVENTF_KEYUP, 0)
+				winUser.keybd_event(winUser.VK_NONE, 0, winBindings.user32.KEYEVENTF.KEYUP, 0)
 		# Now actually execute the script.
 		super().executeScript(script)
 
@@ -817,7 +817,7 @@ def injectRawKeyboardInput(isPress, code, isExtended):
 	if isExtended:
 		# Change what we pass to MapVirtualKeyEx, but don't change what NVDA gets.
 		mapScan |= 0xE000
-	vkCode = winUser.user32.MapVirtualKeyExW(mapScan, winUser.MAPVK_VSC_TO_VK_EX, getInputHkl())
+	vkCode = user32.MapVirtualKeyEx(mapScan, winUser.MAPVK_VSC_TO_VK_EX, getInputHkl())
 	flags = 0
 	if not isPress:
 		flags |= 2

```