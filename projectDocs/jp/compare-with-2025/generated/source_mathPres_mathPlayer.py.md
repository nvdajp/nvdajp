# Diff for: `source\mathPres\mathPlayer.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\mathPres\mathPlayer.py`  
**Current**: `F:\nvda\gh\alphajp\source\mathPres\mathPlayer.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\mathPres\\mathPlayer.py" "b/F:\\nvda\\gh\\alphajp\\source\\mathPres\\mathPlayer.py"
index e86e2df4cf..1b9938263a 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\mathPres\\mathPlayer.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\mathPres\\mathPlayer.py"
@@ -179,8 +179,6 @@ def _setSpeechLanguage(self, mathMl):
 		lang = mathPres.getLanguageFromMath(mathMl)
 		if not lang:
 			lang = speech.getCurrentLanguage()
-		if config.conf["language"]["alwaysSpeakMathInEnglish"]:
-			lang = "en"
 		self._mpSpeechSettings.SetLanguage(lang.replace("_", "-"))
 		self._language = lang
 

```