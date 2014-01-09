# coding: UTF-8
# text2mecab.py for python-jtalk

import unicodedata
import re

CODE = 'utf-8'

predic = None

def text2mecab_setup():
	global predic
	if predic is None:
		predic = [
			[re.compile(u" "), u"　"],
			[re.compile(u"!"), u"！"],
			[re.compile(u"\""), u"”"],
			[re.compile(u"#"), u"＃"],
			[re.compile(u"\\$"), u"＄"],
			[re.compile(u"%"), u"％"],
			[re.compile(u"&"), u"＆"],
			[re.compile(u"'"), u"’"],
			[re.compile(u"\\("), u"（"],
			[re.compile(u"\\)"), u"）"],
			[re.compile(u"\\*"), u"＊"],
			[re.compile(u"\\+"), u"＋"],
			[re.compile(u","), u"，"],
			[re.compile(u"\\-"), u"−"],
			[re.compile(u"\\."), u"．"],
			[re.compile(u"\\/"), u"／"],
			[re.compile(u"0"), u"０"],
			[re.compile(u"1"), u"１"],
			[re.compile(u"2"), u"２"],
			[re.compile(u"3"), u"３"],
			[re.compile(u"4"), u"４"],
			[re.compile(u"5"), u"５"],
			[re.compile(u"6"), u"６"],
			[re.compile(u"7"), u"７"],
			[re.compile(u"8"), u"８"],
			[re.compile(u"9"), u"９"],
			[re.compile(u":"), u"："],
			[re.compile(u";"), u"；"],
			[re.compile(u"<"), u"＜"],
			[re.compile(u"="), u"＝"],
			[re.compile(u">"), u"＞"],
			[re.compile(u"\?"), u"？"],
			[re.compile(u"@"), u"＠"],
			[re.compile(u"A"), u"Ａ"],
			[re.compile(u"B"), u"Ｂ"],
			[re.compile(u"C"), u"Ｃ"],
			[re.compile(u"D"), u"Ｄ"],
			[re.compile(u"E"), u"Ｅ"],
			[re.compile(u"F"), u"Ｆ"],
			[re.compile(u"G"), u"Ｇ"],
			[re.compile(u"H"), u"Ｈ"],
			[re.compile(u"I"), u"Ｉ"],
			[re.compile(u"J"), u"Ｊ"],
			[re.compile(u"K"), u"Ｋ"],
			[re.compile(u"L"), u"Ｌ"],
			[re.compile(u"M"), u"Ｍ"],
			[re.compile(u"N"), u"Ｎ"],
			[re.compile(u"O"), u"Ｏ"],
			[re.compile(u"P"), u"Ｐ"],
			[re.compile(u"Q"), u"Ｑ"],
			[re.compile(u"R"), u"Ｒ"],
			[re.compile(u"S"), u"Ｓ"],
			[re.compile(u"T"), u"Ｔ"],
			[re.compile(u"U"), u"Ｕ"],
			[re.compile(u"V"), u"Ｖ"],
			[re.compile(u"W"), u"Ｗ"],
			[re.compile(u"X"), u"Ｘ"],
			[re.compile(u"Y"), u"Ｙ"],
			[re.compile(u"Z"), u"Ｚ"],
			[re.compile(u"\\["), u"［"],
			[re.compile(u"\\\\"), u"￥"],
			[re.compile(u"\\]"), u"］"],
			[re.compile(u"\\^"), u"＾"],
			[re.compile(u"_"), u"＿"],
			[re.compile(u"`"), u"‘"],
			[re.compile(u"a"), u"ａ"],
			[re.compile(u"b"), u"ｂ"],
			[re.compile(u"c"), u"ｃ"],
			[re.compile(u"d"), u"ｄ"],
			[re.compile(u"e"), u"ｅ"],
			[re.compile(u"f"), u"ｆ"],
			[re.compile(u"g"), u"ｇ"],
			[re.compile(u"h"), u"ｈ"],
			[re.compile(u"i"), u"ｉ"],
			[re.compile(u"j"), u"ｊ"],
			[re.compile(u"k"), u"ｋ"],
			[re.compile(u"l"), u"ｌ"],
			[re.compile(u"m"), u"ｍ"],
			[re.compile(u"n"), u"ｎ"],
			[re.compile(u"o"), u"ｏ"],
			[re.compile(u"p"), u"ｐ"],
			[re.compile(u"q"), u"ｑ"],
			[re.compile(u"r"), u"ｒ"],
			[re.compile(u"s"), u"ｓ"],
			[re.compile(u"t"), u"ｔ"],
			[re.compile(u"u"), u"ｕ"],
			[re.compile(u"v"), u"ｖ"],
			[re.compile(u"w"), u"ｗ"],
			[re.compile(u"x"), u"ｘ"],
			[re.compile(u"y"), u"ｙ"],
			[re.compile(u"z"), u"ｚ"],
			[re.compile(u"{"), u"｛"],
			[re.compile(u"\\|"), u"｜"],
			[re.compile(u"}"), u"｝"],
			[re.compile(u"~"), u"〜"],
		]

def text2mecab_convert(s):
	for p in predic:
		try:
			s = re.sub(p[0], p[1], s)
		except:
			pass
	return s

def text2mecab(txt, CODE_=CODE):
	text2mecab_setup()
	txt = unicodedata.normalize('NFKC', txt)
	txt = text2mecab_convert(txt)
	return txt.encode(CODE_, 'ignore')

