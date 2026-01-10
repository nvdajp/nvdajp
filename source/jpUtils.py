# coding: UTF-8
# jpUtils.py
# NVDA Japanese Team
# A part of NonVisual Desktop Access (NVDA)

import re  # noqa: E402
import unicodedata  # noqa: E402
import languageHandler  # noqa: E402
from logHandler import log  # noqa: E402
from jpDicUtils import (  # noqa: E402
	isJa,  # noqa: F401
	isZenkakuHiragana,  # noqa: F401
	isZenkakuKatakana,  # noqa: F401
	isHankakuKatakana,  # noqa: F401
	isHalfShape,  # noqa: F401
	isFullShapeAlphabet,  # noqa: F401
	isHalfShapeAlphabet,  # noqa: F401
	isFullShapeNumber,  # noqa: F401
	isHalfShapeNumber,  # noqa: F401
	isKanaCharacter,  # noqa: F401
	isLatinCharacter,  # noqa: F401
	isFullShapeSymbol,  # noqa: F401
	isUpper,  # noqa: F401
	getAttrDesc,  # noqa: F401
	getJpAttr,  # noqa: F401
	getPitchChangeForCharAttr,  # noqa: F401
	code2hex,  # noqa: F401
	useAttrDesc,  # noqa: F401
	getOrd,  # noqa: F401
	splitChars,  # noqa: F401
	modifyTimeText,  # noqa: F401
	processKangxiRadicals,  # noqa: F401
	CharAttr,  # noqa: F401
	JpAttr,  # noqa: F401
)


from typing import Generator, Any  # noqa: E402
import config  # noqa: E402
import characterProcessing  # noqa: E402
from speech.types import SequenceItemT  # noqa: E402
from speech.commands import (  # noqa: E402
	LangChangeCommand,
	EndUtteranceCommand,
	PitchCommand,
	BeepCommand,
)


def _getSpellingCharAddCapNotification(
	speakCharOrg: str,
	speakCharAs: str,
	sayCapForCapitals: bool,
	capPitchChange: int,
	beepForCapitals: bool,
	sayCharTypes: bool,
	reportNormalized: bool = False,
) -> Generator[SequenceItemT, None, None]:
	"""This function produces a speech sequence containing a character to be spelt as well as commands
	to indicate that this character is uppercase if applicable.
	@param speakCharOrg: The character.
	@param speakCharAs: The character as it will be spoken by the synthesizer.
	@param sayCapForCapitals: indicates if 'cap' should be reported along with the currently spelt character.
	@param capPitchChange: pitch offset to apply while spelling the currently spelt character.
	@param beepForCapitals: indicates if a cap notification beep should be produced while spelling the currently
	spellt character.
	@param sayCharTypes: indicates if character types should be reported.
	"""
	capMsgBefore = getJaCharAttrDetails(speakCharOrg, sayCapForCapitals, sayCharTypes)
	capMsgAfter = None
	if reportNormalized:
		# Translators: 'Normalized' will be spoken after the given letter when it is normalized.
		normalizedMsg = _("%s normalized")
		normalizedMsgBefore, normalizedMsgAfter = normalizedMsg.split("%s")
	else:
		normalizedMsgBefore = normalizedMsgAfter = ""

	if capPitchChange:
		yield PitchCommand(offset=capPitchChange)
	if normalizedMsgBefore:
		yield normalizedMsgBefore
	if beepForCapitals:
		yield BeepCommand(2000, 50)
	if capMsgBefore:
		yield capMsgBefore
	yield speakCharAs
	if capMsgAfter:
		yield capMsgAfter
	if normalizedMsgAfter:
		yield normalizedMsgAfter
	if capPitchChange:
		yield PitchCommand()


