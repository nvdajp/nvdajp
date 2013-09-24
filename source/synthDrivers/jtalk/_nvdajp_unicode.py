# _nvdajp_unicode.py 
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import unicodedata

def unicode_normalize(s):
	s = s.replace('\ufffd', '')   # Unicode REPLACEMENT CHARACTER
	s = s.replace('\u200e', '')   # Unicode LEFT-TO-RIGHT MARK
	s = s.replace('\u200f', '')   # Unicode RIGHT-TO-LEFT MARK
	# Mecab_text2mecab() で全角に変換され NFKC で戻せない文字
	s = s.replace('．', '.')
	s = unicodedata.normalize('NFKC', s)
	s = s.replace('\u2212', '-')  # 0x2212 MUNUS SIGN to 0x002D HYPHEN-MINUS
	s = s.replace('\u00a5', '\\') # 0x00A5 YEN SIGN
	s = s.replace('\u301c', '~')  # 0x301C WAVE DASH
	return s

