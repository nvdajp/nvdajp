# Diff for: `source\nvwave.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\nvwave.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\nvwave.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\nvwave.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\nvwave.py"
index 637af93..15f0bde 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\nvwave.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\nvwave.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2007-2024 NV Access Limited, Aleksey Sadovoy, Cyrille Bougot, Peter Vágner, Babbage B.V.,
+# Copyright (C) 2007-2025 NV Access Limited, Aleksey Sadovoy, Cyrille Bougot, Peter Vágner, Babbage B.V.,
 # Leonard de Ruijter, James Teh
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
@@ -13,16 +13,12 @@
 )
 from enum import Enum, auto
 from ctypes import (
-	Structure,
 	c_uint,
 	byref,
 	c_void_p,
 	CFUNCTYPE,
 	c_float,
-)
-from ctypes.wintypes import (
-	WORD,
-	DWORD,
+	string_at,
 )
 from comtypes import HRESULT
 from comtypes.hresult import E_INVALIDARG
@@ -41,7 +37,16 @@
 from speech import SpeechSequence
 from speech.commands import BreakCommand
 from synthDriverHandler import pre_synthSpeak
-
+from utils import _deprecate
+from winBindings.mmeapi import WAVEFORMATEX as _WAVEFORMATEX
+
+__getattr__ = _deprecate.handleDeprecations(
+	_deprecate.MovedSymbol(
+		"WAVEFORMATEX",
+		"winBindings.mmeapi",
+	),
+)
+"""Module __getattr__ to handle backward compatibility."""
 
 __all__ = (
 	"WavePlayer",
@@ -60,18 +65,6 @@
 """
 
 
-class WAVEFORMATEX(Structure):
-	_fields_ = [
-		("wFormatTag", WORD),
-		("nChannels", WORD),
-		("nSamplesPerSec", DWORD),
-		("nAvgBytesPerSec", DWORD),
-		("nBlockAlign", WORD),
-		("wBitsPerSample", WORD),
-		("cbSize", WORD),
-	]
-
-
 WAVE_FORMAT_PCM = 1
 
 
@@ -232,7 +225,7 @@ def __init__(
 		self.channels = channels
 		self.samplesPerSec = samplesPerSec
 		self.bitsPerSample = bitsPerSample
-		format = self._format = WAVEFORMATEX()
+		format = self._format = _WAVEFORMATEX()
 		format.wFormatTag = WAVE_FORMAT_PCM
 		format.nChannels = channels
 		format.nSamplesPerSec = samplesPerSec
@@ -346,6 +339,8 @@ def feed(
 		# turn off trimming temporarily.
 		if self._purpose is AudioPurpose.SPEECH and self._isLeadingSilenceInserted:
 			self.startTrimmingLeadingSilence(False)
+		if not isinstance(data, bytes):
+			data = string_at(data, size)
 		try:
 			NVDAHelper.localLib.wasPlay_feed(
 				self._player,

```