# Diff for: `source\characterProcessing.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\characterProcessing.py`  
**Current**: `F:\nvda\gh\alphajp\source\characterProcessing.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\characterProcessing.py" "b/F:\\nvda\\gh\\alphajp\\source\\characterProcessing.py"
index eb86df37c5..f0b8b096b9 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\characterProcessing.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\characterProcessing.py"
@@ -122,98 +122,6 @@ def __init__(self, locale: str):
 		log.debug("Loaded %d entries." % len(self._entries))
 		f.close()
 
-		# nvdajp charaters.dic
-		self._readings = {}
-		fileName = os.path.join("locale", locale, "characters.dic")
-		if os.path.isfile(fileName):
-			f = codecs.open(fileName, "r", "utf_8_sig", errors="replace")
-			for line in f:
-				if line.isspace() or line.startswith("#"):
-					continue
-				line = line.rstrip("\r\n")
-				temp = line.split("\t")
-				if len(temp) > 1:
-					key = temp.pop(0)
-					code = temp.pop(0)
-					rd = temp.pop(0)
-					if rd.startswith("[") and rd.endswith("]"):
-						self._readings[key] = rd[1:-1]
-					self._entries[key] = temp
-				else:
-					log.warning("can't parse line '%s'" % line)
-			log.debug("Loaded %d readings." % len(self._readings))
-			f.close()
-		# nvdajp charaters.dic end
-
-		# nvdajp cldr emoji
-		if "cldr" in config.conf["speech"]["symbolDictionaries"]:  # type: ignore
-			fileName = os.path.join("locale", locale, "cldr.dic")
-			if os.path.isfile(fileName):
-				import unicodedata
-
-				f = codecs.open(fileName, "r", "utf_8_sig", errors="replace")
-				for line in f:
-					line = line.rstrip("\r\n")
-					temp = line.split("\t")
-					if len(temp) > 1:
-						key = temp.pop(0)
-						if unicodedata.category(key[0]) not in ("So", "Cn"):
-							continue
-						rd = temp.pop(0)
-						self._readings[key] = rd
-						self._entries[key] = (rd,)
-				f.close()
-		# nvdajp cldr emoji end
-
-		# nvdajp users chardesc
-		fileName = os.path.join(globalVars.appArgs.configPath, "characterDescriptions-%s.dic" % locale)
-		if os.path.isfile(fileName):
-			log.debug("Loading users characterDescriptions-%s.dic" % locale)
-			f = codecs.open(fileName, "r", "utf_8_sig", errors="replace")
-			for line in f:
-				if line.isspace() or line.startswith("#"):
-					continue
-				line = line.rstrip("\r\n")
-				temp = line.split("\t")
-				if len(temp) > 1:
-					key = temp.pop(0)
-					self._entries[key] = temp
-				else:
-					log.warning("can't parse line '%s'" % line)
-			log.debug("Loaded users characterDescriptions.")
-			f.close()
-		# nvdajp users chardesc end
-
-		# nvdajp users characters
-		fileName = os.path.join(globalVars.appArgs.configPath, "characters-%s.dic" % locale)
-		if os.path.isfile(fileName):
-			f = codecs.open(fileName, "r", "utf_8_sig", errors="replace")
-			for line in f:
-				if line.isspace() or line.startswith("#"):
-					continue
-				line = line.rstrip("\r\n")
-				temp = line.split("\t")
-				if len(temp) > 1:
-					key = temp.pop(0)
-					code = temp.pop(0)  # noqa: F841
-					rd = temp.pop(0)
-					if rd.startswith("[") and rd.endswith("]"):
-						self._readings[key] = rd[1:-1]
-					self._entries[key] = temp
-				else:
-					log.warning("can't parse line '%s'" % line)
-			log.debug("Loaded users characters.")
-			f.close()
-		# nvdajp users characters end
-
-	# nvdajp reading
-	def getCharacterReading(self, character):
-		if character in self._readings:
-			return self._readings.get(character)
-		return character
-
-	# nvdajp reading end
-
 	def getCharacterDescription(self, character: str) -> Optional[List[str]]:
 		"""
 		Looks up the given character and returns a list containing all the description strings found.
@@ -243,18 +151,6 @@ def getCharacterDescription(locale: str, character: str) -> Optional[List[str]]:
 	return desc
 
 
-# nvdajp
-def getCharacterReading(locale, character):
-	try:
-		l = _charDescLocaleDataMap.fetchLocaleData(locale)  # noqa: E741
-	except LookupError:
-		return character
-	return l.getCharacterReading(character)
-
-
-# nvdajp end
-
-
 # Speech symbol levels
 class SymbolLevel(IntEnum):
 	"""The desired symbol level in a speech sequence or in configuration.

```