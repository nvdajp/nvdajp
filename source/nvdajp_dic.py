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
import speech

RE_HIRAGANA = re.compile(u'^[\u3041-\u309e]+$')

def get_long_desc(s):
	try:
		s = characterProcessing.getCharacterDescription('ja', s)[0]
	except:
		pass
	return s

def get_short_desc(s):
	s2 = characterProcessing.processSpeechSymbol('ja', s)
	if s != s2:
		log.debug("get_short_desc (%s)-(%s)" % (s, s2))
		return s2
	return characterProcessing.getCharacterReading('ja', s.lower())

# characters which use dictionary for spelling reading
SMALL_KANA_CHARACTERS = u'ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮヵヶｧｨｩｪｫｬｭｮｯ'
SPECIAL_KANA_CHARACTERS = SMALL_KANA_CHARACTERS + u'をヲｦはへー'

def isJapaneseLocale(locale=None):
	if locale is None:
		return speech.getCurrentLanguage()[:2] == 'ja'
	return locale[:2] == 'ja'

def isZenkakuHiragana(c):
	return re.search(ur'[ぁ-ゞ]', c) is not None

def isZenkakuKatakana(c):
	if c == u'ー':
		return False
	return re.search(ur'[ァ-ヾ]', c) is not None

def isHankakuKatakana(c):
	return re.search(ur'[ｦ-ﾝ｢｣､｡ｰ]', c) is not None

def isHalfShape(c):
	return (32 < ord(c)) and (ord(c) < 128)

def isFullShapeAlphabet(c):
	return re.search(ur'[ａ-ｚＡ-Ｚ]', c) is not None

def isHalfShapeAlphabet(c):
	return re.search(ur'[a-zA-Z]', c) is not None

def isFullShapeNumber(c):
	return re.search(ur'[０-９]', c) is not None

def isHalfShapeNumber(c):
	return re.search(ur'[0-9]', c) is not None

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
		d.append(u'半角')
	if a.full:
		d.append(u'全角')
	if a.latin:
		d.append(u'英字')
	if a.upper:
		d.append(u'大文字')
	return ' '.join(d)

def code2kana(code):
	"""
	input 0x123a
　	output 'イチニーサンエー'
	"""
	s = ''
	src = hex(code)[2:]
	src = ("000" + src)[-4:]
	for c in src:
		if c == '2':
			s += u'ニー'
		elif c == '5':
			s += u'ゴー'
		else:
			s += get_short_desc(c)
	return s

def code2hex(code):
	"""
	input 0x123a
　	output 'u+123a'
	"""
	s = ''
	src = hex(code)[2:]
	src = ("000" + src)[-4:]
	return 'u+' + src

def getCandidateCharDesc(c, a, forBraille=False):
	d = ''
	if forBraille and (isLatinCharacter(c) or isZenkakuHiragana(c) or isZenkakuKatakana(c) or isFullShapeNumber(c) or isHalfShapeNumber(c) or c == u'．'):
		d = c
	elif a.half or isFullShapeAlphabet(c) or isFullShapeNumber(c) or isFullShapeSymbol(c):
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
				d = code2hex(ord(c[0]))
				log.debug(u"code (%s) %s" % (c, d))
	if len(d) > 1:
		return ' ' + d + ' '
	return d

def useAttrDesc(a):
	if a[0] == u'ー':
		return False
	if a[1].half or a[1].upper or a[1].hira or a[1].kata or a[1].full:
		return True
	return False

#TODO: merge _get_description() and getJapaneseDiscriminantReading().
#nvdajp must modify locale/ja/characterDescriptions.dic and nvdajp_dic.py.
def getJapaneseDiscriminantReading(name, attrOnly=False, capAnnounced=False, forBraille=False):
	if not name: return ''
	attrs = []
	for c in name:
		ca = CharAttr(
			isUpper(c) if (not capAnnounced and not forBraille) else False,
			isZenkakuHiragana(c),
			isZenkakuKatakana(c),
			isHalfShape(c) or isHankakuKatakana(c),
			isFullShapeAlphabet(c) or isFullShapeNumber(c) or isFullShapeSymbol(c),
			isLatinCharacter(c) and not forBraille)
		log.debug(u"(%s) %s" % (c, getAttrDesc(ca)))
		attrs.append((c, ca))
	if attrOnly:
		s = ''
		for a in attrs:
			s += getAttrDesc(a[1]) + ' '
		return s
	s = ''
	prevAttr = None
	prevChar = None
	for a in attrs:
		# attribute unchanged
		if prevAttr == a[1]:
			s += getCandidateCharDesc(a[0], a[1], forBraille=forBraille)
			prevAttr = a[1]
		else:
			if s:
				s += u' '
			if useAttrDesc(a):
				s += getAttrDesc(a[1]) + ' '
			s += getCandidateCharDesc(a[0], a[1], forBraille=forBraille)
			prevAttr = a[1]
		prevChar = a[0]
	s = s.replace('  ', ' ')
	return s.strip(' ')

def processHexCode(locale, msg):
	if isJapaneseLocale(locale):
		try:
			msg = re.sub(r"u\+([0-9a-f]{4})", lambda x: "u+" + code2kana(int("0x"+x.group(1),16)), unicode(msg))
		except Exception, e:
			log.debug(e)
			pass
	return msg

def fixNewText(newText):
	log.debug(newText)
	if RE_HIRAGANA.match(newText):
		newText = ''.join([unichr(ord(c) + 0x60) for c in newText])
		log.debug('convert hiragana to katakana: ' + newText)
	if newText == u'\u30fc':
		newText = getJapaneseDiscriminantReading(newText)
		log.debug('katakana-hiragana prolonged sound mark')
	return newText
