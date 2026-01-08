# Diff for: `source\vkCodes.py`

**Source**: `F:\nvda\gh\beta\source\vkCodes.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\vkCodes.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\vkCodes.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\vkCodes.py"
index 63c801c..72225fd 100644
--- "a/F:\\nvda\\gh\\beta\\source\\vkCodes.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\vkCodes.py"
@@ -31,6 +31,7 @@
 	(0x13, None): "pause",
 	(0x14, None): "capsLock",
 	(0x18, None): "IMEFinalMode",
+	(0x19, None): "IMEChangeStatus1",  # nvdajp: IME status change key 1
 	(0x1B, None): "escape",
 	(0x1C, None): "IMEConvert",
 	(0x1D, None): "IMENonconvert",
@@ -132,6 +133,11 @@
 	(0xB5, None): "launchMediaPlayer",
 	(0xB6, None): "launchApp1",
 	(0xB7, None): "launchApp2",
+	# BEGIN JP PATCH
+	# nvdajp: IME status change keys 2 and 3
+	(0xF3, None): "IMEChangeStatus2",
+	(0xF4, None): "IMEChangeStatus3",
+	# END JP PATCH
 }
 
 #: Maps key names to vk codes.

```