# coding: UTF-8
#_checkCharDesc.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2012 Takuya Nishimoto (NVDA Japanese Team)

from __future__ import print_function
import re
from getord import getOrd

# CONSOLE_ENCODING = 'utf-8' # mintty
CONSOLE_ENCODING = 'cp932' # cmd.exe

LOCALE_JA = r'..\source\locale\ja'
SY_FILE = LOCALE_JA + r'\symbols.dic'
CH_FILE = LOCALE_JA + r'\characterDescriptions.dic'
CS_FILE = LOCALE_JA + r'\characters.dic'

import re

def my_print(s):
	print(s.encode(CONSOLE_ENCODING, 'ignore'))

def read_symbol_file(sy_file, returnSource=False):
	src = []
	with open(sy_file) as sy:
		mode = None
		ar = {}
		c = 0
		for line in sy:
			c += 1
			line = line.rstrip().decode('utf-8-sig')
			if line == 'complexSymbols:': 
				mode = 1
			    # print c, line
				src.append(line)
				continue
			if line == 'symbols:': 
				mode = 2
			    # print c, line
				src.append(line)
				continue
			if len(line) == 0:
				src.append(line)
				continue
			if line[0] == '#':
				src.append(line)
				continue
			if mode == 2:
				a = line.split('\t')
				if len(a) >= 2 and (len(a[0]) == 1 or a[0][0] == '\\'):
					if ar.has_key(a[0]):
						my_print("duplicated %04x %s (line %d and %d)" % (ord(a[0]), a[0], ar[a[0]][0], c))
					key = a[0]
					if key[0] == '\\':
						key = key.decode('string_escape')[0]
					s = "U+%04x" % ord(key)
					ar[key] = [c, a[1].strip()]
					# add comment field
					if a[-1][0] == '#':
						# delete existing 'U+xxxx' string
						a[-1] = re.sub(r" U\+[0-9a-f]{4}", '', a[-1])
						a[-1] += ' ' + s
					else:
						a.append('# %s %s' % (key, s))
					line = "\t".join(a)
			src.append(line)
	if returnSource:
		return ar, src
	return ar

def read_chardesc_file(ch_file):
	with open(ch_file) as ch:
		ar = {}
		c = 0
		for line in ch:
			c += 1
			line = line.rstrip().decode('utf-8')
			if len(line) == 0: continue
			if line[0] == '#': continue
			if line[0:2] == '\\#': 
				line = '#' + line[2:]
			a = line.split('\t')
			if len(a) >= 2:
				#my_print("%d %s %s" % (c, a[0], a[1]))
				ar[a[0]] = [c, a[1]]
	return ar

def read_characters_file(cs_file):
	count = 0
	with open(cs_file) as ch:
		ar = {}
		c = 0
		for line in ch:
			c += 1
			line = line.rstrip().decode('utf-8')
			if len(line) == 0: continue
			if line[0] == '#': continue
			if line[0:2] == '\\#': 
				line = '#' + line[2:]
			a = line.split('\t')
			if len(a) >= 4:
				ar[a[0]] = [c, a[3]]
				count += 1
	#my_print("total characters: %d" % count)
	return ar

def print_diff(sy, ch):
	for k,v in ch.items():
		if k in sy:
			if v[1] == sy[k][1]: continue
			my_print("ch %d %s %s / sy %d %s" % (v[0], k, v[1], sy[k][0], sy[k][1]))

C = re.compile(u'\s+')
def equals_ignore_spaces(s1, s2):
	s1 = C.sub('', s1)
	s2 = C.sub('', s2)
	if s1 == s2: return True
	return False
	
def print_different(sy, ch, skip_included=False):
	ar = {}
	for k,v in ch.items():
		if k in sy:
			s1 = v[1]
			s2 = sy[k][1]
			if equals_ignore_spaces(s1, s2): continue
			if skip_included:
				# 片方がもう一方に含まれる場合はスキップ
				if (s1 in s2) or (s2 in s1): continue
				# 'セン' を取り除いて、片方がもう一方に含まれる場合はスキップ
				s1_ = s1.replace(u'セン', '')
				s2_ = s2.replace(u'セン', '')
				if (s1_ in s2_) or (s2_ in s1_): continue
				# 'ノ ナカニ' を取り除いて、片方がもう一方に含まれる場合はスキップ
				s1_ = s1.replace(u'ノ ナカニ', '')
				s2_ = s2.replace(u'ノ ナカニ', '')
				if (s1_ in s2_) or (s2_ in s1_): continue
				# 'スーガク' を取り除いて、片方がもう一方に含まれる場合はスキップ
				s1_ = s1.replace(u' ', '')
				s2_ = s2.replace(u' ', '')
				if (s1_ in s2_) or (s2_ in s1_): continue
			output = "%04x sy %d %s / ch %d %s %s" % (ord(k), sy[k][0], sy[k][1], v[0], k, v[1])
			ar[sy[k][0]] = output
	for s in sorted(ar.items(), key=lambda x:int(x[0])):
		my_print(s[1])

def find_desc_duplicate(ch, skipKeisen=True, skipEmoji=True):
	for k,v in ch.items():
		for k2,v2 in ch.items():
			if skipKeisen and (u'ケイセン' in v[1] or u'ケイセン' in v2[1]):
				 continue
			if skipEmoji and (u'エモジ' in v[1] or u'エモジ' in v2[1]):
				 continue
			if v[0] < v2[0] and k != k2 and equals_ignore_spaces(v[1], v2[1]):
				my_print("ch %d:%s %04x / %d:%s %04x / %s" % (v[0], k, getOrd(k), v2[0], k2, getOrd(k2), v2[1]))

def isZenkakuKatakana(c):
	return re.search(ur'[ァ-ヾ]', c) is not None

def isHankakuKatakana(c):
	return re.search(ur'[ｦ-ﾝ]', c) is not None

def isHalfShape(c):
	c = c[0:1]
	return (32 < ord(c)) and (ord(c) < 128)

def add_katakana_prefix_to_characters(ch):
	ar = {}
	for k,v in ch.items():
		if isZenkakuKatakana(k):
			v = u'カタカナ ' + unicode(v)
		elif isHankakuKatakana(k):
			v = u'ハンカクカタカナ ' + unicode(v)
		elif k.isupper():
			v = u'オオモジ ' + unicode(v)
		elif isHalfShape(k):
			v = u'ハンカク ' + unicode(v)
		ar[k] = v
	return ar
