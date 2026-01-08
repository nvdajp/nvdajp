# Diff for: `source\gui\blockAction.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\gui\blockAction.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\gui\blockAction.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\gui\\blockAction.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\blockAction.py"
index 21fbe4a..78372d5 100644
--- "a/F:\\nvda\\gh\\beta\\source\\gui\\blockAction.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\gui\\blockAction.py"
@@ -42,9 +42,13 @@ def _isRemoteAccessDisabled() -> bool:
 def _isScreenCurtainEnabled() -> bool:
 	"""Whether screen curtain functionality is **enabled**."""
 	# Import late to avoid circular import
-	from screenCurtain import screenCurtain
+	import vision
+	from visionEnhancementProviders.screenCurtain import ScreenCurtainProvider
 
-	return screenCurtain is not None and screenCurtain.enabled
+	screenCurtainId = ScreenCurtainProvider.getSettings().getId()
+	screenCurtainProviderInfo = vision.handler.getProviderInfo(screenCurtainId)
+	isScreenCurtainRunning = bool(vision.handler.getProviderInstance(screenCurtainProviderInfo))
+	return isScreenCurtainRunning
 
 
 @dataclass

```