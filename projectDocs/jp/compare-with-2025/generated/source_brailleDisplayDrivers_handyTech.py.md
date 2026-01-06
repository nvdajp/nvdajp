# Diff for: `source\brailleDisplayDrivers\handyTech.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\brailleDisplayDrivers\handyTech.py`  
**Current**: `F:\nvda\gh\alphajp\source\brailleDisplayDrivers\handyTech.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\brailleDisplayDrivers\\handyTech.py" "b/F:\\nvda\\gh\\alphajp\\source\\brailleDisplayDrivers\\handyTech.py"
index e68555bf72..ecba0ec644 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\brailleDisplayDrivers\\handyTech.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\brailleDisplayDrivers\\handyTech.py"
@@ -1,7 +1,7 @@
 # A part of NonVisual Desktop Access (NVDA)
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
-# Copyright (C) 2008-2023 NV Access Limited, Bram Duvigneau, Babbage B.V.,
+# Copyright (C) 2008-2025 NV Access Limited, Bram Duvigneau, Babbage B.V.,
 # Felix Grützmacher (Handy Tech Elektronik GmbH), Leonard de Ruijter
 
 """
@@ -31,7 +31,7 @@
 import bdDetect
 import time
 import datetime
-from ctypes import windll
+from winBindings import user32
 import windowUtils
 
 import wx
@@ -48,7 +48,7 @@ def __init__(self):
 		# Register shared window message.
 		# Note: There is no corresponding unregister function.
 		# Still this does no harm if done repeatedly.
-		self.window_message = windll.user32.RegisterWindowMessageW("Handy_Tech_Server")
+		self.window_message = user32.RegisterWindowMessage("Handy_Tech_Server")
 
 	def windowProc(self, hwnd: int, msg: int, wParam: int, lParam: int):
 		if msg == self.window_message:

```