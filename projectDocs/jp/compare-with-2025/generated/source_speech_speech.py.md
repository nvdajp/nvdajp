# Diff for: `source\speech\speech.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\speech\speech.py`  
**Current**: `F:\nvda\gh\alphajp-260109\source\speech\speech.py`

**注**: このdiffは空白文字（インデントなど）の違いを無視して表示されています。

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\speech\\speech.py" "b/F:\\nvda\\gh\\alphajp-260109\\source\\speech\\speech.py"
index 38d1211..95d9c1b 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\speech\\speech.py"
+++ "b/F:\\nvda\\gh\\alphajp-260109\\source\\speech\\speech.py"
@@ -6,7 +6,7 @@
 
 """High-level functions to speak information."""
 
-import jpUtils
+import jpUtils  # nvdajp
 import itertools
 import typing
 import weakref
@@ -40,6 +40,7 @@
 	EndUtteranceCommand,
 	SuppressUnicodeNormalizationCommand,
 	CharacterModeCommand,
+	WaveFileCommand,
 )
 from .shortcutKeys import getKeyboardShortcutsSpeech
 
@@ -52,6 +53,7 @@
 	_flattenNestedSequences,
 )
 from typing import (
+	Final,
 	Iterable,
 	Optional,
 	Dict,
@@ -66,6 +68,7 @@
 import config
 from config.configFlags import (
 	ReportLineIndentation,
+	ReportSpellingErrors,
 	ReportTableHeaders,
 	ReportCellBorders,
 	OutputMode,
@@ -84,6 +87,7 @@
 
 _speechState: Optional["SpeechState"] = None
 _curWordChars: List[str] = []
+IDEOGRAPHIC_COMMA: Final[str] = "\u3001"
 
 
 class SpeechMode(DisplayStringIntEnum):
@@ -187,7 +191,10 @@ def processText(
 	text = speechDictHandler.processText(text)
 	text = characterProcessing.processSpeechSymbols(locale, text, symbolLevel)
 	text = RE_CONVERT_WHITESPACE.sub(" ", text)
+	# BEGIN JP PATCH
+	# nvdajp: Process Kangxi radicals for Japanese character descriptions
 	text = jpUtils.processKangxiRadicals(text)
+	# END JP PATCH
 	if normalize:
 		text = unicodeNormalize(text)
 		# keep leading space for normalization message
@@ -309,7 +316,10 @@ def getCurrentLanguage() -> str:
 def spellTextInfo(
 	info: textInfos.TextInfo,
 	useCharacterDescriptions: bool = False,
+	# BEGIN JP PATCH
+	# nvdajp: useDetails parameter for detailed character descriptions
 	useDetails: bool = False,
+	# END JP PATCH
 	priority: Optional[Spri] = None,
 ) -> None:
 	"""Spells the text from the given TextInfo, honouring any LangChangeCommand objects it finds if autoLanguageSwitching is enabled."""
@@ -339,7 +349,10 @@ def speakSpelling(
 	text: str,
 	locale: Optional[str] = None,
 	useCharacterDescriptions: bool = False,
+	# BEGIN JP PATCH
+	# nvdajp: useDetails parameter for detailed character descriptions
 	useDetails: bool = False,
+	# END JP PATCH
 	priority: Optional[Spri] = None,
 ) -> None:
 	# This could be a very large list. In future we could convert this into chunks.
@@ -497,23 +510,37 @@ def _getSpellingSpeechWithoutCharMode(
 		itemIsNormalized = textIsNormalized
 		uppercase = speakCharAs.isupper()
 		if useCharacterDescriptions and charDesc:
+			# BEGIN JP PATCH
+			# nvdajp: Use ideographic comma for joining character descriptions
 			IDEOGRAPHIC_COMMA = "\u3001"
 			speakCharAs = charDesc[0] if textLength > 1 else IDEOGRAPHIC_COMMA.join(charDesc)
+			# END JP PATCH
+			charList = [speakCharAs]
 		elif useCharacterDescriptions and not charDesc and not fallbackToCharIfNoDescription:
 			return None
 		else:
 			if (symbol := characterProcessing.processSpeechSymbol(locale, speakCharAs)) != speakCharAs:
-				speakCharAs = symbol
+				charList = [symbol]
 			elif not textIsNormalized and unicodeNormalization:
 				if (normalized := unicodeNormalize(speakCharAs)) != speakCharAs:
-					speakCharAs = " ".join(
-						characterProcessing.processSpeechSymbol(locale, normChar) for normChar in normalized
-					)
+					charList = [
+						" ".join(
+							characterProcessing.processSpeechSymbol(locale, normChar)
+							for normChar in normalized
+						),
+					]
 					itemIsNormalized = True
+				else:
+					# Tried to normalize, but it didn't result in normalization at all.
+					# We need to deal with the case where splitAtCharacterBoundaries might have merged characters we need to speak separately.
+					charList = [characterProcessing.processSpeechSymbol(locale, char) for char in speakCharAs]
+			else:
+				charList = [speakCharAs]
 		if languageHandling.shouldMakeLangChangeCommand():
 			yield LangChangeCommand(locale)
+		for charToSpeak in charList:
 			yield from _getSpellingCharAddCapNotification(
-			speakCharAs,
+				charToSpeak,
 				uppercase and sayCapForCapitals,
 				capPitchChange if uppercase else 0,
 				uppercase and beepForCapitals,
@@ -574,7 +601,10 @@ def getSpellingSpeech(
 	text: str,
 	locale: Optional[str] = None,
 	useCharacterDescriptions: bool = False,
+	# BEGIN JP PATCH
+	# nvdajp: useDetails parameter for detailed character descriptions
 	useDetails: bool = False,
+	# END JP PATCH
 ) -> Generator[SequenceItemT, None, None]:
 	synth = getSynth()
 	synthConfig = config.conf["speech"][synth.name]
@@ -586,6 +616,8 @@ def getSpellingSpeech(
 	unicodeNormalization = not useCharacterDescriptions and bool(
 		config.conf["speech"]["unicodeNormalization"],
 	)
+	# BEGIN JP PATCH
+	# nvdajp: Use JP-specific spelling speech function
 	seq = jpUtils.getSpellingSpeechWithoutCharMode(
 		text,
 		locale,
@@ -599,6 +631,7 @@ def getSpellingSpeech(
 			"reportNormalizedForCharacterNavigation"
 		],
 	)
+	# END JP PATCH
 	if synthConfig["useSpellingFunctionality"]:
 		seq = _getSpellingSpeechAddCharMode(seq)
 	# This function applies Unicode normalization as appropriate.
@@ -1102,6 +1135,8 @@ def speak(  # noqa: C901
 	if speechViewer.isActive:
 		speechViewer.appendSpeechSequence(speechSequence)
 	pre_speech.notify(speechSequence=speechSequence, symbolLevel=symbolLevel, priority=priority)
+	# BEGIN JP PATCH
+	# nvdajp: Send speech to JP braille viewer
 	from gui import jpBrailleViewer
 
 	if jpBrailleViewer.isActive:
@@ -1111,6 +1146,7 @@ def speak(  # noqa: C901
 				s += item
 		if s:
 			jpBrailleViewer.appendText(s)
+	# END JP PATCH
 	if _speechState.speechMode == SpeechMode.off:
 		return
 	elif _speechState.speechMode == SpeechMode.beeps:
@@ -1489,11 +1525,14 @@ def speakTextInfo(
 	suppressBlanks: bool = False,
 	priority: Optional[Spri] = None,
 ) -> bool:
+	# BEGIN JP PATCH
+	# nvdajp: Character description mode support
 	from globalCommands import characterDescriptionMode
 
 	if characterDescriptionMode and reason == OutputReason.CARET and unit == textInfos.UNIT_CHARACTER:
 		speakSpelling(info.text, useCharacterDescriptions=True)
 		return True
+	# END JP PATCH
 	speechGen = getTextInfoSpeech(
 		info,
 		useCache,
@@ -1517,7 +1556,7 @@ def speakTextInfo(
 def getTextInfoSpeech(  # noqa: C901
 	info: textInfos.TextInfo,
 	useCache: Union[bool, SpeakTextInfoState] = True,
-	formatConfig: Dict[str, bool] = None,
+	formatConfig: dict[str, bool | int] | None = None,
 	unit: Optional[str] = None,
 	reason: OutputReason = OutputReason.QUERY,
 	_prefixSpeechCommand: Optional[SpeechCommand] = None,
@@ -1541,7 +1580,7 @@ def getTextInfoSpeech(  # noqa: C901
 	)
 	# For performance reasons, when navigating by paragraph or table cell, spelling errors will not be announced.
 	if unit in (textInfos.UNIT_PARAGRAPH, textInfos.UNIT_CELL) and reason == OutputReason.CARET:
-		formatConfig["reportSpellingErrors"] = False
+		formatConfig["reportSpellingErrors2"] = 0
 
 	# Fetch the last controlFieldStack, or make a blank one
 	controlFieldStackCache = speakTextInfoState.controlFieldStackCache if speakTextInfoState else []
@@ -1918,7 +1957,7 @@ def _getTextInfoSpeech_considerSpelling(
 	speechSequence: SpeechSequence,
 	language: str,
 ) -> Generator[SpeechSequence, None, None]:
-	if onlyInitialFields or any(isinstance(x, str) for x in speechSequence):
+	if onlyInitialFields or speechSequence:
 		yield speechSequence
 	if not onlyInitialFields:
 		spellingSequence = list(
@@ -3018,33 +3057,35 @@ def getFormatFieldSpeech(  # noqa: C901
 				# Translators: Reported when text no longer contains a bookmark
 				text = _("out of bookmark")
 				textList.append(text)
-	if formatConfig["reportSpellingErrors"]:
+	if formatConfig["reportSpellingErrors2"]:
 		invalidSpelling = attrs.get("invalid-spelling")
 		oldInvalidSpelling = attrsCache.get("invalid-spelling") if attrsCache is not None else None
 		if (invalidSpelling or oldInvalidSpelling is not None) and invalidSpelling != oldInvalidSpelling:
+			texts = []
 			if invalidSpelling:
+				if formatConfig["reportSpellingErrors2"] & ReportSpellingErrors.SOUND.value:
+					texts.append(WaveFileCommand(r"waves\textError.wav"))
+				if formatConfig["reportSpellingErrors2"] & ReportSpellingErrors.SPEECH.value:
 					# Translators: Reported when text contains a spelling error.
-				text = _("spelling error")
+					texts.append(_("spelling error"))
 			elif extraDetail:
 				# Translators: Reported when moving out of text containing a spelling error.
-				text = _("out of spelling error")
-			else:
-				text = ""
-			if text:
-				textList.append(text)
+				texts.append(_("out of spelling error"))
+			textList.extend(texts)
 		invalidGrammar = attrs.get("invalid-grammar")
 		oldInvalidGrammar = attrsCache.get("invalid-grammar") if attrsCache is not None else None
 		if (invalidGrammar or oldInvalidGrammar is not None) and invalidGrammar != oldInvalidGrammar:
+			texts = []
 			if invalidGrammar:
+				if formatConfig["reportSpellingErrors2"] & ReportSpellingErrors.SOUND.value:
+					texts.append(WaveFileCommand(r"waves\textError.wav"))
+				if formatConfig["reportSpellingErrors2"] & ReportSpellingErrors.SPEECH.value:
 					# Translators: Reported when text contains a grammar error.
-				text = _("grammar error")
+					texts.append(_("grammar error"))
 			elif extraDetail:
 				# Translators: Reported when moving out of text containing a grammar error.
-				text = _("out of grammar error")
-			else:
-				text = ""
-			if text:
-				textList.append(text)
+				texts.append(_("out of grammar error"))
+			textList.extend(texts)
 	# The line-prefix formatField attribute contains the text for a bullet or number for a list item, when the bullet or number does not appear in the actual text content.
 	# Normally this attribute could be repeated across formatFields within a list item and therefore is not safe to speak when the unit is word or character.
 	# However, some implementations (such as MS Word with UIA) do limit its useage to the very first formatField of the list item.

```