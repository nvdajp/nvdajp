# coding: UTF-8
# nvdajp_dic.py
# NVDA Japanese Team
# A part of NonVisual Desktop Access (NVDA)

import characterProcessing
import languageHandler
import config
import re
import collections
from logHandler import log

def get_long_desc(s):
	try:
		s = characterProcessing.getCharacterDescription('ja', s)[0]
	except:
		pass
	return s

def get_short_desc(s):
	s2 = characterProcessing.processSpeechSymbol('ja', s)
	if s != s2:
		log.debug("(%s)-(%s)" % (s, s2))
		return s2
	return characterProcessing.getCharacterReading('ja', s.lower())

# characters which use dictionary for spelling reading
SMALL_KANA_CHARACTERS = u'ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮヵヶｧｨｩｪｫｬｭｮｯ'
SPECIAL_KANA_CHARACTERS = SMALL_KANA_CHARACTERS + u'をヲｦはへー'

def isJapaneseLocale(locale):
	return locale[:2] == 'ja'

def isZenkakuHiragana(c):
	return re.search(ur'[ぁ-ゞ]', c) is not None

def isZenkakuKatakana(c):
	return re.search(ur'[ァ-ヾ]', c) is not None

def isHankakuKatakana(c):
	return re.search(ur'[ｦ-ﾝ｢｣]', c) is not None

def isHalfShape(c):
	return (32 < ord(c)) and (ord(c) < 128)

def isFullShapeAlphabet(c):
	return re.search(ur'[ａ-ｚＡ-Ｚ]', c) is not None

def isHalfShapeAlphabet(c):
	return re.search(ur'[a-zA-Z]', c) is not None

def isFullShapeNumber(c):
	return re.search(ur'[０-９]', c) is not None

def isKanaCharacter(c):
	return isZenkakuHiragana(c) or isZenkakuKatakana(c) or isHankakuKatakana(c)

def isLatinCharacter(c):
	return isFullShapeAlphabet(c) or isHalfShapeAlphabet(c)

def isFullShapeSymbol(c):
	return c in u'　、。，．・：；？！´｀¨＾￣＿ー―／＼～∥｜‘’“”（）〔〕［］「」｛｝〈〉＋－＝＜＞￥＄％＃＆＊＠＇＂゙゚゛゜'

def isUpper(c):
	return re.search(ur'[A-ZＡ-Ｚ]', c) is not None

def replaceSpecialKanaCharacter(c):
	if c in SPECIAL_KANA_CHARACTERS:
		c = get_short_desc(c)
	return c

CharAttr = collections.namedtuple('CharAttr', 'upper hira kata half full latin')

def getAttrDesc(a):
	d = []
	if a.hira:
		d.append(u'ヒラガナ')
	if a.kata:
		d.append(u'カタカナ')
	if a.half:
		d.append(u'ハンカク')
	if a.full:
		d.append(u'ゼンカク')
	if a.latin:
		d.append(u'エイジ')
	if a.upper:
		d.append(u'オーモジ')
	return ' '.join(d)

def hex2kana(code):
	"""
	input 0x123a
　	output u'イチニーサンエー'
	"""
	s = ''
	src = hex(code)[2:]
	src = ("000" + src)[-4:]
	for c in src:
		s += get_short_desc(c)
	return s

def getCandidateCharDesc(c, a):
	d = ''
	if a.half or isFullShapeAlphabet(c) or isFullShapeNumber(c) or isFullShapeSymbol(c):
		d = get_short_desc(c)
		log.debug(u"shortdesc (%s) %s" % (c, d))
	elif a.hira or a.kata:
		d = replaceSpecialKanaCharacter(c)
		log.debug(u"kana (%s) %s" % (c, d))
	else:
		d = get_long_desc(c)
		if d != c:
			log.debug(u"longdesc (%s) %s" % (c, d))
		else:
			d2 = characterProcessing.processSpeechSymbol('ja', c)
			if d != d2:
				log.debug(u"sym (%s) %s" % (c, d2))
				d = d2
			else:
				d = hex2kana(ord(c[0]))
				log.debug(u"code (%s) %s" % (c, d))
	if len(d) > 1:
		return ' ' + d + ' '
	return d

#TODO: merge _get_description() and getJapaneseDiscriminantReading().
#nvdajp must modify locale/ja/characterDescriptions.dic and nvdajp_dic.py.
def getJapaneseDiscriminantReading(name):
	if not name: return ''
	attrs = []
	for c in name:
		ca = CharAttr(
			isUpper(c),
			isZenkakuHiragana(c),
			isZenkakuKatakana(c),
			isHalfShape(c) or isHankakuKatakana(c),
			isFullShapeAlphabet(c) or isFullShapeNumber(c) or isFullShapeSymbol(c),
			isLatinCharacter(c))
		log.debug(u"(%s) %s" % (c, getAttrDesc(ca)))
		attrs.append((c, ca))
	s = ''
	prevAttr = None
	prevChar = None
	for a in attrs:
		# symbols treated as 'attribute unchanged'
		if prevAttr and (prevAttr.hira or prevAttr.kata) and a[0] in (u'ー', u'、', u'。'):
			if a[0] == u'ー' and prevChar in SMALL_KANA_CHARACTERS:
				s += ' ' + get_short_desc(a[0]) + ' '
			else:
				s += a[0]
		# attribute unchanged
		elif prevAttr == a[1]:
			s += getCandidateCharDesc(a[0], a[1])
			prevAttr = a[1]
		else:
			if s:
				s += u' ' + getAttrDesc(a[1]) + ' '
			elif (a[1].kata and a[0] != u'ー') or a[1].half or a[1].upper or a[1].hira or a[1].full:
				s += getAttrDesc(a[1]) + ' '
			s += getCandidateCharDesc(a[0], a[1])
			prevAttr = a[1]
		prevChar = a[0]
	s = s.replace('  ', ' ')
	return s.strip(' ')
