# Diff for: `source\mathPres\MathCAT\preferences.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\mathPres\MathCAT\preferences.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\mathPres\MathCAT\preferences.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\mathPres\\MathCAT\\preferences.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\mathPres\\MathCAT\\preferences.py"
index 67a3d3f..10be2c4 100644
--- "a/F:\\nvda\\gh\\beta\\source\\mathPres\\MathCAT\\preferences.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\mathPres\\MathCAT\\preferences.py"
@@ -7,8 +7,8 @@
 import os
 
 import config
-import languageHandler
 import yaml
+from languageHandler import getLanguage
 from logHandler import log
 from NVDAState import ReadPaths
 from utils.displayString import DisplayStringStrEnum
@@ -241,7 +241,7 @@ def getAutoBrailleCode(
 	if not availableCodes:
 		availableCodes = getBrailleCodes()
 	if languageCode is None:
-		languageCode = languageHandler.getLanguage()
+		languageCode = getLanguage()
 
 	# de, nb, and nn should probably use Marburg when implemented upstream
 	languagesToBrailleCodes: dict[str, str] = {
@@ -285,7 +285,6 @@ def setEffectiveBrailleCode() -> None:
 			exc_info=True,
 		)
 
-
 def toNVDAConfigKey(key: str) -> str:
 	"""Converts a key for MathCAT's preferences (UpperCamelCase) to a
 	key for NVDA's configobj-based configuration (lowerCamelCase).

```