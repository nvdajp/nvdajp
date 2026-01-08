# Diff for: `source\vision\visionHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\vision\visionHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\vision\visionHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\vision\\visionHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\vision\\visionHandler.py"
index e3aa82d..b70d3f4 100644
--- "a/F:\\nvda\\gh\\beta\\source\\vision\\visionHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\vision\\visionHandler.py"
@@ -102,9 +102,11 @@ def postGuiInit(self) -> None:
 
 	def _getBuiltInProviderIds(self):
 		from visionEnhancementProviders.NVDAHighlighter import NVDAHighlighterSettings
+		from visionEnhancementProviders.screenCurtain import ScreenCurtainSettings
 
 		return [
 			NVDAHighlighterSettings.getId(),
+			ScreenCurtainSettings.getId(),
 		]
 
 	def _updateAllProvidersList(self):

```