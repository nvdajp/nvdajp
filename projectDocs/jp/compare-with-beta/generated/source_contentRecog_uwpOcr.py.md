# Diff for: `source\contentRecog\uwpOcr.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\contentRecog\uwpOcr.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\contentRecog\uwpOcr.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\contentRecog\\uwpOcr.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\contentRecog\\uwpOcr.py"
index 0610d5f..76b1f16 100644
--- "a/F:\\nvda\\gh\\beta\\source\\contentRecog\\uwpOcr.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\contentRecog\\uwpOcr.py"
@@ -1,16 +1,11 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2017-2025 NV Access Limited, Cary-rowen
+# Copyright (C) 2017-2021 NV Access Limited
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
 """Recognition of text using the UWP OCR engine included in Windows 10 and later."""
 
-from ctypes import (
-	cast,
-	POINTER,
-)
 import json
-from winBindings.gdi32 import RGBQUAD
 import NVDAHelper
 from NVDAHelper.localWin10 import (
 	uwpOcr_getLanguages,
@@ -91,10 +86,6 @@ def _get_allowAutoRefresh(cls) -> bool:
 	def _get_autoRefreshInterval(cls) -> int:
 		return config.conf["uwpOcr"]["autoRefreshInterval"]
 
-	@classmethod
-	def _get_autoSayAllOnResult(cls) -> bool:
-		return config.conf["uwpOcr"]["autoSayAllOnResult"]
-
 	def getResizeFactor(self, width, height):
 		# UWP OCR performs poorly with small images, so increase their size.
 		if width < 100 or height < 100:
@@ -133,15 +124,7 @@ def callback(result):
 		if not self._handle:
 			onResult(RuntimeError("UWP OCR initialization failed"))
 			return
-		uwpOcr_recognize(
-			self._handle,
-			# pixels, as fetched from screenBitmap.captureImage is a 2d array of RGBQUAD values.
-			# However uwpOcr_recognize expects a 1d array (pointer).
-			# These are identical in memory, so we can just cast.
-			cast(pixels, POINTER(RGBQUAD)),
-			imgInfo.recogWidth,
-			imgInfo.recogHeight,
-		)
+		uwpOcr_recognize(self._handle, pixels, imgInfo.recogWidth, imgInfo.recogHeight)
 
 	def cancel(self):
 		self._onResult = None

```