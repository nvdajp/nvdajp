# Diff for: `source\JABHandler.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\JABHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\JABHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\JABHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\JABHandler.py"
index 93dd36b..a2f74d6 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\JABHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\JABHandler.py"
@@ -1,6 +1,5 @@
-# -*- coding: UTF-8 -*-
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2007-2023 NV Access Limited, Peter Vágner, Renaud Paquay, Babbage B.V.
+# Copyright (C) 2007-2025 NV Access Limited, Peter Vágner, Renaud Paquay, Babbage B.V.
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -22,7 +21,6 @@
 	POINTER,
 	byref,
 	cdll,
-	windll,
 	CFUNCTYPE,
 	WinError,
 	create_string_buffer,
@@ -30,6 +28,8 @@
 )
 from ctypes.wintypes import BOOL, HWND, WCHAR
 import time
+from winBindings.kernel32 import FreeLibrary
+from winBindings import user32
 import queueHandler
 from logHandler import log
 import winUser
@@ -39,7 +39,7 @@
 import NVDAObjects.JAB
 import core
 import textUtils
-import NVDAHelper
+import NVDAState
 import config
 from utils.security import isRunningOnSecureDesktop
 
@@ -1136,9 +1136,7 @@ def enableBridge():
 def initialize():
 	global bridgeDll, isRunning
 	try:
-		bridgeDll = cdll.LoadLibrary(
-			os.path.join(NVDAHelper.versionedLibPath, "windowsaccessbridge-32.dll"),
-		)
+		bridgeDll = cdll.LoadLibrary(NVDAState.ReadPaths.javaAccessBridgeDLL)
 	except WindowsError:
 		raise NotImplementedError("dll not available")
 	_fixBridgeFuncs()
@@ -1148,10 +1146,10 @@ def initialize():
 	):
 		enableBridge()
 	# Accept wm_copydata and any wm_user messages from other processes even if running with higher privileges
-	if not windll.user32.ChangeWindowMessageFilter(winUser.WM_COPYDATA, winUser.MSGFLT.ALLOW):
+	if not user32.ChangeWindowMessageFilter(winUser.WM_COPYDATA, winUser.MSGFLT.ALLOW):
 		raise WinError()
 	for msg in range(winUser.WM_USER + 1, 0xFFFF):
-		if not windll.user32.ChangeWindowMessageFilter(msg, winUser.MSGFLT.ALLOW):
+		if not user32.ChangeWindowMessageFilter(msg, winUser.MSGFLT.ALLOW):
 			raise WinError()
 	bridgeDll.Windows_run()
 	# Register java events
@@ -1180,7 +1178,7 @@ def terminate():
 	bridgeDll.setPropertyCaretChangeFP(None)
 	h = bridgeDll._handle
 	bridgeDll = None
-	windll.kernel32.FreeLibrary(h)
+	FreeLibrary(h)
 	isRunning = False
 
 

```