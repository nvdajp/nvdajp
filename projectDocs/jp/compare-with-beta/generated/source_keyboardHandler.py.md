# Diff for: `source\keyboardHandler.py`

**Source**: `F:\nvda\gh\beta\source\keyboardHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\keyboardHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\keyboardHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\keyboardHandler.py"
index f8115d4..f3f471f 100644
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
 
 

```