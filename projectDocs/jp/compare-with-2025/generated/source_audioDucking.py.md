# Diff for: `source\audioDucking.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\audioDucking.py`  
**Current**: `F:\nvda\gh\alphajp\source\audioDucking.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\audioDucking.py" "b/F:\\nvda\\gh\\alphajp\\source\\audioDucking.py"
index c9709cfac8..02335f387b 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\audioDucking.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\audioDucking.py"
@@ -7,8 +7,10 @@
 from utils.displayString import DisplayStringIntEnum
 import threading
 from typing import Dict
-from ctypes import oledll, wintypes, windll
+from ctypes import wintypes, windll
 import time
+import winBindings.oleacc
+import winBindings.kernel32
 import config
 from logHandler import log
 import systemUtils
@@ -25,7 +27,7 @@ def __init__(self):
 
 	def __del__(self):
 		if self:
-			windll.kernel32.CloseHandle(self)
+			winBindings.kernel32.CloseHandle(self)
 
 
 WAIT_TIMEOUT = 0x102
@@ -74,14 +76,14 @@ def _setDuckingState(switch):
 
 			ATWindow = gui.mainFrame.GetHandle()
 			if switch:
-				oledll.oleacc.AccSetRunningUtilityState(
+				winBindings.oleacc.AccSetRunningUtilityState(
 					ATWindow,
 					ANRUSDucking.AUDIO_ACTIVE | ANRUSDucking.AUDIO_ACTIVE_NODUCK,
 					ANRUSDucking.AUDIO_ACTIVE | ANRUSDucking.AUDIO_ACTIVE_NODUCK,
 				)
 				_lastDuckedTime = time.time()
 			else:
-				oledll.oleacc.AccSetRunningUtilityState(
+				winBindings.oleacc.AccSetRunningUtilityState(
 					ATWindow,
 					ANRUSDucking.AUDIO_ACTIVE | ANRUSDucking.AUDIO_ACTIVE_NODUCK,
 					ANRUSDucking.AUDIO_ACTIVE_NODUCK,
@@ -179,10 +181,7 @@ def initialize():
 def isAudioDuckingSupported():
 	global _isAudioDuckingSupported
 	if _isAudioDuckingSupported is None:
-		_isAudioDuckingSupported = (config.isInstalledCopy() or config.isAppX) and hasattr(
-			oledll.oleacc,
-			"AccSetRunningUtilityState",
-		)
+		_isAudioDuckingSupported = config.isInstalledCopy()
 		_isAudioDuckingSupported &= systemUtils.hasUiAccess()
 	return _isAudioDuckingSupported
 

```