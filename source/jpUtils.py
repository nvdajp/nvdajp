# coding: UTF-8
# jpUtils.py
# NVDA Japanese Team
# A part of NonVisual Desktop Access (NVDA)
# for unittest, see ../jptools/jpDicTest.py

import characterProcessing
import languageHandler
import config
import re
import collections
import unicodedata
from dataclasses import dataclass
from logHandler import log

RE_HIRAGANA = re.compile('^[\u3041-\u309e]+$')

def getLongDesc(s):
	try:
		lang = languageHandler.getLanguage()[:2]
		if len(s) == 1 and ord(s) < 128 and lang != 'ja':
			d = characterProcessing.getCharacterDescription(lang, s)
			log.debug(repr([s, d, 0]))
			if d:
				r = '  '.join(d)
				return r
		d = characterProcessing.getCharacterDescription('ja', s)
		log.debug(repr([s, d, 1]))
		if d:
			r = '  '.join(d)
			return r
	except Exception as e:
		log.debug(repr(e))
	log.debug(repr([s, 2]))
	return s

def getShortDesc(s):
	lang = languageHandler.getLanguage()[:2]
	if len(s) == 1 and ord(s) < 128 and lang != 'ja':
		return characterProcessing.processSpeechSymbol(lang, s)
	s2 = characterProcessing.processSpeechSymbol('ja', s)
	if s != s2:
		return s2
	return characterProcessing.getCharacterReading('ja', s.lower())

# characters which use dictionary for spelling reading
SMALL_ZEN_KATAKANA = 'ァィゥェォッャュョヮヵヶ'
SMALL_KANA_CHARACTERS = SMALL_ZEN_KATAKANA + 'ぁぃぅぇぉっゃゅょゎｧｨｩｪｫｬｭｮｯ'
SPECIAL_KANA_CHARACTERS = SMALL_KANA_CHARACTERS + 'をヲｦはへー'
FIX_NEW_TEXT_CHARS = SMALL_ZEN_KATAKANA + 'ー'

def isJa(locale=None):
	if locale is None:
		return languageHandler.getLanguage()[:2] == 'ja'
	return locale[:2] == 'ja'

def isZenkakuHiragana(c):
	return re.search('[ぁ-ゞ]', c) is not None

def isZenkakuKatakana(c):
	if c == 'ー':
		return False
	return re.search('[ァ-ヾ]', c) is not None

def isHankakuKatakana(c):
	return re.search('[ｦ-ﾝ｢｣､｡ｰ]', c) is not None

def isHalfShape(c):
	return len(c) == 1 and (32 < ord(c)) and (ord(c) < 128)

def isFullShapeAlphabet(c):
	return re.search('[ａ-ｚＡ-Ｚ]', c) is not None

def isHalfShapeAlphabet(c):
	return re.search('[a-zA-Z]', c) is not None

def isFullShapeNumber(c):
	return re.search('[０-９]', c) is not None

def isHalfShapeNumber(c):
	return re.search('[0-9]', c) is not None

def isKanaCharacter(c):
	return isZenkakuHiragana(c) or isZenkakuKatakana(c) or isHankakuKatakana(c)

def isLatinCharacter(c):
	return isFullShapeAlphabet(c) or isHalfShapeAlphabet(c)

def isFullShapeSymbol(c):
	return c in '　、。，．・：；？！´｀¨＾￣＿ー―／＼～〜∥｜‘’“”（）〔〕［］「」｛｝〈〉＋－＝＜＞￥＄％＃＆＊＠＇＂゙゚゛゜'

def isUpper(c):
	return (len(c) == 1) and (re.search('[A-ZＡ-Ｚ]', c) is not None)

def replaceSpecialKanaCharacter(c):
	if c in SPECIAL_KANA_CHARACTERS:
		c = getShortDesc(c)
	return c

CharAttr = collections.namedtuple('CharAttr', 'upper hira kata half full latin')

def getAttrDesc(a):
	d = []
	if a.hira:
		# Translators: character attribute name
		d.append(_('hiragana'))
	if a.kata:
		# Translators: character attribute name
		d.append(_('katakana'))
	if a.half:
		# Translators: character attribute name
		d.append(_('half shape'))
	if a.full:
		# Translators: character attribute name
		d.append(_('full shape'))
	if a.latin:
		# Translators: character attribute name
		d.append(_('latin'))
	if a.upper:
		# Translators: cap will be spoken before the given letter when it is capitalized.
		capMsg = _("cap %s")
		(capMsgBefore, capMsgAfter) = capMsg.split('%s')
		d.append(capMsgBefore)
	return ' '.join(d)


