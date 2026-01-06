# Diff for: `source\contentRecog\uwpOcr.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\contentRecog\uwpOcr.py`  
**Current**: `F:\nvda\gh\alphajp\source\contentRecog\uwpOcr.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\contentRecog\\uwpOcr.py" "b/F:\\nvda\\gh\\alphajp\\source\\contentRecog\\uwpOcr.py"
index 45f2e010d4..76b1f16ecb 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\contentRecog\\uwpOcr.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\contentRecog\\uwpOcr.py"
@@ -5,14 +5,23 @@
 
 """Recognition of text using the UWP OCR engine included in Windows 10 and later."""
 
-import ctypes
 import json
 import NVDAHelper
+from NVDAHelper.localWin10 import (
+	uwpOcr_getLanguages,
+	uwpOcr_initialize,
+	uwpOcr_recognize,
+	uwpOcr_terminate,
+	uwpOcr_Callback as _uwpOcr_Callback,
+)
 from . import ContentRecognizer, LinesWordsResult
 import config
 import languageHandler
+from utils import _deprecate
 
-uwpOcr_Callback = ctypes.CFUNCTYPE(None, ctypes.c_wchar_p)
+__getattr__ = _deprecate.handleDeprecations(
+	_deprecate.MovedSymbol("uwpOcr_Callback", "NVDAHelper.localWin10"),
+)
 
 
 def getLanguages():
@@ -22,9 +31,7 @@ def getLanguages():
 		for use as NVDA language codes.
 	@rtype: list of str
 	"""
-	dll = NVDAHelper.getHelperLocalWin10Dll()
-	dll.uwpOcr_getLanguages.restype = NVDAHelper.bstrReturn
-	langs = dll.uwpOcr_getLanguages()
+	langs = uwpOcr_getLanguages()
 	return langs.split(";")[:-1]
 
 
@@ -99,7 +106,7 @@ def __init__(self, language=None):
 	def recognize(self, pixels, imgInfo, onResult):
 		self._onResult = onResult
 
-		@uwpOcr_Callback
+		@_uwpOcr_Callback
 		def callback(result):
 			# If self._onResult is None, recognition was cancelled.
 			if self._onResult:
@@ -108,16 +115,16 @@ def callback(result):
 					self._onResult(LinesWordsResult(data, imgInfo))
 				else:
 					self._onResult(RuntimeError("UWP OCR failed"))
-			self._dll.uwpOcr_terminate(self._handle)
+			uwpOcr_terminate(self._handle)
 			self._callback = None
 			self._handle = None
 
 		self._callback = callback
-		self._handle = self._dll.uwpOcr_initialize(self.language, callback)
+		self._handle = uwpOcr_initialize(self.language, callback)
 		if not self._handle:
 			onResult(RuntimeError("UWP OCR initialization failed"))
 			return
-		self._dll.uwpOcr_recognize(self._handle, pixels, imgInfo.recogWidth, imgInfo.recogHeight)
+		uwpOcr_recognize(self._handle, pixels, imgInfo.recogWidth, imgInfo.recogHeight)
 
 	def cancel(self):
 		self._onResult = None

```