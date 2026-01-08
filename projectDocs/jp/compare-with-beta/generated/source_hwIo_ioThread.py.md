# Diff for: `source\hwIo\ioThread.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\hwIo\ioThread.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\hwIo\ioThread.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\hwIo\\ioThread.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\hwIo\\ioThread.py"
index fbcc13f..e88298e 100644
--- "a/F:\\nvda\\gh\\beta\\source\\hwIo\\ioThread.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\hwIo\\ioThread.py"
@@ -207,7 +207,7 @@ def setWaitableTimer(
 		winKernel.setWaitableTimer(
 			handle,
 			dueTime,
-			completionRoutine=ctypes.cast(self._internalApc, winBindings.kernel32.PTIMERAPCROUTINE),
+			completionRoutine=self._internalApc,
 			arg=internalParam,
 		)
 

```