@dataclass
class JpAttr:
	jpZenkakuHiragana: bool
	jpZenkakuKatakana: bool
	jpHankakuKatakana: bool
	jpLatinCharacter: bool
	nonJpLatinCharacter: bool
	jpFullShapeAlphabet: bool
	nonJpFullShapeAlphabet: bool
	jpFullShapeSymbol: bool
	jpFullShape: bool
	halfShape: bool
	usePhoneticReadingLatin: bool
	usePhoneticReadingKana: bool


def getJpAttr(locale, char, useDetails):
	"""
	"""
	_isJa = isJa(locale)
	jpZenkakuHiragana = _isJa and isZenkakuHiragana(char)
	jpZenkakuKatakana = _isJa and isZenkakuKatakana(char)
	jpHankakuKatakana = _isJa and isHankakuKatakana(char)
	jpLatinCharacter = _isJa and isLatinCharacter(char)
	nonJpLatinCharacter = (not _isJa) and isLatinCharacter(char)
	jpFullShapeAlphabet = _isJa and isFullShapeAlphabet(char)
	nonJpFullShapeAlphabet = (not _isJa) and isFullShapeAlphabet(char)
	jpFullShapeSymbol = _isJa and isFullShapeSymbol(char)
	jpFullShape = jpFullShapeAlphabet or jpFullShapeSymbol
	halfShape = _isJa and isHalfShape(char)
	usePhoneticReadingLatin = useDetails and config.conf["language"]["jpPhoneticReadingLatin"]
	usePhoneticReadingKana = useDetails and config.conf["language"]["jpPhoneticReadingKana"]
	jpAttr = JpAttr(
		jpZenkakuHiragana,
		jpZenkakuKatakana,
		jpHankakuKatakana,
		jpLatinCharacter,
		nonJpLatinCharacter,
		jpFullShapeAlphabet,
		nonJpFullShapeAlphabet,
		jpFullShapeSymbol,
		jpFullShape,
		halfShape,
		usePhoneticReadingLatin,
		usePhoneticReadingKana,
	)
	return jpAttr


def getCharDesc(locale, char, jpAttr):
	"""
	"""
	if jpAttr.jpLatinCharacter and not jpAttr.usePhoneticReadingLatin:
		charDesc = (getShortDesc(char.lower()),)
	elif jpAttr.nonJpLatinCharacter and not jpAttr.usePhoneticReadingLatin:
		charDesc = (char.lower(),)
	elif jpAttr.nonJpFullShapeAlphabet and not jpAttr.usePhoneticReadingLatin:
		charDesc = (unicodedata.normalize('NFKC', char.lower()),)
	elif jpAttr.nonJpFullShapeAlphabet and jpAttr.usePhoneticReadingLatin:
		charDesc = characterProcessing.getCharacterDescription(locale, unicodedata.normalize('NFKC', char.lower()))
	elif (jpAttr.jpZenkakuHiragana or jpAttr.jpZenkakuKatakana or jpAttr.jpHankakuKatakana) and not jpAttr.usePhoneticReadingKana:
		charDesc = (getShortDesc(char),)
	else:
		charDesc = characterProcessing.getCharacterDescription(locale, char.lower())
	log.debug(repr([locale, char, ("%0x" % getOrd(char)), charDesc]))
	return charDesc


def getPitchChangeForCharAttr(uppercase, jpAttr, capPitchChange):
	"""
	"""
	if uppercase and capPitchChange:
		return capPitchChange
	conf = config.conf['language']
	if jpAttr.jpZenkakuKatakana and conf['jpKatakanaPitchChange']:
		return conf['jpKatakanaPitchChange']
	elif jpAttr.jpHankakuKatakana and conf['halfShapePitchChange']:
		return conf['halfShapePitchChange']
	elif jpAttr.halfShape and conf['halfShapePitchChange']:
		return conf['halfShapePitchChange']
	return 0


def getJaCharAttrDetails(char, sayCapForCapitals, sayCharTypes):
	r = getDiscriminantReading(char, attrOnly=True, sayCapForCapitals=sayCapForCapitals, sayCharTypes=sayCharTypes).rstrip()
	log.debug(repr(r))
	return r


