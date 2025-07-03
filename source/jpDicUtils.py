# coding: UTF-8
# jpDicUtils.py
# NVDA Japanese Team
# A part of NonVisual Desktop Access (NVDA)
# Japanese dictionary and character utilities (lightweight version for testing)

import characterProcessing
import languageHandler
import config
import re
import collections
import unicodedata
from dataclasses import dataclass
from logHandler import log

RE_HIRAGANA = re.compile("^[\u3041-\u309e]+$")


def getLongDesc(s):
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


def getShortDesc(s):
	lang = languageHandler.getLanguage()[:2]
	if len(s) == 1 and ord(s) < 128 and lang != "ja":
		return characterProcessing.processSpeechSymbol(lang, s)
	s2 = characterProcessing.processSpeechSymbol("ja", s)
	if s != s2:
		return s2
	return characterProcessing.getCharacterReading("ja", s.lower())


# characters which use dictionary for spelling reading
SMALL_ZEN_KATAKANA = "ァィゥェォッャュョヮヵヶ"
SMALL_KANA_CHARACTERS = SMALL_ZEN_KATAKANA + "ぁぃぅぇぉっゃゅょゎｧｨｩｪｫｬｭｮｯ"
SPECIAL_KANA_CHARACTERS = SMALL_KANA_CHARACTERS + "をヲｦはへー"
FIX_NEW_TEXT_CHARS = SMALL_ZEN_KATAKANA + "ー"


def isJa(locale=None):
	if locale is None:
		return languageHandler.getLanguage()[:2] == "ja"
	return locale[:2] == "ja"


def isZenkakuHiragana(c):
	return re.search("[ぁ-ゞ]", c) is not None


def isZenkakuKatakana(c):
	if c == "ー":
		return False
	return re.search("[ァ-ヾ]", c) is not None


def isHankakuKatakana(c):
	return re.search("[ｦ-ﾝ｢｣､｡ｰ]", c) is not None


def isHalfShape(c):
	return len(c) == 1 and (32 < ord(c)) and (ord(c) < 128)


def isFullShapeAlphabet(c):
	return re.search("[ａ-ｚＡ-Ｚ]", c) is not None


def isHalfShapeAlphabet(c):
	return re.search("[a-zA-Z]", c) is not None


def isFullShapeNumber(c):
	return re.search("[０-９]", c) is not None


def isHalfShapeNumber(c):
	return re.search("[0-9]", c) is not None


def isKanaCharacter(c):
	return isZenkakuHiragana(c) or isZenkakuKatakana(c) or isHankakuKatakana(c)


def isLatinCharacter(c):
	return isHalfShapeAlphabet(c) or isFullShapeAlphabet(c)


def isZenkakuNumber(c):
	return isFullShapeNumber(c)


def isHankakuNumber(c):
	return isHalfShapeNumber(c)


def isNumber(c):
	return isZenkakuNumber(c) or isHankakuNumber(c)


def isZenkakuNoSpace(c):
	return isZenkakuHiragana(c) or isZenkakuKatakana(c) or isFullShapeAlphabet(c) or isFullShapeNumber(c)


def isHankakuNoSpace(c):
	return isHankakuKatakana(c) or isHalfShapeAlphabet(c) or isHalfShapeNumber(c)


def _tryGetCharacterFromKanjiDictionary(character):
	"""Try to get description from kanji dictionary entries in the form '角字エリア' -> '角字'"""
	try:
		descriptions = characterProcessing.getCharacterDescription("ja", character)
		if not descriptions:
			return None
		
		# Check if any description contains typical kanji dictionary terms
		for desc in descriptions:
			if re.search(r'字|偏|旁|部首', desc):
				return desc
		
		# Return first description if available
		return descriptions[0] if descriptions else None
	except Exception:
		return None


def _addCharacterType(s, character, sayCharTypes):
	if not sayCharTypes:
		return s
	
	characterType = ""
	
	if isZenkakuHiragana(character):
		characterType = "ヒラガナ"
	elif isZenkakuKatakana(character):
		characterType = "カタカナ"
	elif isHankakuKatakana(character):
		characterType = "半角カタカナ"
	elif isFullShapeAlphabet(character):
		characterType = "全角英字"
	elif isHalfShapeAlphabet(character):
		characterType = "半角英字"
	elif isFullShapeNumber(character):
		characterType = "全角数字"
	elif isHalfShapeNumber(character):
		characterType = "半角数字"
	elif ord(character) >= 0x4E00 and ord(character) <= 0x9FFF:
		characterType = "漢字"
	
	if characterType:
		return f"{characterType} {s}"
	return s


@dataclass
class JaCharDescription:
	character: str
	short_description: str
	long_description: str
	character_type: str = ""


def getJaCharDescription(character, longDesc=True, sayCharTypes=True):
	"""Get Japanese character description"""
	short_desc = getShortDesc(character)
	long_desc = getLongDesc(character) if longDesc else short_desc
	
	if sayCharTypes:
		short_desc = _addCharacterType(short_desc, character, True)
		long_desc = _addCharacterType(long_desc, character, True) if longDesc else short_desc
	
	return JaCharDescription(
		character=character,
		short_description=short_desc,
		long_description=long_desc
	)


def getJaCharAttrDetails(character, sayCapForCapitals=True, sayCharTypes=True):
	"""Get Japanese character attribute details for speech output"""
	if not character:
		return ""
	
	desc = getJaCharDescription(character, longDesc=False, sayCharTypes=sayCharTypes)
	result = desc.short_description
	
	# Add capitalization info if applicable
	if sayCapForCapitals and character.isupper() and isHalfShapeAlphabet(character):
		result = f"オオモジ {result}"
	
	return result


def isCharLike(s):
	"""Check if string is a single character or character-like"""
	return len(s) == 1


def normalizeText(text, isCandidate=False):
	"""Normalize text for Japanese processing"""
	if not text:
		return text
	
	newText = text
	if not isCandidate:
		for c in FIX_NEW_TEXT_CHARS:
			newText = newText.replace(c, " " + getShortDesc(c) + " ")
	return newText