def getSpellingSpeechWithoutCharMode(
	text: str,
	locale: str,
	useCharacterDescriptions: bool,
	useDetails: bool,
	sayCapForCapitals: bool,
	capPitchChange: int,
	beepForCapitals: bool,
	fallbackToCharIfNoDescription: bool = True,
	unicodeNormalization: bool = False,
	reportNormalizedForCharacterNavigation: bool = False,
) -> Generator[SequenceItemT, None, None]:
	from speech import (
		getCurrentLanguage,
		getCharDescListFromText,
		LANGS_WITH_CONJUNCT_CHARS,
	)
	from textUtils import unicodeNormalize

	defaultLanguage = getCurrentLanguage()
	speech_conf: dict[str, Any] = config.conf["speech"]  # type: ignore[assignment]
	if not locale or (
		not speech_conf["autoDialectSwitching"]
		and locale.split("_")[0] == defaultLanguage.split("_")[0]
	):
		locale = defaultLanguage

	if not text:
		# Translators: This is spoken when NVDA moves to an empty line.
		yield _("blank")
		return
	if not text.isspace():
		text = text.rstrip()

	textLength = len(text)
	isNormalized = False
	if unicodeNormalization and textLength > 1:
		normalized = unicodeNormalize(text)
		if len(normalized) == 1:
			# Normalization of a composition
			text = normalized
			isNormalized = True
	# count = 0
	localeHasConjuncts = True if locale.split("_", 1)[0] in LANGS_WITH_CONJUNCT_CHARS else False
	charDescList = getCharDescListFromText(text, locale) if localeHasConjuncts else text
	for item in charDescList:
		charDesc: tuple[str, ...] | list[str] | str | None = None
		if localeHasConjuncts:
			# item is a tuple containing character and its description
			speakCharOrg = item[0]
			charDesc = item[1]
		else:
			# item is just a character.
			speakCharOrg = item
			if useCharacterDescriptions:
				charDesc = characterProcessing.getCharacterDescription(locale, speakCharOrg)
		uppercase = speakCharOrg.isupper()
		jpAttr = getJpAttr(locale, speakCharOrg, useDetails)
		speakCharAs = speakCharOrg
		pitchChange = getPitchChangeForCharAttr(uppercase, jpAttr, capPitchChange)
		if isJa(locale) and useCharacterDescriptions:
			charDesc = getCharDesc(locale, speakCharOrg, jpAttr)
		if useCharacterDescriptions and charDesc:
			IDEOGRAPHIC_COMMA = "\u3001"
			speakCharAs = charDesc[0] if textLength > 1 else IDEOGRAPHIC_COMMA.join(charDesc)
		elif useCharacterDescriptions and not charDesc and not fallbackToCharIfNoDescription:
			return None
		else:
			if (symbol := characterProcessing.processSpeechSymbol(locale, speakCharAs)) != speakCharAs:
				speakCharAs = symbol
			elif not isNormalized and unicodeNormalization:
				if (normalized := unicodeNormalize(speakCharAs)) != speakCharAs:
					speakCharAs = " ".join(
						characterProcessing.processSpeechSymbol(locale, normChar) for normChar in normalized
					)
					isNormalized = True
		if speech_conf["autoLanguageSwitching"]:
			yield LangChangeCommand(locale)
		yield from _getSpellingCharAddCapNotification(
			speakCharOrg,
			speakCharAs,
			uppercase and sayCapForCapitals,
			pitchChange,
			uppercase and beepForCapitals,
			sayCharTypes=useDetails,
			reportNormalized=isNormalized and reportNormalizedForCharacterNavigation,
		)
		yield EndUtteranceCommand()


# Constants for character processing
RE_HIRAGANA = re.compile("^[\u3041-\u309e]+$")
SMALL_ZEN_KATAKANA = "ァィゥェォッャュョヮヵヶ"
SMALL_KANA_CHARACTERS = SMALL_ZEN_KATAKANA + "ぁぃぅぇぉっゃゅょゎｧｨｩｪｫｬｭｮｯ"
SPECIAL_KANA_CHARACTERS = SMALL_KANA_CHARACTERS + "をヲｦはへー"
FIX_NEW_TEXT_CHARS = SMALL_ZEN_KATAKANA + "ー"


