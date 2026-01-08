# Diff for: `source\_remoteClient\input.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\_remoteClient\input.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\_remoteClient\input.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\input.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\input.py"
index e3caca5..4dcfdb9 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\input.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\_remoteClient\\input.py"
@@ -4,8 +4,7 @@
 # See the file COPYING for more details.
 
 import ctypes
-from ctypes import POINTER, Structure, Union, c_long, c_ulong, wintypes
-from enum import IntEnum, IntFlag
+from enum import IntEnum
 
 import api
 import baseObject
@@ -14,23 +13,7 @@
 import globalPluginHandler
 import scriptHandler
 import vision
-
-
-class InputType(IntEnum):
-	"""Values permissible as the `type` field in an `INPUT` struct.
-
-	.. seealso::
-		https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input
-	"""
-
-	MOUSE = 0
-	"""The event is a mouse event. Use the mi structure of the union."""
-
-	KEYBOARD = 1
-	"""The event is a keyboard event. Use the ki structure of the union."""
-
-	HARDWARE = 2
-	"""The event is a hardware event. Use the hi structure of the union."""
+from winBindings import user32
 
 
 class VKMapType(IntEnum):
@@ -44,80 +27,6 @@ class VKMapType(IntEnum):
 	"""Maps a virtual key code to a scan code."""
 
 
-class KeyEventFlag(IntFlag):
-	"""Specifies various aspects of a keystroke in a KEYBDINPUT struct.
-
-	.. seealso::
-		https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-keybdinput
-	"""
-
-	EXTENDED_KEY = 0x0001
-	"""If specified, the wScan scan code consists of a sequence of two bytes, where the first byte has a value of 0xE0."""
-
-	KEY_UP = 0x0002
-	"""If specified, the key is being released. If not specified, the key is being pressed. """
-
-	SCAN_CODE = 0x0008
-	"""If specified, wScan identifies the key and wVk is ignored. """
-
-	UNICODE = 0x0004
-	"""If specified, the system synthesizes a VK_PACKET keystroke.
-
-	.. warning::
-		Must only be combined with :const:`KEY_UP`.
-	"""
-
-
-class MOUSEINPUT(Structure):
-	_fields_ = (
-		("dx", c_long),
-		("dy", c_long),
-		("mouseData", wintypes.DWORD),
-		("dwFlags", wintypes.DWORD),
-		("time", wintypes.DWORD),
-		("dwExtraInfo", POINTER(c_ulong)),
-	)
-
-
-class KEYBDINPUT(Structure):
-	_fields_ = (
-		("wVk", wintypes.WORD),
-		("wScan", wintypes.WORD),
-		("dwFlags", wintypes.DWORD),
-		("time", wintypes.DWORD),
-		("dwExtraInfo", POINTER(c_ulong)),
-	)
-
-
-class HARDWAREINPUT(Structure):
-	_fields_ = (
-		("uMsg", wintypes.DWORD),
-		("wParamL", wintypes.WORD),
-		("wParamH", wintypes.WORD),
-	)
-
-
-class INPUTUnion(Union):
-	_fields_ = (
-		("mi", MOUSEINPUT),
-		("ki", KEYBDINPUT),
-		("hi", HARDWAREINPUT),
-	)
-
-
-class INPUT(Structure):
-	"""Stores information for synthesizing input events.
-
-	.. seealso::
-		https://learn.microsoft.com/en-us/windows/win32/api/winuser/ns-winuser-input
-	"""
-
-	_fields_ = (
-		("type", wintypes.DWORD),
-		("union", INPUTUnion),
-	)
-
-
 class BrailleInputGesture(braille.BrailleDisplayGesture, brailleInput.BrailleInputGesture):
 	def __init__(self, **kwargs):
 		super().__init__()
@@ -216,15 +125,15 @@ def sendKey(vk: int | None = None, scan: int | None = None, extended: bool = Fal
 	:param extended: Whether this is an extended key, defaults to False
 	:param pressed: ``True`` if key pressed; ``False`` if released, defaults to True
 	"""
-	i = INPUT()
-	i.union.ki.wVk = vk
+	input = user32.INPUT()
+	input.ii.ki.wVk = vk
 	if scan:
-		i.union.ki.wScan = scan
+		input.ii.ki.wScan = scan
 	else:  # No scancode provided, try to get one
-		i.union.ki.wScan = ctypes.windll.user32.MapVirtualKeyW(vk, VKMapType.VK_TO_VSC)
+		input.ii.ki.wScan = user32.MapVirtualKey(vk, VKMapType.VK_TO_VSC)
 	if not pressed:
-		i.union.ki.dwFlags |= KeyEventFlag.KEY_UP
+		input.ii.ki.dwFlags |= user32.KEYEVENTF.KEYUP
 	if extended:
-		i.union.ki.dwFlags |= KeyEventFlag.EXTENDED_KEY
-	i.type = InputType.KEYBOARD
-	ctypes.windll.user32.SendInput(1, ctypes.byref(i), ctypes.sizeof(INPUT))
+		input.ii.ki.dwFlags |= user32.KEYEVENTF.EXTENDEDKEY
+	input.type = user32.INPUT_TYPE.KEYBOARD
+	user32.SendInput(1, ctypes.byref(input), ctypes.sizeof(user32.INPUT))

```