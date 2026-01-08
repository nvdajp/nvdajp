# Diff for: `source\characterProcessing.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\characterProcessing.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\characterProcessing.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\characterProcessing.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\characterProcessing.py"
index eb86df3..93e928d 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\characterProcessing.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\characterProcessing.py"
@@ -122,9 +122,10 @@ def __init__(self, locale: str):
 		log.debug("Loaded %d entries." % len(self._entries))
 		f.close()
 
-		# nvdajp charaters.dic
+		# BEGIN JP PATCH
+		# nvdajp characters.dic
 		self._readings = {}
-		fileName = os.path.join("locale", locale, "characters.dic")
+		fileName = os.path.join(globalVars.appDir, "locale", locale, "characters.dic")
 		if os.path.isfile(fileName):
 			f = codecs.open(fileName, "r", "utf_8_sig", errors="replace")
 			for line in f:
@@ -143,11 +144,11 @@ def __init__(self, locale: str):
 					log.warning("can't parse line '%s'" % line)
 			log.debug("Loaded %d readings." % len(self._readings))
 			f.close()
-		# nvdajp charaters.dic end
+		# nvdajp characters.dic end
 
 		# nvdajp cldr emoji
 		if "cldr" in config.conf["speech"]["symbolDictionaries"]:  # type: ignore
-			fileName = os.path.join("locale", locale, "cldr.dic")
+			fileName = os.path.join(globalVars.appDir, "locale", locale, "cldr.dic")
 			if os.path.isfile(fileName):
 				import unicodedata
 
@@ -205,7 +206,15 @@ def __init__(self, locale: str):
 			log.debug("Loaded users characters.")
 			f.close()
 		# nvdajp users characters end
+		# END JP PATCH
 
+	def getCharacterDescription(self, character: str) -> Optional[List[str]]:
+		"""
+		Looks up the given character and returns a list containing all the description strings found.
+		"""
+		return self._entries.get(character)
+
+	# BEGIN JP PATCH
 	# nvdajp reading
 	def getCharacterReading(self, character):
 		if character in self._readings:
@@ -213,12 +222,7 @@ def getCharacterReading(self, character):
 		return character
 
 	# nvdajp reading end
-
-	def getCharacterDescription(self, character: str) -> Optional[List[str]]:
-		"""
-		Looks up the given character and returns a list containing all the description strings found.
-		"""
-		return self._entries.get(character)
+	# END JP PATCH
 
 
 _charDescLocaleDataMap: LocaleDataMap[CharacterDescriptions] = LocaleDataMap(CharacterDescriptions)
@@ -243,6 +247,7 @@ def getCharacterDescription(locale: str, character: str) -> Optional[List[str]]:
 	return desc
 
 
+# BEGIN JP PATCH
 # nvdajp
 def getCharacterReading(locale, character):
 	try:
@@ -253,6 +258,7 @@ def getCharacterReading(locale, character):
 
 
 # nvdajp end
+# END JP PATCH
 
 
 # Speech symbol levels

```