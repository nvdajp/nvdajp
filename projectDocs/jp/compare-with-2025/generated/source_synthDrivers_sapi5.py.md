# Diff for: `source\synthDrivers\sapi5.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\synthDrivers\sapi5.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\synthDrivers\sapi5.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\sapi5.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDrivers\\sapi5.py"
index e9a0854..5430a89 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\synthDrivers\\sapi5.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDrivers\\sapi5.py"
@@ -18,13 +18,13 @@
 	memmove,
 	memset,
 	sizeof,
-	windll,
 )
 from enum import IntEnum
 import locale
 from collections import OrderedDict, deque
 import threading
 from typing import TYPE_CHECKING, Any, NamedTuple, Generator
+import winBindings.ole32
 import audioDucking
 from ctypes.wintypes import _LARGE_INTEGER, _ULARGE_INTEGER
 from comInterfaces.SpeechLib import (
@@ -66,9 +66,6 @@
 import NVDAState
 
 
-windll.ole32.CoTaskMemAlloc.restype = c_void_p
-
-
 class _SPAudioState(IntEnum):
 	# https://docs.microsoft.com/en-us/previous-versions/windows/desktop/ms720596(v=vs.85)
 	CLOSED = 0
@@ -173,7 +170,7 @@ def clear(self) -> None:
 		if self.elParamType in (_SPEventLParamType.TOKEN, _SPEventLParamType.OBJECT):
 			_Com_Release(cast(self.lParam, c_void_p))
 		elif self.elParamType in (_SPEventLParamType.POINTER, _SPEventLParamType.STRING):
-			windll.ole32.CoTaskMemFree(cast(self.lParam, c_void_p))
+			winBindings.ole32.CoTaskMemFree(cast(self.lParam, c_void_p))
 		memset(byref(self), 0, sizeof(self))
 
 	def __del__(self):
@@ -185,14 +182,14 @@ def copy(dst: SPEVENT, src: SPEVENT) -> None:
 		if not src.lParam:
 			return
 		if src.elParamType == _SPEventLParamType.POINTER:
-			dst.lParam = windll.ole32.CoTaskMemAlloc(src.wParam)
+			dst.lParam = winBindings.ole32.CoTaskMemAlloc(src.wParam)
 			if not dst.lParam:
 				raise COMError(hresult.E_OUTOFMEMORY, "CoTaskMemAlloc failed", (None, None, None, None, None))
 			memmove(dst.lParam, src.lParam, src.wParam)
 		elif src.elParamType == _SPEventLParamType.STRING:
 			strbuf = create_unicode_buffer(cast(src.lParam, c_wchar_p).value)
 			bufsize = sizeof(strbuf)
-			dst.lParam = windll.ole32.CoTaskMemAlloc(bufsize)
+			dst.lParam = winBindings.ole32.CoTaskMemAlloc(bufsize)
 			if not dst.lParam:
 				raise COMError(hresult.E_OUTOFMEMORY, "CoTaskMemAlloc failed", (None, None, None, None, None))
 			memmove(dst.lParam, byref(strbuf), bufsize)
@@ -333,7 +330,7 @@ def ISpStreamFormat_GetFormat(self, pguidFormatId: _Pointer[GUID]) -> _Pointer[W
 		"""
 		# pguidFormatId is actually an out parameter
 		pguidFormatId.contents = _SPDFID_WaveFormatEx
-		pwfx = cast(windll.ole32.CoTaskMemAlloc(sizeof(WAVEFORMATEX)), POINTER(WAVEFORMATEX))
+		pwfx = cast(winBindings.ole32.CoTaskMemAlloc(sizeof(WAVEFORMATEX)), POINTER(WAVEFORMATEX))
 		if not pwfx:
 			raise COMError(hresult.E_OUTOFMEMORY, "CoTaskMemAlloc failed", (None, None, None, None, None))
 		memmove(pwfx, byref(self.waveFormat), sizeof(WAVEFORMATEX))
@@ -380,7 +377,7 @@ def ISpAudio_GetDefaultFormat(self) -> tuple[GUID, _Pointer[WAVEFORMATEX]]:
 
 		:returns: A tuple of a GUID, which should always be SPDFID_WaveFormatEx,
 			and a pointer to a WAVEFORMATEX structure, allocated by CoTaskMemAlloc."""
-		pwfx = cast(windll.ole32.CoTaskMemAlloc(sizeof(WAVEFORMATEX)), POINTER(WAVEFORMATEX))
+		pwfx = cast(winBindings.ole32.CoTaskMemAlloc(sizeof(WAVEFORMATEX)), POINTER(WAVEFORMATEX))
 		if not pwfx:
 			raise COMError(hresult.E_OUTOFMEMORY, "CoTaskMemAlloc failed", (None, None, None, None, None))
 		self._writeDefaultFormat(pwfx.contents)

```