# Diff for: `source\_remoteClient\localMachine.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\_remoteClient\localMachine.py`  
**Current**: `F:\nvda\gh\alphajp\source\_remoteClient\localMachine.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\localMachine.py" "b/F:\\nvda\\gh\\alphajp\\source\\_remoteClient\\localMachine.py"
index 0f319cc7eb..4221f3d283 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\_remoteClient\\localMachine.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\_remoteClient\\localMachine.py"
@@ -18,12 +18,12 @@
 	not be used directly outside of the remote connection infrastructure.
 """
 
-import ctypes
 from enum import IntEnum, nonmember
 import os
 from typing import Any, Dict, List, Optional
 import winreg
 
+import winBindings.sas
 import api
 import braille
 from config.registry import RegistryKey
@@ -284,7 +284,7 @@ def sendSAS(self) -> None:
 		:note: SendSAS requires UI Access. If this fails, a warning is displayed.
 		"""
 		if self._canSendSAS():
-			ctypes.windll.sas.SendSAS(not isRunningOnSecureDesktop())
+			winBindings.sas.SendSAS(not isRunningOnSecureDesktop())
 		else:
 			# Translators: Message displayed when a remote computer tries to send control+alt+delete but UI Access is disabled.
 			ui.message(pgettext("remote", "Unable to trigger control+alt+delete"))

```