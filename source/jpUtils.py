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
	return c in '　、。，．・：；？！´｀¨＾￣＿ー―／＼～∥｜‘’“”（）〔〕［］「」｛｝〈〉＋－＝＜＞￥＄％＃＆＊＠＇＂゙゚゛゜'

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
	mo = re.match('(\d{1,2}):(\d{2})', text)
	if mo:
		hour, minute = mo.group(1), mo.group(2)
		if len(hour) == 2 and hour[0] == '0': hour = hour[1:]
		if len(minute) == 2 and minute[0] == '0': minute = minute[1:]
		# Translators: hour and minute
		text = _('{hour}:{minute}').format(hour=hour, minute=minute)
	else:
		mo = re.match('([^\d]+)(\d{1,2}):(\d{2})', text)
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


## braille labels (not translated)

import typing
from speech import controlTypes

_gettext_org = _
_ = lambda x: x
_pgettext_org = pgettext
pgettext = lambda x, y: y

roleLabels: typing.Dict[controlTypes.Role, str] = {
	# Translators: Displayed in braille for an object which is a
	# window.
	controlTypes.Role.WINDOW: _("wnd"),
	# Translators: Displayed in braille for an object which is a
	# dialog.
	controlTypes.Role.DIALOG: _("dlg"),
	# Translators: Displayed in braille for an object which is a
	# check box.
	controlTypes.Role.CHECKBOX: _("chk"),
	# Translators: Displayed in braille for an object which is a
	# radio button.
	controlTypes.Role.RADIOBUTTON: _("rbtn"),
	# Translators: Displayed in braille for an object which is an
	# editable text field.
	controlTypes.Role.EDITABLETEXT: _("edt"),
	# Translators: Displayed in braille for an object which is a
	# button.
	controlTypes.Role.BUTTON: _("btn"),
	# Translators: Displayed in braille for an object which is a
	# menu bar.
	controlTypes.Role.MENUBAR: _("mnubar"),
	# Translators: Displayed in braille for an object which is a
	# menu item.
	controlTypes.Role.MENUITEM: _("mnuitem"),
	# Translators: Displayed in braille for an object which is a
	# menu.
	controlTypes.Role.POPUPMENU: _("mnu"),
	# Translators: Displayed in braille for an object which is a
	# combo box.
	controlTypes.Role.COMBOBOX: _("cbo"),
	# Translators: Displayed in braille for an object which is a
	# list.
	controlTypes.Role.LIST: _("lst"),
	# Translators: Displayed in braille for an object which is a
	# graphic.
	controlTypes.Role.GRAPHIC: _("gra"),
	# Translators: Displayed in braille for toast notifications and for an object which is a
	# help balloon.
	controlTypes.Role.HELPBALLOON: _("hlp"),
	# Translators: Displayed in braille for an object which is a
	# tool tip.
	controlTypes.Role.TOOLTIP: _("tltip"),
	# Translators: Displayed in braille for an object which is a
	# link.
	controlTypes.Role.LINK: _("lnk"),
	# Translators: Displayed in braille for an object which is a
	# tree view.
	controlTypes.Role.TREEVIEW: _("tv"),
	# Translators: Displayed in braille for an object which is a
	# tree view item.
	controlTypes.Role.TREEVIEWITEM: _("tvitem"),
	# Translators: Displayed in braille for an object which is a
	# tab control.
	controlTypes.Role.TABCONTROL: _("tabctl"),
	# Translators: Displayed in braille for an object which is a
	# progress bar.
	controlTypes.Role.PROGRESSBAR: _("prgbar"),
	# Translators: Displayed in braille for an object which is an
	# indeterminate progress bar, aka busy indicator.
	controlTypes.Role.BUSY_INDICATOR: _("bsyind"),
	# Translators: Displayed in braille for an object which is a
	# scroll bar.
	controlTypes.Role.SCROLLBAR: _("scrlbar"),
	# Translators: Displayed in braille for an object which is a
	# status bar.
	controlTypes.Role.STATUSBAR: _("stbar"),
	# Translators: Displayed in braille for an object which is a
	# table.
	controlTypes.Role.TABLE: _("tbl"),
	# Translators: Displayed in braille for an object which is a
	# tool bar.
	controlTypes.Role.TOOLBAR: _("tlbar"),
	# Translators: Displayed in braille for an object which is a
	# drop down button.
	controlTypes.Role.DROPDOWNBUTTON: _("drbtn"),
	# Displayed in braille for an object which is a
	# separator.
	controlTypes.Role.SEPARATOR: u"⠤⠤⠤⠤⠤",
	# Translators: Displayed in braille for an object which is a
	# block quote.
	controlTypes.Role.BLOCKQUOTE: _("bqt"),
	# Translators: Displayed in braille for an object which is a
	# document.
	controlTypes.Role.DOCUMENT: _("doc"),
	# Translators: Displayed in braille for an object which is a
	# application.
	controlTypes.Role.APPLICATION: _("app"),
	# Translators: Displayed in braille for an object which is a
	# grouping.
	controlTypes.Role.GROUPING: _("grp"),
	# Translators: Displayed in braille for an object which is a
	# caption.
	controlTypes.Role.CAPTION: _("cap"),
	# Translators: Displayed in braille for an object which is a
	# embedded object.
	controlTypes.Role.EMBEDDEDOBJECT: _("embedded"),
	# Translators: Displayed in braille for an object which is a
	# end note.
	controlTypes.Role.ENDNOTE: _("enote"),
	# Translators: Displayed in braille for an object which is a
	# foot note.
	controlTypes.Role.FOOTNOTE: _("fnote"),
	# Translators: Displayed in braille for an object which is a
	# terminal.
	controlTypes.Role.TERMINAL: _("term"),
	# Translators: Displayed in braille for an object which is a
	# section.
	controlTypes.Role.SECTION: _("sect"),
	# Translators: Displayed in braille for an object which is a
	# toggle button.
	controlTypes.Role.TOGGLEBUTTON: _("tgbtn"),
	# Translators: Displayed in braille for an object which is a
	# split button.
	controlTypes.Role.SPLITBUTTON: _("splbtn"),
	# Translators: Displayed in braille for an object which is a
	# menu button.
	controlTypes.Role.MENUBUTTON: _("mnubtn"),
	# Translators: Displayed in braille for an object which is a
	# spin button.
	controlTypes.Role.SPINBUTTON: _("spnbtn"),
	# Translators: Displayed in braille for an object which is a
	# tree view button.
	controlTypes.Role.TREEVIEWBUTTON: _("tvbtn"),
	# Translators: Displayed in braille for an object which is a
	# menu.
	controlTypes.Role.MENU: _("mnu"),
	# Translators: Displayed in braille for an object which is a
	# panel.
	controlTypes.Role.PANEL: _("pnl"),
	# Translators: Displayed in braille for an object which is a
	# password edit.
	controlTypes.Role.PASSWORDEDIT: _("pwdedt"),
	# Translators: Displayed in braille for an object which is deleted.
	controlTypes.Role.DELETED_CONTENT: _("del"),
	# Translators: Displayed in braille for an object which is inserted.
	controlTypes.Role.INSERTED_CONTENT: _("ins"),
	# Translators: Displayed in braille for a landmark.
	controlTypes.Role.LANDMARK: _("lmk"),
	# Translators: Displayed in braille for an object which is an article.
	controlTypes.Role.ARTICLE: _("art"),
	# Translators: Displayed in braille for an object which is a region.
	controlTypes.Role.REGION: _("rgn"),
	# Translators: Displayed in braille for an object which is a figure.
	controlTypes.Role.FIGURE: _("fig"),
	# Translators: Displayed in braille for an object which represents marked (highlighted) content
	controlTypes.Role.MARKED_CONTENT: _("hlght"),
	# Translators: Displayed in braille when an object is a comment.
	controlTypes.Role.COMMENT: _("cmnt"),
	# Translators: Displayed in braille when an object is a suggestion.
	controlTypes.Role.SUGGESTION: _("sggstn"),
	# Translators: Displayed in braille when an object is a definition.
	controlTypes.Role.DEFINITION: _("definition"),
	# Translators: Displayed in braille when an object is a switch control
	controlTypes.Role.SWITCH: _("swtch"),
}

