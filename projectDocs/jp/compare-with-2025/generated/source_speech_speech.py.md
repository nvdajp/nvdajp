# Diff for: `source\speech\speech.py`

**Source 2025.3.x jp**: `F:\nvda\gh\alphajp-251219\source\speech\speech.py`  
**Current**: `F:\nvda\gh\alphajp\source\speech\speech.py`

## Diff

```diff
diff --git "a/F:\\nvda\\gh\\alphajp-251219\\source\\speech\\speech.py" "b/F:\\nvda\\gh\\alphajp\\source\\speech\\speech.py"
index 38d121177a..02545fbd92 100644
--- "a/F:\\nvda\\gh\\alphajp-251219\\source\\speech\\speech.py"
+++ "b/F:\\nvda\\gh\\alphajp\\source\\speech\\speech.py"
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
@@ -499,27 +503,38 @@ def _getSpellingSpeechWithoutCharMode(
 		if useCharacterDescriptions and charDesc:
 			IDEOGRAPHIC_COMMA = "\u3001"
 			speakCharAs = charDesc[0] if textLength > 1 else IDEOGRAPHIC_COMMA.join(charDesc)
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
-		yield from _getSpellingCharAddCapNotification(
-			speakCharAs,
-			uppercase and sayCapForCapitals,
-			capPitchChange if uppercase else 0,
-			uppercase and beepForCapitals,
-			itemIsNormalized and reportNormalizedForCharacterNavigation,
-		)
-		yield EndUtteranceCommand()
+		for charToSpeak in charList:
+			yield from _getSpellingCharAddCapNotification(
+				charToSpeak,
+				uppercase and sayCapForCapitals,
+				capPitchChange if uppercase else 0,
+				uppercase and beepForCapitals,
+				itemIsNormalized and reportNormalizedForCharacterNavigation,
+			)
+			yield EndUtteranceCommand()
 
 
 def getSingleCharDescriptionDelayMS() -> int:
@@ -1517,7 +1532,7 @@ def speakTextInfo(
 def getTextInfoSpeech(  # noqa: C901
 	info: textInfos.TextInfo,
 	useCache: Union[bool, SpeakTextInfoState] = True,
-	formatConfig: Dict[str, bool] = None,
+	formatConfig: dict[str, bool | int] | None = None,
 	unit: Optional[str] = None,
 	reason: OutputReason = OutputReason.QUERY,
 	_prefixSpeechCommand: Optional[SpeechCommand] = None,
@@ -1541,7 +1556,7 @@ def getTextInfoSpeech(  # noqa: C901
 	)
 	# For performance reasons, when navigating by paragraph or table cell, spelling errors will not be announced.
 	if unit in (textInfos.UNIT_PARAGRAPH, textInfos.UNIT_CELL) and reason == OutputReason.CARET:
-		formatConfig["reportSpellingErrors"] = False
+		formatConfig["reportSpellingErrors2"] = 0
 
 	# Fetch the last controlFieldStack, or make a blank one
 	controlFieldStackCache = speakTextInfoState.controlFieldStackCache if speakTextInfoState else []
@@ -1918,7 +1933,7 @@ def _getTextInfoSpeech_considerSpelling(
 	speechSequence: SpeechSequence,
 	language: str,
 ) -> Generator[SpeechSequence, None, None]:
-	if onlyInitialFields or any(isinstance(x, str) for x in speechSequence):
+	if onlyInitialFields or speechSequence:
 		yield speechSequence
 	if not onlyInitialFields:
 		spellingSequence = list(
@@ -3018,20 +3033,21 @@ def getFormatFieldSpeech(  # noqa: C901
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
-				# Translators: Reported when text contains a spelling error.
-				text = _("spelling error")
+				if formatConfig["reportSpellingErrors2"] & ReportSpellingErrors.SOUND.value:
+					texts.append(WaveFileCommand(r"waves\textError.wav"))
+				if formatConfig["reportSpellingErrors2"] & ReportSpellingErrors.SPEECH.value:
+					# Translators: Reported when text contains a spelling error.
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

```