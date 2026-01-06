# Diff for: `source\winGDI.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\winGDI.py`  
**Current**: `F:\nvda\gh\alphajp\source\winGDI.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\winGDI.py" "b/F:\\nvda\\gh\\alphajp\\source\\winGDI.py"
index ddb3d0a13e..8c7e51bcfd 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\winGDI.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\winGDI.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2011-2022 NV Access Limited
+# Copyright (C) 2011-2025 NV Access Limited
 # This file is covered by the GNU General Public License.
 # See the file COPYING for more details.
 
@@ -7,45 +7,56 @@
 When working on this file, consider moving to winAPI.
 """
 
-from ctypes import windll, Structure, c_ubyte, c_uint32, c_void_p, c_int, c_float, POINTER, byref, c_ulong
-from ctypes.wintypes import LONG, DWORD, WORD, BOOL
+from ctypes import (
+	POINTER,
+	byref,
+)
 from contextlib import contextmanager
 
-user32 = windll.user32
-gdi32 = windll.gdi32
-gdiplus = windll.gdiplus
-
-
-class RGBQUAD(Structure):
-	_fields_ = [
-		("rgbBlue", c_ubyte),
-		("rgbGreen", c_ubyte),
-		("rgbRed", c_ubyte),
-		("rgbReserved", c_ubyte),
-	]
-
-
-class BITMAPINFOHEADER(Structure):
-	_fields_ = [
-		("biSize", DWORD),
-		("biWidth", LONG),
-		("biHeight", LONG),
-		("biPlanes", WORD),
-		("biBitCount", WORD),
-		("biCompression", WORD),
-		("biSizeImage", DWORD),
-		("biXPelsPerMeter", LONG),
-		("biYPelsPerMeter", LONG),
-		("biClrUsed", DWORD),
-		("biClrImportant", DWORD),
-	]
-
-
-class BITMAPINFO(Structure):
-	_fields_ = [
-		("bmiHeader", BITMAPINFOHEADER),
-		("bmiColors", (RGBQUAD * 1)),
-	]
+from utils import _deprecate
+from winBindings.gdiplus import (
+	ULONG_PTR,
+	GdipCreateFromHDC,
+	GdipCreatePen1,
+	GdipDeleteGraphics,
+	GdipDeletePen,
+	GdipDrawRectangle,
+	GdiplusShutdown,
+	GdiplusStartup,
+	GdipSetPenDashStyle,
+	GpGraphics,
+	GpPen,
+	# Aliased as these used to be part of this module's public API
+	# and without the alias we can't issue a deprecation warning.
+	GdiplusStartupInput as _GdiplusStartupInput,
+	GdiplusStartupOutput as _GdiplusStartupOutput,
+)
+
+__getattr__ = _deprecate.handleDeprecations(
+	_deprecate.MovedSymbol("gdiplus", "winBindings.gdiplus", "dll"),
+	_deprecate.MovedSymbol(
+		"GdiplusStartupInput",
+		"winBindings.gdiplus",
+	),
+	_deprecate.MovedSymbol(
+		"GdiplusStartupOutput",
+		"winBindings.gdiplus",
+	),
+	_deprecate.MovedSymbol(
+		"RGBQUAD",
+		"winBindings.gdi32",
+	),
+	_deprecate.MovedSymbol(
+		"BITMAPINFOHEADER",
+		"winBindings.gdi32",
+	),
+	_deprecate.MovedSymbol(
+		"BITMAPINFO",
+		"winBindings.gdi32",
+	),
+	_deprecate.MovedSymbol("gdi32", "winBindings.gdi32", "dll"),
+	_deprecate.MovedSymbol("user32", "winBindings.user32", "dll"),
+)
 
 
 BI_RGB = 0
@@ -53,43 +64,6 @@ class BITMAPINFO(Structure):
 DIB_RGB_COLORS = 0
 
 
-class GdiplusStartupInput(Structure):
-	_fields_ = [
-		("GdiplusVersion", c_uint32),
-		("DebugEventCallback", c_void_p),
-		("SuppressBackgroundThread", BOOL),
-		("SuppressExternalCodecs", BOOL),
-	]
-
-
-class GdiplusStartupOutput(Structure):
-	_fields = [
-		("NotificationHookProc", c_void_p),
-		("NotificationUnhookProc", c_void_p),
-	]
-
-
-gdiplus.GdipCreateFromHDC.argtypes = [c_int, POINTER(c_void_p)]
-gdiplus.GdipCreateFromHDC.restype = c_int
-
-gdiplus.GdipCreatePen1.argtypes = [c_int, c_float, c_int, POINTER(c_void_p)]
-gdiplus.GdipCreatePen1.restype = c_int
-
-gdiplus.GdipSetPenDashStyle.argtypes = [c_void_p, c_int]
-gdiplus.GdipSetPenDashStyle.restype = c_int
-
-gdiplus.GdipDrawLine.argtypes = [c_void_p, c_void_p, c_float, c_float, c_float, c_float]
-gdiplus.GdipDrawLine.restype = c_int
-
-gdiplus.GdipDrawRectangle.argtypes = [c_void_p, c_void_p, c_float, c_float, c_float, c_float]
-gdiplus.GdipDrawRectangle.restype = c_int
-
-gdiplus.GdipDeletePen.argtypes = [c_void_p]
-gdiplus.GdipDeletePen.restype = c_int
-
-gdiplus.GdipDeleteGraphics.argtypes = [c_void_p]
-gdiplus.GdipDeleteGraphics.restype = c_int
-
 # GDI+ dash style enumeration
 DashStyleSolid = 0  # Specifies a solid line.
 DashStyleDash = 1  # Specifies a dashed line.
@@ -108,26 +82,26 @@ def gdiPlusInitialize():
 	global gdipToken
 	if gdipToken:
 		return  # Already initialized
-	gdipToken = c_ulong()
-	startupInput = GdiplusStartupInput()
+	gdipToken = ULONG_PTR()
+	startupInput = _GdiplusStartupInput()
 	startupInput.GdiplusVersion = 1
-	startupOutput = GdiplusStartupOutput()
-	gdiplus.GdiplusStartup(byref(gdipToken), byref(startupInput), byref(startupOutput))
+	startupOutput = _GdiplusStartupOutput()
+	GdiplusStartup(byref(gdipToken), byref(startupInput), byref(startupOutput))
 
 
 def gdiPlusTerminate():
 	global gdipToken
 	if not gdipToken:
 		return  # Not initialized
-	gdiplus.GdiplusShutdown(gdipToken)
+	GdiplusShutdown(gdipToken)
 	gdipToken = None
 
 
 @contextmanager
 def GDIPlusGraphicsContext(hdc):
 	"""Creates a GDI+ graphics context from a device context handle."""
-	gpGraphics = c_void_p()
-	gpStatus = gdiplus.GdipCreateFromHDC(hdc, byref(gpGraphics))
+	gpGraphics = POINTER(GpGraphics)()
+	gpStatus = GdipCreateFromHDC(hdc, byref(gpGraphics))
 	if gpStatus:
 		# See https://docs.microsoft.com/en-us/windows/desktop/api/Gdiplustypes/ne-gdiplustypes-status
 		# for a list of applicable status codes
@@ -135,7 +109,7 @@ def GDIPlusGraphicsContext(hdc):
 	try:
 		yield gpGraphics
 	finally:
-		gdiplus.GdipDeleteGraphics(gpGraphics)
+		GdipDeleteGraphics(gpGraphics)
 
 
 @contextmanager
@@ -150,21 +124,21 @@ def GDIPlusPen(color, width, dashStyle=DashStyleSolid):
 		Defaults to C{DashStyleSolid}, which draws solid lines.
 	@type dashStyle: int
 	"""
-	gpPen = c_void_p()
-	gpStatus = gdiplus.GdipCreatePen1(color, width, UnitPixel, byref(gpPen))
+	gpPen = POINTER(GpPen)()
+	gpStatus = GdipCreatePen1(color, width, UnitPixel, byref(gpPen))
 	if gpStatus:
 		raise RuntimeError("GdipCreatePen1 failed with status code %d" % gpStatus)
-	gpStatus = gdiplus.GdipSetPenDashStyle(gpPen, dashStyle)
+	gpStatus = GdipSetPenDashStyle(gpPen, dashStyle)
 	if gpStatus:
 		raise RuntimeError("GdipSetPenDashStyle failed with status code %d" % gpStatus)
 	try:
 		yield gpPen
 	finally:
-		gdiplus.GdipDeletePen(gpPen)
+		GdipDeletePen(gpPen)
 
 
 def gdiPlusDrawRectangle(gpGraphics, gpPen, left, top, width, height):
-	gpStatus = gdiplus.GdipDrawRectangle(
+	gpStatus = GdipDrawRectangle(
 		gpGraphics,
 		gpPen,
 		float(left),

```