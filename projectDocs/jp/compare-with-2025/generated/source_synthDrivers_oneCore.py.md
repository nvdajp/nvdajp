# Diff for: `source\synthDrivers\oneCore.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\synthDrivers\oneCore.py`  
**Current**: `F:\nvda\gh\alphajp\source\synthDrivers\oneCore.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\oneCore.py" "b/F:\\nvda\\gh\\alphajp\\source\\synthDrivers\\oneCore.py"
index 2d346ef6bf..0b00add00f 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\oneCore.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\synthDrivers\\oneCore.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2016-2024 Tyler Spivey, NV Access Limited, James Teh, Leonard de Ruijter
+# Copyright (C) 2016-2025 Tyler Spivey, NV Access Limited, James Teh, Leonard de Ruijter
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -18,6 +18,8 @@
 )
 from collections import OrderedDict
 import ctypes
+from ctypes.wintypes import HANDLE
+import comtypes
 import winreg
 import wave
 from synthDriverHandler import (
@@ -36,7 +38,6 @@
 from speech.types import SpeechSequence
 import speechXml
 import languageHandler
-import winVersion
 import NVDAHelper
 
 from speech.commands import (
@@ -194,7 +195,7 @@ class OneCoreSynthDriver(SynthDriver):
 	@classmethod
 	def check(cls):
 		# Only present this as an available synth if this is Windows 10.
-		return winVersion.getWinVer() >= winVersion.WIN10
+		return True
 
 	def _get_supportsProsodyOptions(self):
 		self.supportsProsodyOptions = self._dll.ocSpeech_supportsProsodyOptions()
@@ -218,6 +219,7 @@ def _get_supportedSettings(self):
 	def __init__(self):
 		super().__init__()
 		self._dll = NVDAHelper.getHelperLocalWin10Dll()
+		self._dll.ocSpeech_initialize.restype = HANDLE
 		self._dll.ocSpeech_getCurrentVoiceLanguage.restype = ctypes.c_wchar_p
 		# Set initial values for parameters that can't be queried when prosody is not supported.
 		# This initialises our cache for the value.
@@ -235,8 +237,9 @@ def __init__(self):
 
 		self._earlyExitCB = False
 		self._callbackInst = ocSpeech_Callback(self._callback)
-		self._ocSpeechToken: Optional[ctypes.POINTER] = self._dll.ocSpeech_initialize(self._callbackInst)
-		self._dll.ocSpeech_getVoices.restype = NVDAHelper.bstrReturn
+		self._ocSpeechToken = HANDLE()
+		self._ocSpeechToken.value = self._dll.ocSpeech_initialize(self._callbackInst)
+		self._dll.ocSpeech_getVoices.restype = comtypes.BSTR
 		self._dll.ocSpeech_getCurrentVoiceId.restype = ctypes.c_wchar_p
 		self._player = None
 		# Initialize state.
@@ -247,7 +250,6 @@ def __init__(self):
 		# Initialize the voice to a sane default
 		self.voice = self._getDefaultVoice()
 		self._consecutiveSpeechFailures = 0
-		self._isSpeaking = False
 
 	def _maybeInitPlayer(self, wav):
 		"""Initialize audio playback based on the wave header provided by the synthesizer.
@@ -313,7 +315,6 @@ def speak(self, speechSequence: SpeechSequence) -> None:
 		if self._player:
 			self._player.open()
 		self._queueSpeech(text)
-		self._isSpeaking = True
 
 	def _queueSpeech(self, item: str) -> None:
 		self._queuedSpeech.append(item)
@@ -406,7 +407,6 @@ def _processQueue(self):
 				log.debug("Calling idle on audio player")
 			self._player.idle()
 			synthDoneSpeaking.notify(synth=self)
-			self._isSpeaking = False
 		while self._queuedSpeech:
 			item = self._queuedSpeech.pop(0)
 			if isinstance(item, tuple):
@@ -519,8 +519,8 @@ def _isVoiceValid(self, ID: str) -> bool:
 		r"""
 		Checks that the given voice actually exists and is valid.
 		It checks the Registry, and also ensures that its data files actually exist on this machine.
-		@param ID: the ID of the requested voice.
-		@returns: True if the voice is valid, False otherwise.
+		:param ID: the ID of the requested voice.
+		:returns: True if the voice is valid, False otherwise.
 
 		OneCore keeps specific registry caches of OneCore for AT applications.
 		Installed copies of NVDA have a OneCore cache in:
@@ -627,9 +627,6 @@ def pause(self, switch):
 		if self._player:
 			self._player.pause(switch)
 
-	def isSpeaking(self):
-		return self._isSpeaking
-
 
 # Alias to allow look up by name "SynthDriver"
 SynthDriver = OneCoreSynthDriver

```