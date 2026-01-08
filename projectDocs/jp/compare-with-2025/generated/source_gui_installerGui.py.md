# Diff for: `source\gui\installerGui.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\gui\installerGui.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\installerGui.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\installerGui.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\installerGui.py"
index 3ae574e..3c90c5e 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\gui\\installerGui.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\installerGui.py"
@@ -4,7 +4,6 @@
 # Copyright (C) 2011-2025 NV Access Limited, Babbage B.v., Cyrille Bougot, Julien Cochuyt, Accessolutions,
 # Bill Dengler, Joseph Lee, Takuya Nishimoto
 
-import ctypes
 import os
 import subprocess
 import sys
@@ -13,6 +12,7 @@
 import wx
 import config
 import core
+from winBindings import shell32
 import globalVars
 import installer
 from logHandler import log
@@ -25,16 +25,12 @@
 from NVDAState import WritePaths
 from .message import DialogType, MessageDialog, ReturnCode, displayDialogAsModal
 
-_IsUserAnAdmin = ctypes.windll.shell32.IsUserAnAdmin
-_IsUserAnAdmin.argtypes = []
-_IsUserAnAdmin.restype = ctypes.wintypes.BOOL
-
 
 def _shouldWarnBeforeUpdate() -> bool:
 	"""Whether or not a warning about being unable to complete installation when connected as follower should be shown to the user."""
 	from _remoteClient import _remoteClient
 
-	return _remoteClient is not None and _remoteClient.isConnectedAsFollower and not _IsUserAnAdmin()
+	return _remoteClient is not None and _remoteClient.isConnectedAsFollower and not shell32.IsUserAnAdmin()
 
 
 def _canPortableConfigBeCopied() -> bool:
@@ -144,7 +140,7 @@ def doInstall(
 	newNVDA = None
 	if startAfterInstall:
 		newNVDA = core.NewNVDAInstance(
-			filePath=os.path.join(installer.defaultInstallPath, "nvda.exe"),
+			filePath=os.path.join(WritePaths.defaultInstallDir, "nvda.exe"),
 			parameters=_generate_executionParameters(),
 		)
 	if not core.triggerNVDAExit(newNVDA):
@@ -223,11 +219,11 @@ def __init__(self, parent, isUpdate):
 				# Translators: An informational message in the Install NVDA dialog.
 				"A previous copy of NVDA has been found on your system. This copy will be updated.",
 			)
-			if not os.path.isdir(installer.defaultInstallPath):
+			if not os.path.isdir(WritePaths.defaultInstallDir):
 				msg += " " + _(
 					# Translators: a message in the installer telling the user NVDA is now located in a different place.
 					"The installation path for NVDA has changed. it will now  be installed in {path}",
-				).format(path=installer.defaultInstallPath)
+				).format(path=WritePaths.defaultInstallDir)
 		if shouldAskAboutAddons:
 			msg += "\n\n" + getAddonCompatibilityMessage()
 

```