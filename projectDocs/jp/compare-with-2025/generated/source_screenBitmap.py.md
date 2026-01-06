# Diff for: `source\screenBitmap.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\screenBitmap.py`  
**Current**: `F:\nvda\gh\alphajp\source\screenBitmap.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\screenBitmap.py" "b/F:\\nvda\\gh\\alphajp\\source\\screenBitmap.py"
index b2da0cbff0..54ad64b0e6 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\screenBitmap.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\screenBitmap.py"
@@ -1,16 +1,15 @@
-# screenBitmap.py
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2011-2017 NV Access Limited
-# This file is covered by the GNU General Public License.
-# See the file COPYING for more details.
+# Copyright (C) 2011-2025 NV Access Limited
+# This file may be used under the terms of the GNU General Public License, version 2 or later, as modified by the NVDA license.
+# For full terms and any additional permissions, see the NVDA license file: https://github.com/nvaccess/nvda/blob/master/copying.txt
 
 """Functionality to capture and work with bitmaps of the screen."""
 
 import ctypes
 import winGDI
-
-user32 = ctypes.windll.user32
-gdi32 = ctypes.windll.gdi32
+import winBindings.gdi32
+from winBindings import user32 as _user32
+from utils import _deprecate
 
 
 class ScreenBitmap(object):
@@ -24,14 +23,14 @@ def __init__(self, width, height):
 		self.width = width
 		self.height = height
 		# Fetch the device context for the screen
-		self._screenDC = user32.GetDC(0)
+		self._screenDC = _user32.GetDC(0)
 		# Create a memory device context with which we can copy screen content to on request.
-		self._memDC = gdi32.CreateCompatibleDC(self._screenDC)
+		self._memDC = winBindings.gdi32.CreateCompatibleDC(self._screenDC)
 		# Create a new bitmap of the chosen size, and set this as the memory device context's bitmap, so that what is drawn is captured.
-		self._memBitmap = gdi32.CreateCompatibleBitmap(self._screenDC, width, height)
-		self._oldBitmap = gdi32.SelectObject(self._memDC, self._memBitmap)
+		self._memBitmap = winBindings.gdi32.CreateCompatibleBitmap(self._screenDC, width, height)
+		self._oldBitmap = winBindings.gdi32.SelectObject(self._memDC, self._memBitmap)
 		# We always want standard RGB data
-		bmInfo = winGDI.BITMAPINFO()
+		bmInfo = winBindings.gdi32.BITMAPINFO()
 		bmInfo.bmiHeader.biSize = ctypes.sizeof(bmInfo)
 		bmInfo.bmiHeader.biWidth = width
 		bmInfo.bmiHeader.biHeight = height * -1
@@ -41,17 +40,17 @@ def __init__(self, width, height):
 		self._bmInfo = bmInfo
 
 	def __del__(self):
-		gdi32.SelectObject(self._memDC, self._oldBitmap)
-		gdi32.DeleteObject(self._memBitmap)
-		gdi32.DeleteDC(self._memDC)
-		user32.ReleaseDC(0, self._screenDC)
+		winBindings.gdi32.SelectObject(self._memDC, self._oldBitmap)
+		winBindings.gdi32.DeleteObject(self._memBitmap)
+		winBindings.gdi32.DeleteDC(self._memDC)
+		_user32.ReleaseDC(0, self._screenDC)
 
 	def captureImage(self, x, y, w, h):
 		"""
 		Captures the part of the screen starting at x,y and extends by w (width) and h (height), and stretches/shrinks it to fit in to the object's bitmap size.
 		"""
 		# Copy the requested content from the screen in to our memory device context, stretching/shrinking its size to fit.
-		gdi32.StretchBlt(
+		winBindings.gdi32.StretchBlt(
 			self._memDC,
 			0,
 			0,
@@ -65,8 +64,8 @@ def captureImage(self, x, y, w, h):
 			winGDI.SRCCOPY,
 		)
 		# Fetch the pixels from our memory bitmap and store them in a buffer to be returned
-		buffer = (winGDI.RGBQUAD * self.width * self.height)()
-		gdi32.GetDIBits(
+		buffer = (winBindings.gdi32.RGBQUAD * (self.width * self.height))()
+		winBindings.gdi32.GetDIBits(
 			self._memDC,
 			self._memBitmap,
 			0,
@@ -81,3 +80,9 @@ def captureImage(self, x, y, w, h):
 def rgbPixelBrightness(p):
 	"""Converts a RGBQUAD pixel in to  one grey-scale brightness value."""
 	return int((0.3 * p.rgbBlue) + (0.59 * p.rgbGreen) + (0.11 * p.rgbRed))
+
+
+__getattr__ = _deprecate.handleDeprecations(
+	_deprecate.MovedSymbol("gdi32", "winBindings.gdi32", "dll"),
+	_deprecate.MovedSymbol("user32", "winBindings.user32", "dll"),
+)

```