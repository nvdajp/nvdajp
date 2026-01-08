# Diff for: `source\mathPres\MathCAT\MathCAT.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\mathPres\MathCAT\MathCAT.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\mathPres\MathCAT\MathCAT.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\mathPres\\MathCAT\\MathCAT.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\mathPres\\MathCAT\\MathCAT.py"
index 00de1eb..db39595 100644
--- "a/F:\\nvda\\gh\\beta\\source\\mathPres\\MathCAT\\MathCAT.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\mathPres\\MathCAT\\MathCAT.py"
@@ -42,7 +42,6 @@
 
 import mathPres
 from .localization import getLanguageToUse
-from .preferences import setEffectiveBrailleCode
 from .speech import convertSSMLTextForNVDA
 
 
@@ -333,7 +332,6 @@ def __init__(self):
 			log.info(f"MathCAT {libmathcat.GetVersion()} installed. Using rules dir: {rulesDir}")
 			libmathcat.SetRulesDir(rulesDir)
 			libmathcat.SetPreference("TTS", "SSML")
-			setEffectiveBrailleCode()
 		except Exception:
 			log.exception()
 			# Translators: this message directs users to look in the log file

```