def code2kana(code):
	"""
	input 0x123a
	output 'イチニーサンエー'
	"""
	s = ''
	src = hex(code)[2:]
	src = ("0000" + src)[-5:]
	if src[0] == '0':
		src = src[1:]
	for c in src:
		if c == '2':
			s += 'ニー'
		elif c == '5':
			s += 'ゴー'
		else:
			s += getShortDesc(c)
	return s

def code2hex(code):
	"""
	input 0x123a
	output 'u+0123a'
	"""
	s = ''
	src = hex(code)[2:]
	src = ("0000" + src)[-5:]
	if src[0] == '0':
		src = src[1:]
	return 'u+' + src

def getCandidateCharDesc(c, a, forBraille=False):
	d = ''
	if forBraille and (isLatinCharacter(c) or isZenkakuHiragana(c) or isZenkakuKatakana(c) or isFullShapeNumber(c) or isHalfShapeNumber(c) or c == '．'):
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
			d2 = characterProcessing.processSpeechSymbol('ja', c)
			if d != d2:
				log.debug("sym (%s) %s" % (c, d2))
				d = d2
			elif (0xd800 <= ord(c[0]) <= 0xdbff) and len(c) == 2:
				uc = (ord(c[0]) - 0xd800) * 0x800 + (ord(c[1]) - 0xdc00)
				d = code2hex(uc)
				log.debug("sp (%s) %s" % (c, d))
			else:
				d = code2hex(ord(c[0]))
				log.debug("code (%s) %s" % (c, d))
	if len(d) > 1:
		return ' ' + d + ' '
	return d

def useAttrDesc(a):
	if a[0] == 'ー':
		return False
	if a[1].half or a[1].upper or a[1].hira or a[1].kata or a[1].full:
		return True
	return False

def getOrd(s):
	# handle surrogate pairs
	if len(s) == 1:
		return ord(s)
	if len(s) != 2:
		raise Exception
	o0 = ord(s[0])
	o1 = ord(s[1])
	uc = (o0 - 0xd800) * 0x800 + (o1 - 0xdc00)
	return uc

def splitChars(name):
	# handle surrogate pairs
	nameChars = []
	n = len(name)
	p = 0
	while p < n:
		o0 = ord(name[p])
		if (0xd800 <= o0 <= 0xdbff) and (p + 1 < n):
			#o1 = ord(name[p+1])
			# assert 0xdc00 <= o1 <= 0xdfff:
			#uc = (o0 - 0xd800) * 0x800 + (o1 - 0xdc00)
			c = name[p] + name[p+1]
			nameChars.append(c)
			#log.info("%d %d %d (%s)" % (n, p, p+1, c))
			p += 2
		else:
			c = name[p]
			nameChars.append(c)
			#log.info("%d %d (%s)" % (n, p, c))
			p += 1
	#log.info(repr(nameChars))
	return nameChars

def getDiscriminantReading(name, attrOnly=False, sayCapForCapitals=False, forBraille=False, sayCharTypes=True):
	if not name: return ''
	nameChars = splitChars(name)
	attrs = []
	for uc in nameChars:
		c = uc[0]
		ca = CharAttr(
			isUpper(c) if (sayCapForCapitals and not forBraille) else False,
			sayCharTypes and isZenkakuHiragana(c),
			sayCharTypes and isZenkakuKatakana(c),
			sayCharTypes and (isHalfShape(c) or isHankakuKatakana(c)),
			sayCharTypes and (isFullShapeAlphabet(c) or isFullShapeNumber(c) or isFullShapeSymbol(c)),
			sayCharTypes and (isLatinCharacter(c) and not forBraille))
		if not attrOnly:
			log.debug("(%s) %d %s" % (uc, len(c), getAttrDesc(ca)))
		attrs.append((uc, ca))
	if attrOnly:
		s = ''
		for a in attrs:
			s += getAttrDesc(a[1]) + ' '
		return s
	s = ''
	prevAttr = None
	# prevChar = None
	for a in attrs:
		# attribute unchanged
		if prevAttr == a[1]:
			s += getCandidateCharDesc(a[0], a[1], forBraille=forBraille)
			prevAttr = a[1]
		else:
			if s:
				s += ' '
			if useAttrDesc(a):
				s += getAttrDesc(a[1]) + ' '
			s += getCandidateCharDesc(a[0], a[1], forBraille=forBraille)
			prevAttr = a[1]
		# prevChar = a[0]
	s = s.replace('  ', ' ')
	r = s.strip(' ')
	log.debug(repr(r))
	return r


