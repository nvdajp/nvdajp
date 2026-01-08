# Diff for: `source\screenBitmap.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\screenBitmap.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\screenBitmap.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\screenBitmap.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\screenBitmap.py"
index da079b2..54ad64b 100644
--- "a/F:\\nvda\\gh\\beta\\source\\screenBitmap.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\screenBitmap.py"
@@ -64,7 +64,7 @@ def captureImage(self, x, y, w, h):
 			winGDI.SRCCOPY,
 		)
 		# Fetch the pixels from our memory bitmap and store them in a buffer to be returned
-		buffer = (winBindings.gdi32.RGBQUAD * self.width * self.height)()
+		buffer = (winBindings.gdi32.RGBQUAD * (self.width * self.height))()
 		winBindings.gdi32.GetDIBits(
 			self._memDC,
 			self._memBitmap,

```