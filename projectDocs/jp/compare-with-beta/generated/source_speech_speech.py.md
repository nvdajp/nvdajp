# Diff for: `source\speech\speech.py`

**Source**: `F:\nvda\gh\beta\source\speech\speech.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\speech\speech.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\beta\\source\\speech\\speech.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\speech\\speech.py"
index bb6b873..1f5cf10 100644
--- "a/F:\\nvda\\gh\\beta\\source\\speech\\speech.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\speech\\speech.py"
@@ -6,6 +6,7 @@
 
 """High-level functions to speak information."""
 
+import jpUtils  # nvdajp
 import itertools
 import typing
 import weakref
@@ -190,6 +191,10 @@ def processText(
 	text = speechDictHandler.processText(text)
 	text = characterProcessing.processSpeechSymbols(locale, text, symbolLevel)
 	text = RE_CONVERT_WHITESPACE.sub(" ", text)
+	# BEGIN JP PATCH
+	# nvdajp: Process Kangxi radicals for Japanese character descriptions
+	text = jpUtils.processKangxiRadicals(text)
+	# END JP PATCH
 	if normalize:
 		text = unicodeNormalize(text)
 		# keep leading space for normalization message
@@ -311,11 +316,20 @@ def getCurrentLanguage() -> str:
 def spellTextInfo(
 	info: textInfos.TextInfo,
 	useCharacterDescriptions: bool = False,
+	# BEGIN JP PATCH
+	# nvdajp: useDetails parameter for detailed character descriptions
+	useDetails: bool = False,
+	# END JP PATCH
 	priority: Optional[Spri] = None,
 ) -> None:
 	"""Spells the text from the given TextInfo, honouring any LangChangeCommand objects it finds if autoLanguageSwitching is enabled."""
 	if not languageHandling.shouldMakeLangChangeCommand():
-		speakSpelling(info.text, useCharacterDescriptions=useCharacterDescriptions)
+		speakSpelling(
+			info.text,
+			useCharacterDescriptions=useCharacterDescriptions,
+			useDetails=useDetails,
+			priority=priority,
+		)
 		return
 	curLanguage = None
 	for field in info.getTextWithFields({}):
@@ -324,6 +338,7 @@ def spellTextInfo(
 				field,
 				curLanguage,
 				useCharacterDescriptions=useCharacterDescriptions,
+				useDetails=useDetails,
 				priority=priority,
 			)
 		elif isinstance(field, textInfos.FieldCommand) and field.command == "formatChange":
@@ -334,6 +349,10 @@ def speakSpelling(
 	text: str,
 	locale: Optional[str] = None,
 	useCharacterDescriptions: bool = False,
+	# BEGIN JP PATCH
+	# nvdajp: useDetails parameter for detailed character descriptions
+	useDetails: bool = False,
+	# END JP PATCH
 	priority: Optional[Spri] = None,
 ) -> None:
 	# This could be a very large list. In future we could convert this into chunks.
@@ -342,7 +361,8 @@ def speakSpelling(
 			text,
 			locale=locale,
 			useCharacterDescriptions=useCharacterDescriptions,
-		),
+			useDetails=useDetails,
+		)
 	)
 	speak(seq, priority=priority)
 
@@ -490,7 +510,12 @@ def _getSpellingSpeechWithoutCharMode(
 		itemIsNormalized = textIsNormalized
 		uppercase = speakCharAs.isupper()
 		if useCharacterDescriptions and charDesc:
-			charList = [charDesc[0] if textLength > 1 else IDEOGRAPHIC_COMMA.join(charDesc)]
+			# BEGIN JP PATCH
+			# nvdajp: Use ideographic comma for joining character descriptions
+			IDEOGRAPHIC_COMMA = "\u3001"
+			speakCharAs = charDesc[0] if textLength > 1 else IDEOGRAPHIC_COMMA.join(charDesc)
+			# END JP PATCH
+			charList = [speakCharAs]
 		elif useCharacterDescriptions and not charDesc and not fallbackToCharIfNoDescription:
 			return None
 		else:
@@ -576,6 +601,10 @@ def getSpellingSpeech(
 	text: str,
 	locale: Optional[str] = None,
 	useCharacterDescriptions: bool = False,
+	# BEGIN JP PATCH
+	# nvdajp: useDetails parameter for detailed character descriptions
+	useDetails: bool = False,
+	# END JP PATCH
 ) -> Generator[SequenceItemT, None, None]:
 	synth = getSynth()
 	synthConfig = config.conf["speech"][synth.name]
@@ -587,10 +616,13 @@ def getSpellingSpeech(
 	unicodeNormalization = not useCharacterDescriptions and bool(
 		config.conf["speech"]["unicodeNormalization"],
 	)
-	seq = _getSpellingSpeechWithoutCharMode(
+	# BEGIN JP PATCH
+	# nvdajp: Use JP-specific spelling speech function
+	seq = jpUtils.getSpellingSpeechWithoutCharMode(
 		text,
 		locale,
 		useCharacterDescriptions,
+		useDetails,
 		sayCapForCapitals=synthConfig["sayCapForCapitals"],
 		capPitchChange=capPitchChange,
 		beepForCapitals=synthConfig["beepForCapitals"],
@@ -599,6 +631,7 @@ def getSpellingSpeech(
 			"reportNormalizedForCharacterNavigation"
 		],
 	)
+	# END JP PATCH
 	if synthConfig["useSpellingFunctionality"]:
 		seq = _getSpellingSpeechAddCharMode(seq)
 	# This function applies Unicode normalization as appropriate.
@@ -1105,6 +1138,18 @@ def speak(  # noqa: C901
 	if speechViewer.isActive:
 		speechViewer.appendSpeechSequence(speechSequence)
 	pre_speech.notify(speechSequence=speechSequence, symbolLevel=symbolLevel, priority=priority)
+	# BEGIN JP PATCH
+	# nvdajp: Send speech to JP braille viewer
+	from gui import jpBrailleViewer
+
+	if jpBrailleViewer.isActive:
+		s = ""
+		for item in speechSequence:
+			if isinstance(item, str):
+				s += item
+		if s:
+			jpBrailleViewer.appendText(s)
+	# END JP PATCH
 	if _speechState.speechMode == SpeechMode.off:
 		return
 	elif _speechState.speechMode == SpeechMode.beeps:
@@ -1483,6 +1528,14 @@ def speakTextInfo(
 	suppressBlanks: bool = False,
 	priority: Optional[Spri] = None,
 ) -> bool:
+	# BEGIN JP PATCH
+	# nvdajp: Character description mode support
+	from globalCommands import characterDescriptionMode
+
+	if characterDescriptionMode and reason == OutputReason.CARET and unit == textInfos.UNIT_CHARACTER:
+		speakSpelling(info.text, useCharacterDescriptions=True)
+		return True
+	# END JP PATCH
 	speechGen = getTextInfoSpeech(
 		info,
 		useCache,

```