def getLongDesc(s: str) -> str:
	try:
		lang = languageHandler.getLanguage()[:2]
		if len(s) == 1 and ord(s) < 128 and lang != "ja":
			d = characterProcessing.getCharacterDescription(lang, s)
			log.debug(repr([s, d, 0]))
			if d:
				r = "  ".join(d)
				return r
		d = characterProcessing.getCharacterDescription("ja", s)
		log.debug(repr([s, d, 1]))
		if d:
			r = "  ".join(d)
			return r
	except Exception as e:
		log.debug(repr(e))
	log.debug(repr([s, 2]))
	return s


def getShortDesc(s: str) -> str:
	lang = languageHandler.getLanguage()[:2]
	if len(s) == 1 and ord(s) < 128 and lang != "ja":
		return characterProcessing.processSpeechSymbol(lang, s)
	s2 = characterProcessing.processSpeechSymbol("ja", s)
	if s != s2:
		return s2
	return characterProcessing.getCharacterReading("ja", s.lower())


def replaceSpecialKanaCharacter(c: str) -> str:
	if c in SPECIAL_KANA_CHARACTERS:
		c = getShortDesc(c)
	return c


def getCharDesc(locale: str, char: str, jpAttr: JpAttr) -> tuple[str, ...]:
	""" """
	if jpAttr.jpLatinCharacter and not jpAttr.usePhoneticReadingLatin:
		charDesc = (getShortDesc(char.lower()),)
	elif jpAttr.nonJpLatinCharacter and not jpAttr.usePhoneticReadingLatin:
		charDesc = (char.lower(),)
	elif jpAttr.nonJpFullShapeAlphabet and not jpAttr.usePhoneticReadingLatin:
		charDesc = (unicodedata.normalize("NFKC", char.lower()),)
	elif jpAttr.nonJpFullShapeAlphabet and jpAttr.usePhoneticReadingLatin:
		charDesc = characterProcessing.getCharacterDescription(
			locale, unicodedata.normalize("NFKC", char.lower())
		)
	elif (
		jpAttr.jpZenkakuHiragana or jpAttr.jpZenkakuKatakana or jpAttr.jpHankakuKatakana
	) and not jpAttr.usePhoneticReadingKana:
		charDesc = (getShortDesc(char),)
	else:
		charDesc = characterProcessing.getCharacterDescription(locale, char.lower())
	log.debug(repr([locale, char, ("%0x" % getOrd(char)), charDesc]))
	return charDesc


def code2kana(code: int) -> str:
	"""
	input 0x123a
	output 'イチニーサンエー'
	"""
	s = ""
	src = hex(code)[2:]
	src = ("0000" + src)[-5:]
	if src[0] == "0":
		src = src[1:]
	for c in src:
		if c == "2":
			s += "ニー"
		elif c == "5":
			s += "ゴー"
		else:
			s += getShortDesc(c)
	return s


def getCandidateCharDesc(c, a, forBraille=False):
	d = ""
	if forBraille and (
		isLatinCharacter(c)
		or isZenkakuHiragana(c)
		or isZenkakuKatakana(c)
		or isFullShapeNumber(c)
		or isHalfShapeNumber(c)
		or c == "．"
	):
		d = c
	elif a.half or isFullShapeAlphabet(c) or isFullShapeNumber(c) or isFullShapeSymbol(c):
		d = getShortDesc(c)
		log.debug("shortdesc (%s) %s" % (c, d))
	elif a.hira or a.kata:
		d = replaceSpecialKanaCharacter(c)
		log.debug("kana (%s) %s" % (c, d))
	else:
		d = getLongDesc(c)
		if d.endswith(" ブシュホジョ") and forBraille:
			d = d.replace(" ブシュホジョ", " 部首補助")
		if d.endswith(" コーキブシュ") and forBraille:
			d = d.replace(" コーキブシュ", " 康熙部首")
		if d != c:
			log.debug("longdesc (%s) %s" % (c, d))
		else:
			d2 = characterProcessing.processSpeechSymbol("ja", c)
			if d != d2:
				log.debug("sym (%s) %s" % (c, d2))
				d = d2
			elif (0xD800 <= ord(c[0]) <= 0xDBFF) and len(c) == 2:
				uc = (ord(c[0]) - 0xD800) * 0x800 + (ord(c[1]) - 0xDC00)
				d = code2hex(uc)
				log.debug("sp (%s) %s" % (c, d))
			else:
				d = code2hex(ord(c[0]))
				log.debug("code (%s) %s" % (c, d))
	if len(d) > 1:
		return " " + d + " "
	return d


