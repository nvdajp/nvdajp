# Diff for: `source\IAccessibleHandler\internalWinEventHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\IAccessibleHandler\internalWinEventHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\IAccessibleHandler\internalWinEventHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\IAccessibleHandler\\internalWinEventHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\IAccessibleHandler\\internalWinEventHandler.py"
index 4669248..e2b17d4 100644
--- "a/F:\\nvda\\gh\\beta\\source\\IAccessibleHandler\\internalWinEventHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\IAccessibleHandler\\internalWinEventHandler.py"
@@ -66,17 +66,7 @@
 
 
 # C901: winEventCallback is too complex
-def winEventCallback(
-	handle: int | None,
-	eventID: int,
-	window: int | None,
-	objectID: int,
-	childID: int,
-	threadID: int,
-	timestamp: int,
-) -> None:  # noqa: C901
-	if window is None:
-		window = 0
+def winEventCallback(handle, eventID, window, objectID, childID, threadID, timestamp):  # noqa: C901
 	if isMSAADebugLoggingEnabled():
 		log.debug(
 			f"Hook received winEvent: {getWinEventLogInfo(window, objectID, childID, eventID, threadID)}",

```