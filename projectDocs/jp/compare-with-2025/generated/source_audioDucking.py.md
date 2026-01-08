# Diff for: `source\audioDucking.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\audioDucking.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\audioDucking.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\audioDucking.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\audioDucking.py"
index c9709cf..17fb7bd 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\audioDucking.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\audioDucking.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2015-2021 NV Access Limited
+# Copyright (C) 2015-2025 NV Access Limited
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -7,8 +7,10 @@
 from utils.displayString import DisplayStringIntEnum
 import threading
 from typing import Dict
-from ctypes import oledll, wintypes, windll
+from ctypes import wintypes
 import time
+import winBindings.oleacc
+import winBindings.kernel32
 import config
 from logHandler import log
 import systemUtils
@@ -20,12 +22,12 @@ def _isDebug():
 
 class AutoEvent(wintypes.HANDLE):
 	def __init__(self):
-		e = windll.kernel32.CreateEventW(None, True, False, None)
+		e = winBindings.kernel32.CreateEvent(None, True, False, None)
 		super(AutoEvent, self).__init__(e)
 
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
@@ -151,7 +153,7 @@ def setAudioDuckingMode(mode):
 		oldMode = _audioDuckingMode
 		_audioDuckingMode = mode
 		if _modeChangeEvent:
-			windll.kernel32.SetEvent(_modeChangeEvent)
+			winBindings.kernel32.SetEvent(_modeChangeEvent)
 		_modeChangeEvent = AutoEvent()
 		if _isDebug():
 			log.debug("Switched modes from %s, to %s" % (oldMode, mode))
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
 
@@ -239,7 +238,7 @@ def enable(self):
 		if debug:
 			log.debug("waiting %s ms or mode change" % deltaMS)
 		wasCanceled = (
-			windll.kernel32.WaitForMultipleObjects(
+			winBindings.kernel32.WaitForMultipleObjects(
 				2,
 				(wintypes.HANDLE * 2)(disableEvent, modeChangeEvent),
 				False,
@@ -265,5 +264,5 @@ def disable(self):
 			if _isDebug():
 				log.debug("disabling")
 			_unensureDucked()
-			windll.kernel32.SetEvent(self._disabledEvent)
+			winBindings.kernel32.SetEvent(self._disabledEvent)
 			return True

```