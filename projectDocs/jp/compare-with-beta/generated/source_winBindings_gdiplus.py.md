# Diff for: `source\winBindings\gdiplus.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\gdiplus.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\gdiplus.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\gdiplus.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\gdiplus.py"
index a9b5b81..cf38551 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\gdiplus.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\gdiplus.py"
@@ -6,7 +6,6 @@
 """Functions exported by gdiplus.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	Structure,
 	c_float,
 	c_int,
@@ -66,7 +65,7 @@ class GdiplusStartupOutput(Structure):
 	]
 
 
-GdiplusStartup = WINFUNCTYPE(None)(("GdiplusStartup", dll))
+GdiplusStartup = dll.GdiplusStartup
 """
 Initializes Windows GDI+.
 
@@ -81,7 +80,7 @@ class GdiplusStartupOutput(Structure):
 )
 
 
-GdiplusShutdown = WINFUNCTYPE(None)(("GdiplusShutdown", dll))
+GdiplusShutdown = dll.GdiplusShutdown
 """
 Cleans up resources used by Windows GDI+.
 
@@ -94,7 +93,7 @@ class GdiplusStartupOutput(Structure):
 )
 
 
-GdipCreateFromHDC = WINFUNCTYPE(None)(("GdipCreateFromHDC", dll))
+GdipCreateFromHDC = dll.GdipCreateFromHDC
 """
 Creates a Graphics object that is associated with a specified device context.
 
@@ -110,7 +109,7 @@ class GdiplusStartupOutput(Structure):
 )
 
 
-GdipCreatePen1 = WINFUNCTYPE(None)(("GdipCreatePen1", dll))
+GdipCreatePen1 = dll.GdipCreatePen1
 """
 Creates a Pen object that has specified color, width, and style.
 
@@ -126,7 +125,7 @@ class GdiplusStartupOutput(Structure):
 )
 
 
-GdipSetPenDashStyle = WINFUNCTYPE(None)(("GdipSetPenDashStyle", dll))
+GdipSetPenDashStyle = dll.GdipSetPenDashStyle
 """
 Sets the dash style of a Pen object.
 
@@ -140,7 +139,7 @@ class GdiplusStartupOutput(Structure):
 )
 
 
-GdipDrawLine = WINFUNCTYPE(None)(("GdipDrawLine", dll))
+GdipDrawLine = dll.GdipDrawLine
 """
 Draws a line.
 
@@ -158,7 +157,7 @@ class GdiplusStartupOutput(Structure):
 )
 
 
-GdipDrawRectangle = WINFUNCTYPE(None)(("GdipDrawRectangle", dll))
+GdipDrawRectangle = dll.GdipDrawRectangle
 """
 Draws a rectangle.
 
@@ -176,7 +175,7 @@ class GdiplusStartupOutput(Structure):
 )
 
 
-GdipDeletePen = WINFUNCTYPE(None)(("GdipDeletePen", dll))
+GdipDeletePen = dll.GdipDeletePen
 """
 Deletes a Pen object.
 
@@ -189,7 +188,7 @@ class GdiplusStartupOutput(Structure):
 )
 
 
-GdipDeleteGraphics = WINFUNCTYPE(None)(("GdipDeleteGraphics", dll))
+GdipDeleteGraphics = dll.GdipDeleteGraphics
 """
 Deletes a Graphics object.
 

```