# coding: UTF-8
# jpDicUtils.py
# NVDA Japanese Team
# A part of NonVisual Desktop Access (NVDA)
# for unittest, see ../jptools/jpDicTest.py

import languageHandler
import config
import re
import collections
from dataclasses import dataclass

RE_HIRAGANA = re.compile("^[\u3041-\u309e]+$")


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
	return isFullShapeAlphabet(c) or isHalfShapeAlphabet(c)


def isFullShapeSymbol(c):
	return (
		c
		in "　、。，．・：；？！´｀¨＾￣＿ー―／＼～〜∥｜‘’“”（）〔〕［］「」｛｝〈〉＋－＝＜＞￥＄％＃＆＊＠＇＂゙゚゛゜"
	)


def isUpper(c):
	return (len(c) == 1) and (re.search("[A-ZＡ-Ｚ]", c) is not None)


CharAttr = collections.namedtuple("CharAttr", "upper hira kata half full latin")


def getAttrDesc(a):
	d = []
	if a.hira:
		# Translators: character attribute name
		d.append(_("hiragana"))
	if a.kata:
		# Translators: character attribute name
		d.append(_("katakana"))
	if a.half:
		# Translators: character attribute name
		d.append(_("half shape"))
	if a.full:
		# Translators: character attribute name
		d.append(_("full shape"))
	if a.latin:
		# Translators: character attribute name
		d.append(_("latin"))
	if a.upper:
		# Translators: cap will be spoken before the given letter when it is capitalized.
		capMsg = _("cap %s")
		(capMsgBefore, capMsgAfter) = capMsg.split("%s")
		d.append(capMsgBefore)
	return " ".join(d)


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
	""" """
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


def getPitchChangeForCharAttr(uppercase, jpAttr, capPitchChange):
	""" """
	if uppercase and capPitchChange:
		return capPitchChange
	conf = config.conf["language"]
	if jpAttr.jpZenkakuKatakana and conf["jpKatakanaPitchChange"]:
		return conf["jpKatakanaPitchChange"]
	elif jpAttr.jpHankakuKatakana and conf["halfShapePitchChange"]:
		return conf["halfShapePitchChange"]
	elif jpAttr.halfShape and conf["halfShapePitchChange"]:
		return conf["halfShapePitchChange"]
	return 0


def code2hex(code):
	"""
	input 0x123a
	output 'u+0123a'
	"""
	# s = ''
	src = hex(code)[2:]
	src = ("0000" + src)[-5:]
	if src[0] == "0":
		src = src[1:]
	return "u+" + src


def useAttrDesc(a):
	if a[0] == "ー":
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
	uc = (o0 - 0xD800) * 0x800 + (o1 - 0xDC00)
	return uc


def splitChars(name):
	# handle surrogate pairs
	nameChars = []
	n = len(name)
	p = 0
	while p < n:
		o0 = ord(name[p])
		if (0xD800 <= o0 <= 0xDBFF) and (p + 1 < n):
			# o1 = ord(name[p+1])
			# assert 0xdc00 <= o1 <= 0xdfff:
			# uc = (o0 - 0xd800) * 0x800 + (o1 - 0xdc00)
			c = name[p] + name[p + 1]
			nameChars.append(c)
			# log.info("%d %d %d (%s)" % (n, p, p+1, c))
			p += 2
		else:
			c = name[p]
			nameChars.append(c)
			# log.info("%d %d (%s)" % (n, p, c))
			p += 1
	# log.info(repr(nameChars))
	return nameChars


def modifyTimeText(text):
	mo = re.match("(\\d{1,2}):(\\d{2})", text)
	if mo:
		hour, minute = mo.group(1), mo.group(2)
		if len(hour) == 2 and hour[0] == "0":
			hour = hour[1:]  # noqa: E701
		if len(minute) == 2 and minute[0] == "0":
			minute = minute[1:]  # noqa: E701
		# Translators: hour and minute
		text = _("{hour}:{minute}").format(hour=hour, minute=minute)
	else:
		mo = re.match("([^\\d]+)(\\d{1,2}):(\\d{2})", text)
		if mo:
			am_or_pm, hour, minute = mo.group(1), mo.group(2), mo.group(3)
			if len(hour) == 2 and hour[0] == "0":
				hour = hour[1:]  # noqa: E701
			if len(minute) == 2 and minute[0] == "0":
				minute = minute[1:]  # noqa: E701
			# Translators: hour and minute
			text = am_or_pm + _("{hour}:{minute}").format(hour=hour, minute=minute)
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
		kangxiRadicalsTable = str.maketrans("".join(left), "".join(right))
	return source.translate(kangxiRadicalsTable)
