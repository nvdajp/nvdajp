# Diff for: `source\appModules\outlook.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\appModules\outlook.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\appModules\outlook.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\appModules\\outlook.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\outlook.py"
index 09e46f8..f73bbda 100644
--- "a/F:\\nvda\\gh\\beta\\source\\appModules\\outlook.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\appModules\\outlook.py"
@@ -342,7 +342,7 @@ def event_valueChange(self):
 		"""Set focus back to the edit field when an auto-complete list item is confirmed."""
 		if vision.handler:
 			vision.handler.handleGainFocus(self)
-			api.setNavigatorObject(self, isFocus=True)
+		api.setNavigatorObject(self)
 		super().event_valueChange()
 
 

```