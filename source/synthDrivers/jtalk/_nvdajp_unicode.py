# _nvdajp_unicode.py
# -*- coding: utf-8 -*-

import unicodedata


def unicode_normalize(s: str) -> str:
	s = s.replace("\u00a0", " ")  # Unicode no break space
	s = s.replace("\u2002", " ")  # Unicode en space
	s = s.replace("\u2003", " ")  # Unicode em space
	s = s.replace("\u2004", " ")  # Unicode 1/3 em space
	s = s.replace("\u2005", " ")  # Unicode 1/4 em space
	s = s.replace("\u2009", " ")  # Unicode 1/5 em space
	s = s.replace("\u2006", " ")  # Unicode 1/6 em space
	s = s.replace("\u2007", " ")  # Unicode figure space
	s = s.replace("\u2008", " ")  # Unicode punctuation space
	s = s.replace("\u200a", " ")  # Unicode hair space
	#              \u200b           Unicode zero width space
	s = s.replace("\u200e", "")  # Unicode LEFT-TO-RIGHT MARK
	s = s.replace("\u200f", "")  # Unicode RIGHT-TO-LEFT MARK
	s = s.replace("\ufffd", "")  # Unicode REPLACEMENT CHARACTER
	# Mecab_text2mecab() で全角に変換され NFKC で戻せない文字
	s = s.replace("．", ".")
	s = unicodedata.normalize("NFKC", s)
	s = s.replace("\u2212", "-")  # 0x2212 MUNUS SIGN to 0x002D HYPHEN-MINUS
	s = s.replace("\u00a5", "\\")  # 0x00A5 YEN SIGN
	s = s.replace("\u301c", "~")  # 0x301C WAVE DASH

	s = s.replace("À", "A")  # 0x00c0
	s = s.replace("Á", "A")  # 0x00c1
	s = s.replace("Â", "A")  # 0x00c2
	s = s.replace("Ä", "A")  # 0x00c4
	s = s.replace("Å", "A")  # 0x00c5
	s = s.replace("Æ", "AE")  # 0x00c6
	s = s.replace("Ç", "C")  # 0x00c7
	s = s.replace("È", "E")  # 0x00c8
	s = s.replace("É", "E")  # 0x00c9
	s = s.replace("Ê", "E")  # 0x00ca
	s = s.replace("Ë", "E")  # 0x00cb
	s = s.replace("Ì", "I")  # 0x00cc
	s = s.replace("Í", "I")  # 0x00cd
	s = s.replace("Î", "I")  # 0x00ce
	s = s.replace("Ï", "I")  # 0x00cf
	s = s.replace("Ñ", "N")  # 0x00d1
	s = s.replace("Ò", "O")  # 0x00d2
	s = s.replace("Ó", "O")  # 0x00d3
	s = s.replace("Ô", "O")  # 0x00d4
	s = s.replace("Ö", "O")  # 0x00d6
	s = s.replace("Ø", "O")  # 0x00d8
	s = s.replace("Ù", "U")  # 0x00d9
	s = s.replace("Ú", "U")  # 0x00da
	s = s.replace("Û", "U")  # 0x00db
	s = s.replace("Ü", "U")  # 0x00dc
	s = s.replace("Ý", "Y")  # 0x00dd
	s = s.replace("à", "a")  # 0x00e0
	s = s.replace("á", "a")  # 0x00e1
	s = s.replace("â", "a")  # 0x00e2
	s = s.replace("ä", "a")  # 0x00e4
	s = s.replace("å", "a")  # 0x00e5
	s = s.replace("æ", "ae")  # 0x00e6
	s = s.replace("ç", "c")  # 0x00e7
	s = s.replace("è", "e")  # 0x00e8
	s = s.replace("é", "e")  # 0x00e9
	s = s.replace("ê", "e")  # 0x00ea
	s = s.replace("ë", "e")  # 0x00eb
	s = s.replace("ì", "i")  # 0x00ec
	s = s.replace("í", "i")  # 0x00ed
	s = s.replace("î", "i")  # 0x00ee
	s = s.replace("ï", "i")  # 0x00ef
	s = s.replace("ñ", "n")  # 0x00f1
	s = s.replace("ò", "o")  # 0x00f2
	s = s.replace("ó", "o")  # 0x00f3
	s = s.replace("ô", "o")  # 0x00f4
	s = s.replace("ö", "o")  # 0x00f6
	s = s.replace("ø", "o")  # 0x00f8
	s = s.replace("ù", "u")  # 0x00f9
	s = s.replace("ú", "u")  # 0x00fa
	s = s.replace("û", "u")  # 0x00fb
	s = s.replace("ü", "u")  # 0x00fc
	s = s.replace("ý", "y")  # 0x00fd
	s = s.replace("ÿ", "y")  # 0x00ff
	s = s.replace("Œ", "OE")  # 0x0152
	s = s.replace("œ", "oe")  # 0x0153
	s = s.replace("Ÿ", "Y")  # 0x0178
	return s
