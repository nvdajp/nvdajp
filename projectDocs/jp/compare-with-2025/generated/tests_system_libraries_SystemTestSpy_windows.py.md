# Diff for: `tests\system\libraries\SystemTestSpy\windows.py`

**Source**: `F:\nvda\gh\alphajp-251219\tests\system\libraries\SystemTestSpy\windows.py`  
**Current**: `F:\nvda\gh\alphajp-260109\tests\system\libraries\SystemTestSpy\windows.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\tests\\system\\libraries\\SystemTestSpy\\windows.py" "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\libraries\\SystemTestSpy\\windows.py"
index df2bd48..57270e0 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\tests\\system\\libraries\\SystemTestSpy\\windows.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\tests\\system\\libraries\\SystemTestSpy\\windows.py"
@@ -1,5 +1,5 @@
 # A part of NonVisual Desktop Access (NVDA)
-# Copyright (C) 2021-2025 NV Access Limited, Łukasz Golonka
+# Copyright (C) 2021-2025 NV Access Limited, Łukasz Golonka, Bill Dengler
 # This file may be used under the terms of the GNU General Public License, version 2 or later.
 # For more details see: https://www.gnu.org/licenses/gpl-2.0.html
 
@@ -75,14 +75,14 @@ def _GetVisibleWindows() -> list[Window]:
 
 def CloseWindow(window: Window) -> bool:
 	"""
-	@return: True if the window exists and the message was sent.
+	Request that the target window close gracefully (WM_CLOSE).
+	:return: True if the window exists and the message was posted.
 	"""
 	if windowWithHandleExists(window.hwndVal):
-		return bool(
-			windll.user32.CloseWindow(
-				window.hwndVal,
-			),
-		)
+		# We do not use user32.CloseWindow, which minimizes (rather than
+		# closing) the window.
+		WM_CLOSE: int = 0x0010
+		return bool(windll.user32.PostMessageW(window.hwndVal, WM_CLOSE, 0, 0))
 	return False
 
 

```