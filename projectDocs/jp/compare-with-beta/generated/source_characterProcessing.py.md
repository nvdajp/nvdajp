# Diff for: `source\characterProcessing.py`

**Source 2025.3.x jp**: `F:\nvda\gh\beta\source\characterProcessing.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\characterProcessing.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\characterProcessing.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\characterProcessing.py"
index 238c4da..93e928d 100644
--- "a/F:\\nvda\\gh\\beta\\source\\characterProcessing.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\characterProcessing.py"
@@ -22,7 +22,6 @@
 	TypeVar,
 )
 
-import NVDAState
 from logHandler import log
 import globalVars
 import config
@@ -123,12 +122,108 @@ def __init__(self, locale: str):
 		log.debug("Loaded %d entries." % len(self._entries))
 		f.close()
 
+		# BEGIN JP PATCH
+		# nvdajp characters.dic
+		self._readings = {}
+		fileName = os.path.join(globalVars.appDir, "locale", locale, "characters.dic")
+		if os.path.isfile(fileName):
+			f = codecs.open(fileName, "r", "utf_8_sig", errors="replace")
+			for line in f:
+				if line.isspace() or line.startswith("#"):
+					continue
+				line = line.rstrip("\r\n")
+				temp = line.split("\t")
+				if len(temp) > 1:
+					key = temp.pop(0)
+					code = temp.pop(0)
+					rd = temp.pop(0)
+					if rd.startswith("[") and rd.endswith("]"):
+						self._readings[key] = rd[1:-1]
+					self._entries[key] = temp
+				else:
+					log.warning("can't parse line '%s'" % line)
+			log.debug("Loaded %d readings." % len(self._readings))
+			f.close()
+		# nvdajp characters.dic end
+
+		# nvdajp cldr emoji
+		if "cldr" in config.conf["speech"]["symbolDictionaries"]:  # type: ignore
+			fileName = os.path.join(globalVars.appDir, "locale", locale, "cldr.dic")
+			if os.path.isfile(fileName):
+				import unicodedata
+
+				f = codecs.open(fileName, "r", "utf_8_sig", errors="replace")
+				for line in f:
+					line = line.rstrip("\r\n")
+					temp = line.split("\t")
+					if len(temp) > 1:
+						key = temp.pop(0)
+						if unicodedata.category(key[0]) not in ("So", "Cn"):
+							continue
+						rd = temp.pop(0)
+						self._readings[key] = rd
+						self._entries[key] = (rd,)
+				f.close()
+		# nvdajp cldr emoji end
+
+		# nvdajp users chardesc
+		fileName = os.path.join(globalVars.appArgs.configPath, "characterDescriptions-%s.dic" % locale)
+		if os.path.isfile(fileName):
+			log.debug("Loading users characterDescriptions-%s.dic" % locale)
+			f = codecs.open(fileName, "r", "utf_8_sig", errors="replace")
+			for line in f:
+				if line.isspace() or line.startswith("#"):
+					continue
+				line = line.rstrip("\r\n")
+				temp = line.split("\t")
+				if len(temp) > 1:
+					key = temp.pop(0)
+					self._entries[key] = temp
+				else:
+					log.warning("can't parse line '%s'" % line)
+			log.debug("Loaded users characterDescriptions.")
+			f.close()
+		# nvdajp users chardesc end
+
+		# nvdajp users characters
+		fileName = os.path.join(globalVars.appArgs.configPath, "characters-%s.dic" % locale)
+		if os.path.isfile(fileName):
+			f = codecs.open(fileName, "r", "utf_8_sig", errors="replace")
+			for line in f:
+				if line.isspace() or line.startswith("#"):
+					continue
+				line = line.rstrip("\r\n")
+				temp = line.split("\t")
+				if len(temp) > 1:
+					key = temp.pop(0)
+					code = temp.pop(0)  # noqa: F841
+					rd = temp.pop(0)
+					if rd.startswith("[") and rd.endswith("]"):
+						self._readings[key] = rd[1:-1]
+					self._entries[key] = temp
+				else:
+					log.warning("can't parse line '%s'" % line)
+			log.debug("Loaded users characters.")
+			f.close()
+		# nvdajp users characters end
+		# END JP PATCH
+
 	def getCharacterDescription(self, character: str) -> Optional[List[str]]:
 		"""
 		Looks up the given character and returns a list containing all the description strings found.
 		"""
 		return self._entries.get(character)
 
+	# BEGIN JP PATCH
+	# nvdajp reading
+	def getCharacterReading(self, character):
+		if character in self._readings:
+			return self._readings.get(character)
+		return character
+
+	# nvdajp reading end
+	# END JP PATCH
+
 
 _charDescLocaleDataMap: LocaleDataMap[CharacterDescriptions] = LocaleDataMap(CharacterDescriptions)
 
@@ -152,6 +247,20 @@ def getCharacterDescription(locale: str, character: str) -> Optional[List[str]]:
 	return desc
 
 
+# BEGIN JP PATCH
+# nvdajp
+def getCharacterReading(locale, character):
+	try:
+		l = _charDescLocaleDataMap.fetchLocaleData(locale)  # noqa: E741
+	except LookupError:
+		return character
+	return l.getCharacterReading(character)
+
+
+# nvdajp end
+# END JP PATCH
+
+
 # Speech symbol levels
 class SymbolLevel(IntEnum):
 	"""The desired symbol level in a speech sequence or in configuration.
@@ -357,9 +466,6 @@ def save(self, fileName=None):
 		@raise ValueError: If C{fileName} is C{None}
 			and L{load} or L{save} has not been called.
 		"""
-		if not NVDAState.shouldWriteToDisk():
-			log.debugWarning("Not saving speech symbols, as shouldWriteToDisk returned False.")
-			return
 		if fileName:
 			self.fileName = fileName
 		elif self.fileName:

```