def getDiscriminantReading(
	name: str, attrOnly: bool = False, sayCapForCapitals: bool = False, forBraille: bool = False, sayCharTypes: bool = True
) -> str:
	if not name:
		return ""  # noqa: E701
	nameChars = splitChars(name)
	attrs: list[tuple[str, CharAttr]] = []
	for uc in nameChars:
		c = uc[0]
		ca = CharAttr(
			isUpper(c) if (sayCapForCapitals and not forBraille) else False,
			sayCharTypes and isZenkakuHiragana(c),
			sayCharTypes and isZenkakuKatakana(c),
			sayCharTypes and (isHalfShape(c) or isHankakuKatakana(c)),
			sayCharTypes and (isFullShapeAlphabet(c) or isFullShapeNumber(c) or isFullShapeSymbol(c)),
			sayCharTypes and (isLatinCharacter(c) and not forBraille),
		)
		if not attrOnly:
			log.debug("(%s) %d %s" % (uc, len(c), getAttrDesc(ca)))
		attrs.append((uc, ca))
	if attrOnly:
		s = ""
		for a in attrs:
			s += getAttrDesc(a[1]) + " "
		return s
	s = ""
	prevAttr = None
	# prevChar = None
	for a in attrs:
		# attribute unchanged
		if prevAttr == a[1]:
			s += getCandidateCharDesc(a[0], a[1], forBraille=forBraille)
			prevAttr = a[1]
		else:
			if s:
				s += " "
			if useAttrDesc(a):
				s += getAttrDesc(a[1]) + " "
			s += getCandidateCharDesc(a[0], a[1], forBraille=forBraille)
			prevAttr = a[1]
		# prevChar = a[0]
	s = s.replace("  ", " ")
	r = s.strip(" ")
	log.debug(repr(r))
	return r


def getJaCharAttrDetails(char: str, sayCapForCapitals: bool, sayCharTypes: bool) -> str:
	r = getDiscriminantReading(
		char, attrOnly=True, sayCapForCapitals=sayCapForCapitals, sayCharTypes=sayCharTypes
	).rstrip()
	log.debug(repr(r))
	return r


def getDescriptionForBraille(name: str, attrOnly: bool = False, sayCapForCapitals: bool = False) -> str:
	return getDiscriminantReading(
		name, attrOnly=attrOnly, sayCapForCapitals=sayCapForCapitals, forBraille=True
	)


def processHexCode(locale: str, msg: str) -> str:
	if isJa(locale):
		try:
			msg = re.sub(
				r"u\+([0-9a-f]{4})", lambda x: "u+" + code2kana(int("0x" + x.group(1), 16)), str(msg)
			)
		except Exception as e:
			log.debug(e)
			pass
	return msg


def fixNewText(newText: str, isCandidate: bool = False) -> str:
	log.debug(newText)
	if RE_HIRAGANA.match(newText):
		newText = "".join([chr(ord(c) + 0x60) for c in newText])
		log.debug("convert hiragana to katakana: " + newText)
	if not isCandidate:
		for c in FIX_NEW_TEXT_CHARS:
			newText = newText.replace(c, " " + getShortDesc(c) + " ")
	return newText