def getDiscrptionForBraille(name, attrOnly=False, sayCapForCapitals=False):
	return getDiscriminantReading(
		name, attrOnly=attrOnly, sayCapForCapitals=sayCapForCapitals, forBraille=True
	)


def processHexCode(locale, msg):
	if isJa(locale):
		try:
			msg = re.sub(r"u\+([0-9a-f]{4})", lambda x: "u+" + code2kana(int("0x"+x.group(1),16)), str(msg))
		except Exception as e:
			log.debug(e)
			pass
	return msg

def fixNewText(newText, isCandidate=False):
	log.debug(newText)
	if RE_HIRAGANA.match(newText):
		newText = ''.join([chr(ord(c) + 0x60) for c in newText])
		log.debug('convert hiragana to katakana: ' + newText)
	if not isCandidate:
		for c in FIX_NEW_TEXT_CHARS:
			newText = newText.replace(c, ' ' + getShortDesc(c) + ' ')
	return newText


from typing import Generator
from speech.types import SequenceItemT
from speech.commands import (
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
	if capPitchChange:
		yield PitchCommand(offset=capPitchChange)
	if beepForCapitals:
		yield BeepCommand(2000, 50)
	if capMsgBefore:
		yield capMsgBefore
	yield speakCharAs
	if capMsgAfter:
		yield capMsgAfter
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
) -> Generator[SequenceItemT, None, None]:
	
	from speech import (
		getCurrentLanguage,
		getCharDescListFromText,
		LANGS_WITH_CONJUNCT_CHARS,
	)
	defaultLanguage=getCurrentLanguage()
	if not locale or (not config.conf['speech']['autoDialectSwitching'] and locale.split('_')[0]==defaultLanguage.split('_')[0]):
		locale=defaultLanguage

	if not text:
		# Translators: This is spoken when NVDA moves to an empty line.
		yield _("blank")
		return
	if not text.isspace():
		text=text.rstrip()

	textLength=len(text)
	count = 0
	localeHasConjuncts = True if locale.split('_',1)[0] in LANGS_WITH_CONJUNCT_CHARS else False
	charDescList = getCharDescListFromText(text,locale) if localeHasConjuncts else text
	for item in charDescList:
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
			speakCharAs=charDesc[0] if textLength>1 else IDEOGRAPHIC_COMMA.join(charDesc)
		else:
			speakCharAs=characterProcessing.processSpeechSymbol(locale,speakCharAs)
		if config.conf['speech']['autoLanguageSwitching']:
			yield LangChangeCommand(locale)
		yield from _getSpellingCharAddCapNotification(
			speakCharOrg,
			speakCharAs,
			uppercase and sayCapForCapitals,
			pitchChange,
			uppercase and beepForCapitals,
			useDetails,
		)
		yield EndUtteranceCommand()


def modifyTimeText(text):
	mo = re.match('(\\d{1,2}):(\\d{2})', text)
	if mo:
		hour, minute = mo.group(1), mo.group(2)
		if len(hour) == 2 and hour[0] == '0': hour = hour[1:]
		if len(minute) == 2 and minute[0] == '0': minute = minute[1:]
		# Translators: hour and minute
		text = _('{hour}:{minute}').format(hour=hour, minute=minute)
	else:
		mo = re.match('([^\\d]+)(\\d{1,2}):(\\d{2})', text)
		if mo:
			am_or_pm, hour, minute = mo.group(1), mo.group(2), mo.group(3)
			if len(hour) == 2 and hour[0] == '0': hour = hour[1:]
			if len(minute) == 2 and minute[0] == '0': minute = minute[1:]
			# Translators: hour and minute
			text = am_or_pm + _('{hour}:{minute}').format(hour=hour, minute=minute)
	return text


kangxiRadicalsTable = None

