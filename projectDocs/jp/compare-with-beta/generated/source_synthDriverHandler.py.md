# Diff for: `source\synthDriverHandler.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\synthDriverHandler.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\synthDriverHandler.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\synthDriverHandler.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDriverHandler.py"
index ba66af5..34c02ed 100644
--- "a/F:\\nvda\\gh\\beta\\source\\synthDriverHandler.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\synthDriverHandler.py"
@@ -344,10 +344,6 @@ def languageIsSupported(self, lang: str | None) -> bool:
 				or lang == languageHandler.normalizeLanguage(availableLang).split("_")[0]
 			):
 				return True
-		rootLang = languageHandler.normalizeLanguage(lang).split("_")[0]
-		fallbackLang = f"{rootLang}-{rootLang}"
-		if fallbackLang in self.availableLanguages:
-			return True
 		return False
 
 	def initSettings(self):
@@ -487,7 +483,10 @@ def getSynthInstance(name, asDefault=False):
 
 # The synthDrivers that should be used by default.
 # The first that successfully initializes will be used when config is set to auto (I.e. new installs of NVDA).
-defaultSynthPriorityList = ["oneCore", "espeak", "silence"]
+# BEGIN JP PATCH
+# nvdajp: use nvdajp_jtalk as the default Japanese synthesizer instead of espeak
+defaultSynthPriorityList = ["oneCore", "nvdajp_jtalk", "silence"]
+# END JP PATCH
 
 
 def setSynth(name: Optional[str], isFallback: bool = False):

```