positiveStateLabels = {
	# Translators: Displayed in braille when an object is selected.
	controlTypes.State.SELECTED: _("sel"),
	# Displayed in braille when an object (e.g. a toggle button) is pressed.
	controlTypes.State.PRESSED: u"⢎⣿⡱",
	# Displayed in braille when an object (e.g. a toggle button) is half pressed.
	controlTypes.State.HALF_PRESSED: u"⢎⣸⡱",
	# Displayed in braille when an object (e.g. a check box) is checked.
	controlTypes.State.CHECKED: u"⣏⣿⣹",
	# Displayed in braille when an object (e.g. a check box) is half checked.
	controlTypes.State.HALFCHECKED: u"⣏⣸⣹",
	# Translators: Displayed in braille when an object (e.g. an editable text field) is read-only.
	controlTypes.State.READONLY: _("ro"),
	# Translators: Displayed in braille when an object (e.g. a tree view item) is expanded.
	controlTypes.State.EXPANDED: _("-"),
	# Translators: Displayed in braille when an object (e.g. a tree view item) is collapsed.
	controlTypes.State.COLLAPSED: _("+"),
	# Translators: Displayed in braille when an object has a popup (usually a sub-menu).
	controlTypes.State.HASPOPUP: _("submnu"),
	# Translators: Displayed in braille when a protected control or a document is encountered.
	controlTypes.State.PROTECTED: _("***"),
	# Translators: Displayed in braille when a required form field is encountered.
	controlTypes.State.REQUIRED: _("req"),
	# Translators: Displayed in braille when an invalid entry has been made.
	controlTypes.State.INVALID_ENTRY: _("invalid"),
	# Translators: Displayed in braille when an object supports autocompletion.
	controlTypes.State.AUTOCOMPLETE: _("..."),
	# Translators: Displayed in braille when an edit field allows typing multiple lines of text such as comment fields on websites.
	controlTypes.State.MULTILINE: _("mln"),
	# Translators: Displayed in braille when an object is clickable.
	controlTypes.State.CLICKABLE: _("clk"),
	# Translators: Displayed in braille when an object is sorted ascending.
	controlTypes.State.SORTED_ASCENDING: _("sorted asc"),
	# Translators: Displayed in braille when an object is sorted descending.
	controlTypes.State.SORTED_DESCENDING: _("sorted desc"),
	# Translators: Displayed in braille when an object (usually a graphic) has a long description.
	controlTypes.State.HASLONGDESC: _("ldesc"),
	# Translators: Displayed in braille when there is a formula on a spreadsheet cell.
	controlTypes.State.HASFORMULA: _("frml"),
	# Translators: Displayed in braille when there is a comment for a spreadsheet cell or piece of text in a document.
	controlTypes.State.HASCOMMENT: _("cmnt"),
	# Translators: Displayed in braille when a control is switched on
	controlTypes.State.ON: "⣏⣿⣹",
}
negativeStateLabels = {
	# Translators: Displayed in braille when an object is not selected.
	controlTypes.State.SELECTED: _("nsel"),
	# Displayed in braille when an object (e.g. a toggle button) is not pressed.
	controlTypes.State.PRESSED: u"⢎⣀⡱",
	# Displayed in braille when an object (e.g. a check box) is not checked.
	controlTypes.State.CHECKED: u"⣏⣀⣹",
	# Displayed in braille when an object (e.g. a switch control) is switched off.
	controlTypes.State.ON: "⣏⣀⣹",
}

landmarkLabels = {
	# Translators: Displayed in braille for the banner landmark, normally found on web pages.
	"banner": pgettext("braille landmark abbreviation", "bnnr"),
	# Translators: Displayed in braille for the complementary landmark, normally found on web pages.
	"complementary": pgettext("braille landmark abbreviation", "cmpl"),
	# Translators: Displayed in braille for the contentinfo landmark, normally found on web pages.
	"contentinfo": pgettext("braille landmark abbreviation", "cinf"),
	# Translators: Displayed in braille for the main landmark, normally found on web pages.
	"main": pgettext("braille landmark abbreviation", "main"),
	# Translators: Displayed in braille for the navigation landmark, normally found on web pages.
	"navigation": pgettext("braille landmark abbreviation", "navi"),
	# Translators: Displayed in braille for the search landmark, normally found on web pages.
	"search": pgettext("braille landmark abbreviation", "srch"),
	# Translators: Displayed in braille for the form landmark, normally found on web pages.
	"form": pgettext("braille landmark abbreviation", "form"),
}

_ = _gettext_org
pgettext = _pgettext_org

## end of braille labels