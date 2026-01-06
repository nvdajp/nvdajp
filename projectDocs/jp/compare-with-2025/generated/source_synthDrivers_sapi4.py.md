# Diff for: `source\synthDrivers\sapi4.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\synthDrivers\sapi4.py`  
**Current**: `F:\nvda\gh\alphajp\source\synthDrivers\sapi4.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\sapi4.py" "b/F:\\nvda\\gh\\alphajp\\source\\synthDrivers\\sapi4.py"
index 9c3a63e716..5bb68ae33e 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\sapi4.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\synthDrivers\\sapi4.py"
@@ -12,6 +12,10 @@
 import threading
 import time
 import winreg
+import winBindings.ole32
+from winBindings import user32
+import winBindings.winmm
+from winBindings.mmeapi import WAVEFORMATEX
 from comtypes import CoCreateInstance, CoInitialize, COMObject, COMError, GUID, hresult, ReturnHRESULT
 from ctypes import (
 	addressof,
@@ -26,7 +30,6 @@
 	memmove,
 	string_at,
 	sizeof,
-	windll,
 )
 from ctypes.wintypes import BOOL, DWORD, FILETIME, HANDLE, MSG, WORD
 from typing import TYPE_CHECKING, Callable, NamedTuple, Optional
@@ -86,9 +89,6 @@
 from speech.types import SpeechSequence
 
 
-windll.ole32.CoTaskMemAlloc.restype = c_void_p
-
-
 class SynthDriverBufSink(COMObject):
 	_com_interfaces_ = [ITTSBufNotifySink]
 
@@ -113,11 +113,6 @@ def ITTSBufNotifySink_BookMark(self, this: int, qTimeStamp: int, dwMarkNum: int)
 			if synth._bookmarks.popleft() == dwMarkNum:
 				break
 
-	def ITTSBufNotifySink_TextDataDone(self, this, qTimeStamp, dwMarkNum):
-		synth = self.synthRef()
-		if synth and hasattr(synth, "setSpeaking"):
-			synth.setSpeaking(False)
-
 	def IUnknown_Release(self, this: int, *args, **kwargs):
 		if not self._allowDelete and self._refcnt.value == 1:
 			log.debugWarning("ITTSBufNotifySink::Release called too many times by engine")
@@ -217,15 +212,15 @@ def run(self):
 		msg = MSG()
 		# Force the message queue to be created first
 		PM_NOREMOVE = 0
-		windll.user32.PeekMessageW(byref(msg), None, 0, 0, PM_NOREMOVE)
+		user32.PeekMessage(byref(msg), None, 0, 0, PM_NOREMOVE)
 		CoInitialize()
 		self._ready.set()
 		# Run a message loop, as it's required by SAPI 4.
 		# When queueing a new task, post a message to this thread to wake it up.
 		# When done, post WM_QUIT to this thread.
-		while windll.user32.GetMessageW(byref(msg), None, 0, 0):
-			windll.user32.TranslateMessage(byref(msg))
-			windll.user32.DispatchMessageW(byref(msg))
+		while user32.GetMessage(byref(msg), None, 0, 0):
+			user32.TranslateMessage(byref(msg))
+			user32.DispatchMessage(byref(msg))
 			# Process queued tasks outside window procedures
 			# to avoid COM error RPC_E_CANTCALLOUT_INEXTERNALCALL
 			# (-2147418107, 0x80010005).
@@ -245,7 +240,7 @@ def run(self):
 
 	def stop(self):
 		WM_QUIT = 18
-		windll.user32.PostThreadMessageW(self.native_id, WM_QUIT, 0, 0)
+		user32.PostThreadMessage(self.native_id, WM_QUIT, 0, 0)
 		self.join()
 
 	def submit(self, func: Callable, *args, **kwargs) -> _ComThreadTask:
@@ -255,7 +250,7 @@ def submit(self, func: Callable, *args, **kwargs) -> _ComThreadTask:
 		task = _ComThreadTask(func, *args, **kwargs)
 		self._tasks.put(task)
 		# post a message to wake up the thread
-		windll.user32.PostThreadMessageW(self.native_id, 0, 0, 0)
+		user32.PostThreadMessage(self.native_id, 0, 0, 0)
 		return task
 
 	def invoke(self, func: Callable, *args, **kwargs):
@@ -342,7 +337,7 @@ def __init__(self, comThread: _ComThread):
 		self._allowDelete = False
 		self._notifySink: LP_IAudioDestNotifySink | None = None
 		self._deviceState = _AudioState.INVALID
-		self._waveFormat: nvwave.WAVEFORMATEX | None = None
+		self._waveFormat: WAVEFORMATEX | None = None
 		self._player: nvwave.WavePlayer | None = None
 		self._writtenBytes = 0
 		self._playedBytes = 0
@@ -581,8 +576,8 @@ def IAudio_WaveFormatGet(self) -> SDATA:
 			Should be freed by the caller using CoTaskMemFree."""
 		if self._deviceState == _AudioState.INVALID:
 			raise ReturnHRESULT(AudioError.NEED_WAVE_FORMAT, None)
-		size = sizeof(nvwave.WAVEFORMATEX)
-		ptr = windll.ole32.CoTaskMemAlloc(size)
+		size = sizeof(WAVEFORMATEX)
+		ptr = winBindings.ole32.CoTaskMemAlloc(size)
 		if not ptr:
 			raise COMError(hresult.E_OUTOFMEMORY, "CoTaskMemAlloc failed", (None, None, None, None, None))
 		memmove(ptr, addressof(self._waveFormat), size)
@@ -594,7 +589,7 @@ def IAudio_WaveFormatSet(self, dWFEX: SDATA) -> None:
 		size = 18  # SAPI4 uses 18 bytes without the final padding
 		if not dWFEX.pData or dWFEX.dwSize < size:
 			raise ReturnHRESULT(hresult.E_INVALIDARG, None)
-		wfx = nvwave.WAVEFORMATEX()
+		wfx = WAVEFORMATEX()
 		memmove(addressof(wfx), dWFEX.pData, size)
 		if self._deviceState != _AudioState.INVALID:
 			# Setting wave format more than once is not allowed.
@@ -923,8 +918,6 @@ def __init__(self):
 		self._volume = 100
 		self._paused = False
 		self.voice = str(self._enginesList[0].gModeID)
-		self._rate = None
-		self._isSpeaking = False
 
 	def terminate(self):
 		self._bufSink._allowDelete = True
@@ -960,13 +953,12 @@ def speak(self, speechSequence: SpeechSequence):
 		lastHandledIndexInSequence = 0
 		for item in speechSequence:
 			if isinstance(item, str):
-				item = item.replace("\u2022", "").replace("\uf0b7", "")  # nvdajp (bullet)
 				textList.append(item.replace("\\", "\\\\"))
 			elif isinstance(item, IndexCommand):
 				textList.append("\\mrk=%d\\" % item.index)
 				bookmarks.append(item.index)
 				lastHandledIndexInSequence = item.index
-			elif False and isinstance(item, CharacterModeCommand):  # nvdajp
+			elif isinstance(item, CharacterModeCommand):
 				textList.append("\\RmS=1\\" if item.state else "\\RmS=0\\")
 				charMode = item.state
 			elif isinstance(item, BreakCommand):
@@ -982,7 +974,8 @@ def speak(self, speechSequence: SpeechSequence):
 				# If you specify a value greater than 65535, the engine assumes that you want to set the
 				# left and right channels separately and converts the value to a double word,
 				# using the low word for the left channel and the high word for the right channel.
-				val |= val << 16
+				# However, some voices don't handle values greater than 65535 properly in Vol tags,
+				# so here only 0~65535 are used.
 				textList.append(f"\\Vol={val}\\")
 			elif isinstance(item, SpeechCommand):
 				log.debugWarning("Unsupported speech command: %s" % item)
@@ -1008,12 +1001,10 @@ def speak(self, speechSequence: SpeechSequence):
 			self._bufSinkPtr,
 			ITTSBufNotifySink._iid_,
 		)
-		self._isSpeaking = True
 
 	def cancel(self):
 		if isDebugForSynthDriver():
 			log.debug("SAPI4: Cancelling")
-		self._isSpeaking = True
 		try:
 			# cancel all pending bookmarks
 			self._bookmarkLists.clear()
@@ -1029,7 +1020,6 @@ def cancel(self):
 			log.debugWarning("Error cancelling speech", exc_info=True)
 		finally:
 			self._finalIndex = None
-		self.lastIndex = None
 
 	def pause(self, switch: bool):
 		if isDebugForSynthDriver():
@@ -1046,12 +1036,6 @@ def pause(self, switch: bool):
 			self._ttsCentral.AudioResume()
 		self._paused = switch
 
-	def setSpeaking(self, switch):
-		self._isSpeaking = switch
-
-	def isSpeaking(self):
-		return self._isSpeaking
-
 	def removeSetting(self, name):
 		# Putting it here because currently no other synths make use of it. OrderedDict, where you are?
 		for i, s in enumerate(self.supportedSettings):
@@ -1197,17 +1181,12 @@ def _getAvailableVoices(self):
 		return voices
 
 	def _get_rate(self) -> int:
-		if self._rate is not None:
-			return self._rate
 		val = DWORD()
 		self._ttsAttrs.SpeedGet(byref(val))
-		ret = self._paramToPercent(val.value, self._minRate, self._maxRate)
-		return min(100, ret)
+		return self._paramToPercent(val.value, self._minRate, self._maxRate)
 
 	def _set_rate(self, val: int):
-		self._rate = val
 		val = self._percentToParam(val, self._minRate, self._maxRate)
-		val = min(self._maxRate, val)
 		self._ttsAttrs.SpeedSet(val)
 		self._rateDelta = val - self._defaultRate
 
@@ -1248,9 +1227,8 @@ def _mmDeviceEndpointIdToWaveOutId(targetEndpointId: str) -> int:
 		currEndpointId = create_string_buffer(targetEndpointIdByteCount)
 		currEndpointIdByteCount = DWORD()
 		# Defined in mmeapi.h
-		winmm = windll.winmm
-		waveOutMessage = winmm.waveOutMessage
-		waveOutGetNumDevs = winmm.waveOutGetNumDevs
+		waveOutMessage = winBindings.winmm.waveOutMessage
+		waveOutGetNumDevs = winBindings.winmm.waveOutGetNumDevs
 		for devID in range(waveOutGetNumDevs()):
 			# Get the length of this device's endpoint ID string.
 			mmr = waveOutMessage(

```