# Diff for: `source\winVersion.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\winVersion.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\winVersion.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\winVersion.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\winVersion.py"
index 140f0d6..797da41 100644
--- "a/F:\\nvda\\gh\\beta\\source\\winVersion.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\winVersion.py"
@@ -223,6 +223,22 @@ def isUwpOcrAvailable() -> bool:
 	return os.path.isdir(UWP_OCR_DATA_PATH)
 
 
+if NVDAState._allowDeprecatedAPI():
+
+	def isFullScreenMagnificationAvailable() -> bool:
+		"""
+		Technically this is always False. The Magnification API has been marked by MS as unsupported for
+		WOW64 applications such as NVDA. For our usages, support has been added since Windows 8, relying on our
+		testing our specific usage of the API with each Windows version since Windows 8
+		"""
+		log.debugWarning(
+			"Deprecated function called: winVersion.isFullScreenMagnificationAvailable, "
+			"use visionEnhancementProviders.screenCurtain.ScreenCurtainProvider.canStart instead.",
+			stack_info=True,
+		)
+		return True
+
+
 def __getattr__(attrName: str) -> Any:
 	"""Module level `__getattr__` used to preserve backward compatibility."""
 	if attrName == "WIN7" and NVDAState._allowDeprecatedAPI():

```