# Diff for: `source\winBindings\gdi32.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winBindings\gdi32.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winBindings\gdi32.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winBindings\\gdi32.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\gdi32.py"
index 06c4047..40e99bd 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winBindings\\gdi32.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winBindings\\gdi32.py"
@@ -6,7 +6,6 @@
 """Functions exported by gdi32.dll, and supporting data structures and enumerations."""
 
 from ctypes import (
-	WINFUNCTYPE,
 	Structure,
 	c_ubyte,
 	c_int,
@@ -33,7 +32,7 @@
 dll = windll.gdi32
 
 
-GetDeviceCaps = WINFUNCTYPE(None)(("GetDeviceCaps", dll))
+GetDeviceCaps = dll.GetDeviceCaps
 """
 Retrieves device-specific information for the specified device.
 
@@ -47,7 +46,7 @@
 )
 
 
-CreateCompatibleDC = WINFUNCTYPE(None)(("CreateCompatibleDC", dll))
+CreateCompatibleDC = dll.CreateCompatibleDC
 """
 Creates a memory device context (DC) compatible with the specified device.
 
@@ -60,7 +59,7 @@
 )
 
 
-CreateCompatibleBitmap = WINFUNCTYPE(None)(("CreateCompatibleBitmap", dll))
+CreateCompatibleBitmap = dll.CreateCompatibleBitmap
 """
 Creates a bitmap compatible with the device that is associated with the specified device context.
 
@@ -75,7 +74,7 @@
 )
 
 
-SelectObject = WINFUNCTYPE(None)(("SelectObject", dll))
+SelectObject = dll.SelectObject
 """
 Selects an object into the specified device context (DC).
 
@@ -89,7 +88,7 @@
 )
 
 
-DeleteObject = WINFUNCTYPE(None)(("DeleteObject", dll))
+DeleteObject = dll.DeleteObject
 """
 Deletes a logical pen, brush, font, bitmap, region, or palette, freeing all system resources associated with the object.
 
@@ -102,7 +101,7 @@
 )
 
 
-DeleteDC = WINFUNCTYPE(None)(("DeleteDC", dll))
+DeleteDC = dll.DeleteDC
 """
 Deletes the specified device context (DC).
 
@@ -115,7 +114,7 @@
 )
 
 
-StretchBlt = WINFUNCTYPE(None)(("StretchBlt", dll))
+StretchBlt = dll.StretchBlt
 """
 Copies a bitmap from a source rectangle into a destination rectangle, stretching or compressing the bitmap to fit the dimensions of the destination rectangle.
 
@@ -191,7 +190,7 @@ class BITMAPINFO(Structure):
 	]
 
 
-GetDIBits = WINFUNCTYPE(None)(("GetDIBits", dll))
+GetDIBits = dll.GetDIBits
 """
 Retrieves the bits of the specified compatible bitmap and copies them into a buffer as a DIB using the specified format.
 
@@ -212,7 +211,7 @@ class BITMAPINFO(Structure):
 )
 
 
-CreateSolidBrush = WINFUNCTYPE(None)(("CreateSolidBrush", dll))
+CreateSolidBrush = dll.CreateSolidBrush
 """
 Creates a logical brush that has the specified solid color.
 
@@ -225,7 +224,7 @@ class BITMAPINFO(Structure):
 )
 
 
-AddFontResourceEx = WINFUNCTYPE(None)(("AddFontResourceExW", dll))
+AddFontResourceEx = dll.AddFontResourceExW
 """
 Adds the font resource from the specified file to the system.
 

```