def processKangxiRadicals(source):
	global kangxiRadicalsTable
	if not kangxiRadicalsTable:
		items = [
			# 02exx CJK部首補助 CJK Radicals Supplement
			"⺐尢",
			"⺓幺",
			"⻑長",
			"⻤鬼",
			# 02fxx 康熙部首 Kangxi Radicals
			"⼀一",
			"⼁丨",
			"⼂丶",
			"⼃丿",
			"⼄乙",
			"⼅亅",
			"⼆二",
			"⼇亠",
			"⼈人",
			"⼉儿",
			"⼊入",
			"⼋八",
			"⼌冂",
			"⼍冖",
			"⼎冫",
			"⼏几",
			"⼐凵",
			"⼑刀",
			"⼒力",
			"⼓勹",
			"⼔匕",
			"⼕匚",
			"⼖匸",
			"⼗十",
			"⼘卜",
			"⼙卩",
			"⼚厂",
			"⼛厶",
			"⼜又",
			"⼝口",
			"⼞囗",
			"⼟土",
			"⼠士",
			"⼡夂",
			"⼢夊",
			"⼣夕",
			"⼤大",
			"⼥女",
			"⼦子",
			"⼧宀",
			"⼨寸",
			"⼩小",
			"⼪尢",
			"⼫尸",
			"⼬屮",
			"⼭山",
			"⼮巛",
			"⼯工",
			"⼰己",
			"⼱巾",
			"⼲干",
			"⼳幺",
			"⼴广",
			"⼵廴",
			"⼶廾",
			"⼷弋",
			"⼸弓",
			"⼹彐",
			"⼺彡",
			"⼻彳",
			"⼼心",
			"⼽戈",
			"⼾戶",
			"⼿手",
			"⽀支",
			"⽁攴",
			"⽂文",
			"⽃斗",
			"⽄斤",
			"⽅方",
			"⽆无",
			"⽇日",
			"⽈曰",
			"⽉月",
			"⽊木",
			"⽋欠",
			"⽌止",
			"⽍歹",
			"⽎殳",
			"⽏毋",
			"⽐比",
			"⽑毛",
			"⽒氏",
			"⽓气",
			"⽔水",
			"⽕火",
			"⽖爪",
			"⽗父",
			"⽘爻",
			"⽙爿",
			"⽚片",
			"⽛牙",
			"⽜牛",
			"⽝犬",
			"⽞玄",
			"⽟玉",
			"⽠瓜",
			"⽡瓦",
			"⽢甘",
			"⽣生",
			"⽤用",
			"⽥田",
			"⽦疋",
			"⽧疒",
			"⽨癶",
			"⽩白",
			"⽪皮",
			"⽫皿",
			"⽬目",
			"⽭矛",
			"⽮矢",
			"⽯石",
			"⽰示",
			"⽱禸",
			"⽲禾",
			"⽳穴",
			"⽴立",
			"⽵竹",
			"⽶米",
			"⽷糸",
			"⽸缶",
			"⽹网",
			"⽺羊",
			"⽻羽",
			"⽼老",
			"⽽而",
			"⽾耒",
			"⽿耳",
			"⾀聿",
			"⾁肉",
			"⾂臣",
			"⾃自",
			"⾄至",
			"⾅臼",
			"⾆舌",
			"⾇舛",
			"⾈舟",
			"⾉艮",
			"⾊色",
			"⾋艸",
			"⾌虍",
			"⾍虫",
			"⾎血",
			"⾏行",
			"⾐衣",
			"⾑襾",
			"⾒見",
			"⾓角",
			"⾔言",
			"⾕谷",
			"⾖豆",
			"⾗豕",
			"⾘豸",
			"⾙貝",
			"⾚赤",
			"⾛走",
			"⾜足",
			"⾝身",
			"⾞車",
			"⾟辛",
			"⾠辰",
			"⾡辵",
			"⾢邑",
			"⾣酉",
			"⾤釆",
			"⾥里",
			"⾦金",
			"⾧長",
			"⾨門",
			"⾩阜",
			"⾪隶",
			"⾫隹",
			"⾬雨",
			"⾭靑",
			"⾮非",
			"⾯面",
			"⾰革",
			"⾱韋",
			"⾲韭",
			"⾳音",
			"⾴頁",
			"⾵風",
			"⾶飛",
			"⾷食",
			"⾸首",
			"⾹香",
			"⾺馬",
			"⾻骨",
			"⾼高",
			"⾽髟",
			"⾾鬥",
			"⾿鬯",
			"⿀鬲",
			"⿁鬼",
			"⿂魚",
			"⿃鳥",
			"⿄鹵",
			"⿅鹿",
			"⿆麥",
			"⿇麻",
			"⿈黃",
			"⿉黍",
			"⿊黑",
			"⿋黹",
			"⿌黽",
			"⿍鼎",
			"⿎鼓",
			"⿏鼠",
			"⿐鼻",
			"⿑齊",
			"⿒齒",
			"⿓龍",
			"⿔龜",
			"⿕龠",
		]
		left, right = zip(*items)
		kangxiRadicalsTable = str.maketrans(''.join(left), ''.join(right))
	return source.translate(kangxiRadicalsTable)
