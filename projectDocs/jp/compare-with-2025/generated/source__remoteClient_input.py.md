# Diff for: `source\_remoteClient\input.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\_remoteClient\input.py`  
**Current**: `F:\nvda\gh\alphajp\source\_remoteClient\input.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\input.py" "b/F:\\nvda\\gh\\alphajp\\source\\_remoteClient\\input.py"
index e3caca524c..678b08489d 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\input.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\_remoteClient\\input.py"
@@ -14,6 +14,7 @@
 import globalPluginHandler
 import scriptHandler
 import vision
+from winBindings import user32
 
 
 class InputType(IntEnum):
@@ -221,10 +222,10 @@ def sendKey(vk: int | None = None, scan: int | None = None, extended: bool = Fal
 	if scan:
 		i.union.ki.wScan = scan
 	else:  # No scancode provided, try to get one
-		i.union.ki.wScan = ctypes.windll.user32.MapVirtualKeyW(vk, VKMapType.VK_TO_VSC)
+		i.union.ki.wScan = user32.MapVirtualKey(vk, VKMapType.VK_TO_VSC)
 	if not pressed:
 		i.union.ki.dwFlags |= KeyEventFlag.KEY_UP
 	if extended:
 		i.union.ki.dwFlags |= KeyEventFlag.EXTENDED_KEY
 	i.type = InputType.KEYBOARD
-	ctypes.windll.user32.SendInput(1, ctypes.byref(i), ctypes.sizeof(INPUT))
+	user32.SendInput(1, ctypes.byref(i), ctypes.sizeof(INPUT))

```