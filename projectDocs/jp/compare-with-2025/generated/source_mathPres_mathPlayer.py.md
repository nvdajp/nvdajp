# Diff for: `source\mathPres\mathPlayer.py`

**Source**: `F:\nvda\gh\alphajp-251219\source\mathPres\mathPlayer.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\mathPres\mathPlayer.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\mathPres\\mathPlayer.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\mathPres\\mathPlayer.py"
index e86e2df..1b99382 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\mathPres\\mathPlayer.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\mathPres\\mathPlayer.py"
@@ -179,8 +179,6 @@ def _setSpeechLanguage(self, mathMl):
 		lang = mathPres.getLanguageFromMath(mathMl)
 		if not lang:
 			lang = speech.getCurrentLanguage()
-		if config.conf["language"]["alwaysSpeakMathInEnglish"]:
-			lang = "en"
 		self._mpSpeechSettings.SetLanguage(lang.replace("_", "-"))
 		self._language = lang
 

```