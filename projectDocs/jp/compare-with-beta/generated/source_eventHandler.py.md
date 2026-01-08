# Diff for: `source\eventHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\eventHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\eventHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\eventHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\eventHandler.py"
index 39e2945..127a777 100644
--- "a/F:\\nvda\\gh\\beta\\source\\eventHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\eventHandler.py"
@@ -501,6 +501,11 @@ def shouldAcceptEvent(eventName, windowHandle=None):
 	if eventName == "hide":
 		return False
 	if eventName == "show":
+		# BEGIN JP PATCH
+		# nvdajp: ATOKxxUIComment
+		if wClass.startswith("ATOK") and wClass.endswith("UIComment"):
+			return True
+		# END JP PATCH
 		# Only accept 'show' events for specific cases, as otherwise we get flooded.
 		return wClass in (
 			"Frame Notification Bar",  # notification bars

```