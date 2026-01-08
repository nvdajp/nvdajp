# Diff for: `source\brailleDisplayDrivers\dotPad\driver.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\brailleDisplayDrivers\dotPad\driver.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\brailleDisplayDrivers\dotPad\driver.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\brailleDisplayDrivers\\dotPad\\driver.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleDisplayDrivers\\dotPad\\driver.py"
index 18b43e6..d7b0f5d 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\brailleDisplayDrivers\\dotPad\\driver.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\brailleDisplayDrivers\\dotPad\\driver.py"
@@ -9,10 +9,10 @@
 import operator
 import enum
 from dataclasses import dataclass
-import ctypes
 import serial
 import inputCore
 import braille
+import winBindings.kernel32
 import hwIo
 import bdDetect
 from logHandler import log
@@ -151,7 +151,7 @@ def _sendCommand(
 				if response is not None and response.cmd == rspCmd and response.dest == dest:
 					break
 				if x > 0:
-					ctypes.windll.kernel32.SleepEx(50, True)
+					winBindings.kernel32.SleepEx(50, True)
 			else:
 				raise RuntimeError(f"No response to {cmd.name}")
 			return response.data

```