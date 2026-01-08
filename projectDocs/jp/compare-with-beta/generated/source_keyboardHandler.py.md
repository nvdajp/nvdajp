# Diff for: `source\keyboardHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\keyboardHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\keyboardHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\keyboardHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\keyboardHandler.py"
index f8115d4..a52ae1f 100644
--- "a/F:\\nvda\\gh\\beta\\source\\keyboardHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\keyboardHandler.py"
@@ -112,6 +112,16 @@ def isNVDAModifierKey(vkCode: int, extended: bool) -> bool:
 		return True
 	elif (config.conf["keyboard"]["NVDAModifierKeys"] & NVDAKey.CAPS_LOCK) and vkCode == winUser.VK_CAPITAL:
 		return True
+	elif config.conf["keyboard"]["useNonConvertAsNVDAModifierKey"] and (
+		vkCode == winUser.VK_NONCONVERT or (vkCode == winUser.VK_IME_OFF and extended)
+	):  # nvdajp
+		return True
+	elif config.conf["keyboard"]["useConvertAsNVDAModifierKey"] and (
+		vkCode == winUser.VK_CONVERT or (vkCode == winUser.VK_IME_ON and extended)
+	):  # nvdajp
+		return True
+	elif config.conf["keyboard"]["useEscapeAsNVDAModifierKey"] and vkCode == winUser.VK_ESCAPE:  # nvdajp
+		return True
 	else:
 		return False
 
@@ -317,6 +327,12 @@ def internal_keyDownEvent(vkCode, scanCode, extended, injected):
 			if res > 0:
 				for ch in charBuf[:res]:
 					eventHandler.queueEvent("typedCharacter", focus, ch=ch)
+	# nvdajp begin
+	if config.conf["keyboard"]["nvdajpEnableKeyEvents"]:
+		from NVDAObjects import inputComposition
+
+		inputComposition.reportKeyDownEvent(gesture)
+	# nvdajp end
 	return True
 
 
@@ -529,9 +545,7 @@ def _get_mainKeyName(self):
 			# Unicode character from non-keyboard input.
 			return chr(self.scanCode)
 		vkChar = user32.MapVirtualKeyEx(self.vkCode, winUser.MAPVK_VK_TO_CHAR, getInputHkl())
-		# the highest bit of a 32 bit value denotes a dead key
-		DEAD_KEY_FLAG = 0x80000000
-		if vkChar > 0 and not (vkChar & DEAD_KEY_FLAG):
+		if vkChar > 0:
 			if vkChar == 43:  # "+"
 				# A gesture identifier can't include "+" except as a separator.
 				return "plus"
@@ -647,7 +661,7 @@ def executeScript(self, script):
 			# it is already too late.
 			with ignoreInjection():
 				winUser.keybd_event(winUser.VK_NONE, 0, 0, 0)
-				winUser.keybd_event(winUser.VK_NONE, 0, user32.KEYEVENTF.KEYUP, 0)
+				winUser.keybd_event(winUser.VK_NONE, 0, winBindings.user32.KEYEVENTF.KEYUP, 0)
 		# Now actually execute the script.
 		super().executeScript(script)
 
@@ -759,7 +773,6 @@ def getDisplayTextForIdentifier(cls, identifier):
 		keys = set(keys.split("+"))
 		names = []
 		main = None
-		numlock = None
 		try:
 			# If present, the NVDA key should appear first.
 			keys.remove("nvda")
@@ -776,15 +789,9 @@ def getDisplayTextForIdentifier(cls, identifier):
 			label = localizedKeyLabels.get(key, key)
 			if vk in cls.NORMAL_MODIFIER_KEYS:
 				names.append(label)
-			elif vk == winUser.VK_NUMLOCK:
-				# Numlock can be both modifier or main key so handle it separately and add it at the end after modifiers
-				# but before main key
-				numlock = label
 			else:
 				# The main key must be last, so handle that outside the loop.
 				main = label
-		if numlock is not None:
-			names.append(numlock)
 		if main is not None:
 			# If there is no main key, this gesture identifier only contains modifiers.
 			names.append(main)

```