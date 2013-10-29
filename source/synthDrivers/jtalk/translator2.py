# coding: UTF-8
#translator2.py (Japanese Braille translator Phase 2)
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2012-2013 Takuya Nishimoto (NVDA Japanese Team)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from __future__ import unicode_literals
import os
import copy
from _nvdajp_unicode import unicode_normalize
from mecab import *
import translator1

_logwrite = None

try:
	from logHandler import log
	_logwrite = log.debug
except:
	def __print(s): print s
	_logwrite = __print

CONNECTED_MORPHS = {
	'について': [
		['に', 'ニ', '0/1', None, None, '*'],
		['ついて', 'ツイテ', '1/3', '動詞', '*', '*'],
		],
	'により': [
		['に', 'ニ', '0/1', None, None, '*'],
		['より', 'ヨリ', '0/2', '動詞', '*', '*'],
		],
	'による': [
		['に', 'ニ', '0/1', None, None, '*'],
		['よる', 'ヨル', '0/2', '動詞', '*', '*'],
		],
	'において': [
		['に', 'ニ', '0/1', None, None, '*'],
		['おいて', 'オイテ', '0/3', '動詞', '*', '*'],
		],
	'における': [
		['に', 'ニ', '0/1', None, None, '*'],
		['おける', 'オケル', '0/3', '動詞', '*', '*'],
		],
	'によって': [
		['に', 'ニ', '0/1', None, None, '*'],
		['よって', 'ヨッテ', '0/3', '動詞', '*', '*'],
		],
	'にとって': [
		['に', 'ニ', '0/1', None, None, '*'],
		['とって', 'トッテ', '0/3', '動詞', '*', '*'],
		],
	'に対して': [
		['に', 'ニ', '0/1', None, None, '*'],
		['対して', 'タイシテ', '1/4', '動詞', '*', '*'],
		],
	'に関して': [
		['に', 'ニ', '0/1', None, None, '*'],
		['関して', 'カンシテ', '1/4', '動詞', '*', '*'],
		],
	'につき': [
		['に', 'ニ', '0/1', None, None, '*'],
		['つき', 'ツキ', '1/2', '動詞', '*', '*'],
		],
	'という': [
		['と', 'ト', '0/1', None, None, '*'],
		['いう', 'イウ', '0/2', '動詞', '*', '*'],
		],
	'どうして': [
		['どう', 'ドー', '0/2', None, None, '*'],
		['して', 'シテ', '0/2', '動詞', '*', '*'],
		],
	'として': [
		['と', 'ト', '1/1', None, None, '*'],
		['して', 'シテ', '0/2', '動詞', '*', '*'],
		],
	'なくなる': [
		['なく', 'ナク', '2/2', None, None, None],
		['なる', 'ナル', '1/2', '動詞', '自立', None],
		],
}

class MecabMorph(object):
	__slots__ = ('hyouki', 'nhyouki', 'hinshi1', 'hinshi2', 'hinshi3', 'hinshi4', 
				 'type1', 'type2', 'kihon',
				 'kana', 'yomi', 'accent', 'output', 'sepflag')

	def __init__(self):
		self.hyouki = '' # 表記
		self.nhyouki = '' # Unicode 正規化された表記
		self.hinshi1 = ''
		self.hinshi2 = ''
		self.hinshi3 = ''
		self.hinshi4 = ''
		self.type1 = ''
		self.type2 = ''
		self.kihon = ''
		self.kana = ''
		self.yomi = ''
		self.accent = ''
		self.output = ''
		self.sepflag = False # この後でマスアケをするか？
		
	# 付属語
	def is_substantive_word(self):
		if self.hinshi1 == '記号': return False
		if self.hinshi2 == '接頭': return True
		if self.hinshi2 == '接尾': return True
		if self.hinshi1 == '助動詞' and self.hyouki == 'ない': return False
		if self.hinshi1 == '名詞' and self.hyouki == 'の': return True
		if self.hinshi1 == '形容詞' and self.hyouki == 'なく': return True
		if self.hinshi1 in ('助動詞', '助詞'): return True
		return False

	# 自立語
	def is_independent_word(self):
		if self.hinshi1 == '記号': return False
		return not self.is_substantive_word()

	def write(self, logwrite):
		logwrite("%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%d" % 
				 (self.hyouki, self.nhyouki, 
				  self.hinshi1, self.hinshi2, self.hinshi3, self.hinshi4,
				  self.type1, self.type2, self.kihon,
				  self.kana, self.yomi, self.accent, self.output, self.sepflag))

def update_phonetic_symbols(mo):
	for p in range(0, len(mo.yomi)):
		# 点訳のてびき第3版 第2章 その1 1 5
		# ５、長音の書き表し方 (1), (2)
		# before: ああ,ああ,感動詞,*,*,*,アア,アー,1/2,アー,0
		# after:  ああ,ああ,感動詞,*,*,*,アア,アー,1/2,アア,0
		if mo.yomi[p] == 'ー' and mo.kana[p] in 'アイエ':
			mo.output = mo.output[:p] + mo.kana[p] + mo.output[p+1:]

		# 点訳のてびき第3版 第2章 その1 1 6
		# ６、「ジ　ズ　ジャ　ジュ　ジョ」と「ヂ　ヅ　ヂャ　ヂョ」の使い分け
		# before: 綴る,綴る,動詞,自立,*,*,ツヅル,ツズル,0/3,ツズル,0
		# after:  綴る,綴る,動詞,自立,*,*,ツヅル,ツズル,0/3,ツヅル,0
		if (mo.yomi[p] == 'ジ' and mo.kana[p] == 'ヂ') or (
			mo.yomi[p] == 'ズ' and mo.kana[p] == 'ヅ'):
			mo.output = mo.output[:p] + mo.kana[p] + mo.output[p+1:]

def mecab_to_morphs(mf):
	li = []
	if mf is None or mf.feature is None or mf.size is None: 
		return li
	for i in xrange(0, mf.size):
		s = string_at(mf.feature[i])
		if s:
			s = s.decode(CODE, 'ignore')
			ar = s.split(",")
			mo = MecabMorph()
			mo.hyouki = ar[0]
			mo.nhyouki = unicode_normalize(ar[0])
			mo.hinshi1 = ar[1]
			mo.hinshi2 = ar[2]
			if len(ar) > 3:
				mo.hinshi3 = ar[3]
				mo.hinshi4 = ar[4]
			if len(ar) > 5:
				mo.type1 = ar[5]
			if len(ar) > 6:
				mo.type2 = ar[6]
			if len(ar) > 7:
				mo.kihon = ar[7]
			if len(ar) > 9:
				mo.kana = ar[8]
				mo.yomi = ar[9]
				mo.accent = ar[10]
				if len(ar) > 12:
					# Mecab辞書の拡張フィールドの点訳表記があれば使用する
					mo.output = ar[12]
				else:
					mo.output = ar[9]
					update_phonetic_symbols(mo)
			mo.sepflag = False
			li.append(mo)
	return li

def replace_morphs(li, dic):
	new_li = []
	for mo in li:
		if mo.hyouki in dic.keys():
			new_morphs = dic[mo.hyouki]
			for i in new_morphs:
				m = copy.deepcopy(mo)
				m.hyouki = m.nhyouki = i[0] # に
				if i[3]: m.hinshi1 = i[3]
				if i[4]: m.hinshi2 = i[4]
				if i[5]: m.hinshi3 = i[5]
				m.output = m.kana = m.yomi = i[1] # ニ
				m.accent = i[2] # 0/1
				new_li.append(m)
		else:
			new_li.append(mo)
	return new_li

RE_KANSUJI = re.compile('^[一二三四五六七八九〇零十拾百千壱二参]+$')

# http://programminblog.blogspot.jp/2010/11/python.html
def kansuji2arabic(text):
	if not RE_KANSUJI.match(text):
		return None
	result = 0
	digit = 1
	numgroup = 1
	kanindex = len(text)
	while kanindex > 0:
		c = text[(kanindex - 1):kanindex]
		c1 = text[kanindex:(kanindex + 1)]
		kanindex -= 1
		if c in '〇零':
			digit *= 10
		elif c in '十拾':
			digit = 10
		elif c == '百':
			if digit == 10 and c1 and c1 in '十拾':
				result += digit * numgroup
			digit = 100
		elif c == '千':
			if (digit == 10 and c1 and c1 in '十拾') or \
					(digit == 100 and c1 and c1 in '百'):
				result += digit * numgroup
			digit = 1000
		else:
			if c in '壱一':
				result += digit * numgroup
			elif c in '二弐':
				result += 2 * digit * numgroup
			elif c in '三参':
				result += 3 * digit * numgroup
			elif c in '四':
				result += 4 * digit * numgroup
			elif c in '五':
				result += 5 * digit * numgroup
			elif c in '六':
				result += 6 * digit * numgroup
			elif c in '七':
				result += 7 * digit * numgroup
			elif c in '八':
				result += 8 * digit * numgroup
			elif c in '九':
				result += 9 * digit * numgroup
			digit *= 10
	if (digit == 10 and text[:1] in '十拾') or \
			(digit == 100 and text[:1] in '百') or \
			(digit == 1000 and text[:1] in '千'):
		result += digit * numgroup
	text = '%d' % result
	return text

def rewrite_number(li):
	new_li = []
	for mo in li:
		m = copy.deepcopy(mo)
		if m.hinshi2 != '固有名詞':
			ret = kansuji2arabic(m.hyouki)
			if ret:
				m.output = ret
		new_li.append(m)
	return new_li

def concatinate_morphs(li):
	mo = copy.deepcopy(li[0])
	s = ''
	y = ''
	for i in li:
		s += i.hyouki
		y += i.yomi
	mo.hyouki = mo.nhyouki = s
	mo.yomi = mo.kana = mo.output = y
	return mo

def replace_digit_morphs(li):
	# handle digit number kanji characters
	# input:
	#  十,名詞,数
	#  七,名詞,数
	# output:
	#  十七,名詞,数
	# input:
	#  二,名詞,数
	#  十,名詞,数
	#  五,名詞,数
	# output:
	#  二十五,名詞,数
	# input:
	#  三,名詞,数,*,*,*,*,三,サン,サン,0/2,C3
	#  兆,名詞,数,*,*,*,*,兆,チョウ,チョー,1/2,C3
	#  二,名詞,数,*,*,*,*,二,ニ,ニ,1/1,C3
	#  千,名詞,数,*,*,*,*,千,セン,セン,1/2,C3
	#  四,名詞,数,*,*,*,*,四,ヨン,ヨン,1/2,C1
	#  百,名詞,数,*,*,*,*,百,ヒャク,ヒャク,2/2,C3
	#  万,名詞,数,*,*,*,*,万,マン,マン,1/2,C3
	# output:
	#  三,三,名詞,数,*,*,サン,サン,,サン,0
	#  兆,兆,名詞,数,*,*,チョー,チョー,,チョー,0
	#  二千四百,二千四百,名詞,数,*,*,ニセンヨンヒャク,ニセンヨンヒャク,,ニセンヨンヒャク,0
	#  万,万,名詞,数,*,*,マン,マン,,マン,0
	# (correct: 3チョー 2400マン)
	new_li = []
	num_morphs = []
	for mo in li:
		if mo.hinshi2 == '数' and mo.hyouki == '，':
			# カンマ
			m = copy.deepcopy(mo)
			m.yomi = m.output = ','
			num_morphs.append(m)
		elif mo.hinshi2 == '数' and not mo.output.isdigit() and \
				not mo.hyouki in ('・', '万', '億', '兆', '京', '．'):
			# 漢数字の結合
			num_morphs.append(mo)
		elif mo.hinshi2 == '数' and mo.hyouki in '０１２３４５６７８９':
			# 算用数字の結合
			m = copy.deepcopy(mo)
			y = unicode_normalize(m.hyouki)
			m.output = m.hyouki = m.nhyouki = m.yomi = y
			num_morphs.append(m)
		else:
			if num_morphs:
				new_li.append(concatinate_morphs(num_morphs))
				num_morphs = []
			new_li.append(mo)
	if num_morphs:
		new_li.append(concatinate_morphs(num_morphs))
	return new_li

RE_ALPHA = re.compile('^[A-Za-z]+$')

def is_alpha(s):
	return RE_ALPHA.match(s)

RE_ASCII_SYMBOLS = re.compile('^[\,\.\:\;\!\?\@\#\\\$\%\&\*\|\+\-\/\=\<\>\"\'\^\`\_\~]+$')

def replace_alphabet_morphs(li):
	# アルファベットまたは記号だけで表記されている語を結合する
	# 情報処理点字の部分文字列になる記号を前後にまとめる
	# input:
	#  Ｂ,B,記号,アルファベット,*,*,ビー,ビー,1/2,B
	#  ａｓｉ,asi,名詞,一般,*,*,アシー,アシー,0/3,asi
	#  ｃ,c,記号,アルファベット,*,*,シー,シー,1/2,c
	# output:
	#  Ｂａｓｉｃ,Basic,名詞,アルファベット,*,*,ビーアシーシー,ビーアシーシー,1/2,Basic
	new_li = []
	alp_morphs = []
	for pos in range(len(li)):
		mo = li[pos]
		if pos < len(li) - 1:
			next_mo = li[pos + 1]
		else:
			next_mo = None
		if is_alpha(mo.nhyouki):
			alp_morphs.append(mo)
		elif mo.nhyouki in r',+@/#$%&*;<':
			alp_morphs.append(mo)
		elif mo.nhyouki == '\\':
			alp_morphs.append(mo)
		elif mo.nhyouki[0] in r',+@/#$%&*;' and \
				RE_ASCII_SYMBOLS.match(mo.nhyouki):
			alp_morphs.append(mo)
		elif alp_morphs and mo.nhyouki in ',.' and \
				((next_mo and next_mo.nhyouki == ' ') or \
					 (next_mo and next_mo.hinshi1 in ('助詞', '助動詞')) or \
					 (not next_mo)):
			alp_morphs.append(mo)
		elif alp_morphs and mo.nhyouki == ' ' and \
				next_mo and is_alpha(next_mo.nhyouki):
			alp_morphs.append(mo)
		elif alp_morphs and mo.nhyouki.isdigit():
			alp_morphs.append(mo)
		elif alp_morphs and mo.nhyouki in ',.:;!?@#\\$%&*|+-/=<>"\'^`_~{}[]':
			alp_morphs.append(mo)
		else:
			if alp_morphs:
				m = concatinate_morphs(alp_morphs)
				m.hinshi1 = '名詞'
				m.hinshi2 = 'アルファベット'
				m.nhyouki = m.output = unicode_normalize(m.nhyouki)
				new_li.append(m)
				alp_morphs = []
			new_li.append(mo)
	if alp_morphs:
		m = concatinate_morphs(alp_morphs)
		m.hinshi1 = '名詞'
		m.hinshi2 = 'アルファベット'
		m.nhyouki = m.output = unicode_normalize(m.nhyouki)
		new_li.append(m)
	return new_li

# 日付の和語読み処理
# すでに output 属性に半角数字が格納されている前提

# 後続する '日' と形態素を結合する
WAGO_DIC = {
	'1': 'ツイタチ', 
	'2': 'フツカ',
	'3': 'ミッカ',
	'4': 'ヨッカ',
	'5': 'イツカ',
	'6': 'ムイカ',
	'7': 'ナノカ',
	'8': 'ヨーカ',
	'9': 'ココノカ',
	'10': 'トオカ',
	'20': 'ハツカ',
}

def fix_japanese_date_morphs(li):
	new_li = []
	for i in xrange(0, len(li)):
		prev_mo = li[i-1] if i-1>=0 else None
		mo = li[i]
		if mo.hyouki == '日' and mo.hinshi3 == '助数詞' and prev_mo is not None:
			if prev_mo.hyouki in ('14', '24', '十四', '一四', '二四', '二十四'):
				li[i].output = 'カ'
				new_li.append(li[i])
			elif prev_mo.output in WAGO_DIC:
				m = copy.deepcopy(mo)
				m.output = WAGO_DIC[prev_mo.output]
				m.hyouki = m.nhyouki = m.kana = m.yomi = m.output
				m.hinshi2 = '日付'
				m.hinshi3 = '*'
				# FIXME: m.accent
				new_li.pop()
				new_li.append(m)
			else:
				new_li.append(li[i])
		else:
			new_li.append(li[i])
	return new_li

def should_separate(prev2_mo, prev_mo, mo, next_mo):
	if mo.hyouki == 'ー': return False
	if prev_mo.hyouki == 'ー': return False
	if mo.hyouki in 'ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮヵヶ': return False

	# )( -> あける
	# )陽が -> あける
	# '02 -> あけない
	if prev_mo.hinshi2 == '括弧閉' and prev_mo.nhyouki != "’":
		if mo.hinshi2 == '括弧開': return True
		if mo.hinshi1 == '名詞': return True

	# 東京/都 千代田/区
	if prev_mo.hinshi2 == '接尾' and prev_mo.hinshi3 == '地域' and \
			mo.hinshi2 == '固有名詞' and mo.hinshi3 == '地域':
		return True
	# 東京/都 交通/局
	if prev_mo.hinshi2 == '接尾' and prev_mo.hinshi3 == '地域' and \
			mo.hinshi1 == '名詞' and mo.hinshi2 == '一般':
		return True
	# 永田町 １
	if prev_mo.hinshi2 == '固有名詞' and prev_mo.hinshi3 == '地域' and \
			mo.hinshi2 == '数':
		return True

	# 晴れ/所に より
	if prev_mo.hinshi1 == '名詞' and mo.hyouki == '所により':
		return True

	# 一時/雨
	if prev_mo.hyouki == '一時' and mo.hyouki == '雨':
		return True

	# 数字の前のマスアケ
	if prev_mo.nhyouki in ('零下', '西暦', 'ボーイング', 'ベスト', 'ルイ', '先', '振替', 'No.', '一人当り') \
			and mo.output.isdigit():
		return True

	# 1月/1日
	if prev_mo.nhyouki[0].isdigit() and prev_mo.nhyouki[-1] == '月' and mo.output.isdigit():
		return True
	# 0/4月 -> 04月
	if prev_mo.output.isdigit() and mo.nhyouki[0].isdigit():
		return False

	# アラビア数字のあとに単位がきたら続ける
	# 三十,三十,名詞,数,*,*,30,30,1/4,30,1
	# センチメートル,センチメートル,名詞,一般,*,*,センチメートル,センチメートル,4/7,センチメートル,0
	if prev_mo.output.isdigit():
		if mo.hinshi3 == '助数詞': return False
		if mo.hyouki == 'センチメートル': return False
		if mo.nhyouki == '#': return False

	# 数%
	if prev_mo.hyouki == '数' and prev_mo.yomi == 'スー' and mo.hyouki == '％':
		return False

	# 三,三,名詞,数,*,*,サン,サン,0/2,3,0
	# 兆,兆,名詞,数,*,*,チョウ,チョー,1/2,チョー,1
	# 二千四百,二千四百,名詞,数,*,*,ニセンヨンヒャク,ニセンヨンヒャク,1/1,2400,0
	# 万,万,名詞,数,*,*,マン,マン,1/2,マン,0
	if prev_mo.hyouki in ('億', '兆', '京') and mo.output.isdigit():
		return True

	# ち,ち,名詞,一般,*,*,チ,チ,0/1,チ,0
	# ゅうりっぷ,ゅうりっぷ,名詞,一般,*,*,,,,ュウリップ,0
	if mo.hyouki[0] in 'ぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮヵヶ': return False

	# 外国語引用符、マスアケ、助詞、助動詞
	if prev_mo.output and prev_mo.output.endswith('⠴') and mo.hinshi1 in ('助詞', '助動詞'): return True

	if prev_mo.hinshi1 == '名詞' and prev_mo.hinshi2 == '接尾':
		# 助数詞のあとにアラビア数字が来たらマスアケ
		# case 1:
		#  零,零,名詞,数,*,*,0,0,1/2,0,0
		#  時,時,名詞,接尾,助数詞,*,ジ,ジ,1/1,ジ,1
		#  十五,十五,名詞,数,*,*,15,15,1/3,15,0
		#  分,分,名詞,接尾,助数詞,*,フン,フン,1/2,フン,0
		# case 2:
		#  一,一,名詞,数,*,*,イチ,イチ,2/2,1,0
		#  人,人,名詞,接尾,助数詞,*,ニン,ニン,1/2,ニン,0
		#  当り,当り,名詞,接尾,一般,*,アタリ,アタリ,1/3,アタリ,1
		#  １,1,名詞,数,*,*,イチ,イチ,2/2,1,0
		#  ０,0,名詞,数,*,*,ゼロ,ゼロ,1/2,0,0
		#  個,個,名詞,接尾,助数詞,*,コ,コ,1/1,コ,0
		if mo.output.isdigit(): return True
		if mo.hinshi1 == '動詞' and mo.hinshi2 == '非自立': return False

	# アルファベットの後の助詞、助動詞
	# ＣＤ,CD,名詞,一般,*,*,シーディー,シーディー,3/4,シーディー,0
	# を,を,助詞,格助詞,一般,*,ヲ,ヲ,0/1,ヲ,0
	if is_alpha(prev_mo.nhyouki) and mo.hinshi1 in ('助詞', '助動詞'):
		return True

	# ピリオドの後の助詞
	if prev_mo.nhyouki.endswith('.') and mo.hinshi1 == '助詞':
		return True

	# ナンバーマークの後の助詞
	if prev_mo.nhyouki == '#' and mo.hinshi1 == '助詞':
		return True

	# カナ名詞の後のアルファベット名詞
	if prev_mo.hinshi1 == '名詞' and is_alpha(mo.nhyouki):
		return False

	# (あける)
	# 映画,映画,名詞,一般,*,*,エイガ,エイガ,0/3,エイガ,1
	# 「,「,記号,括弧開,*,*,「,「,*/*,「,0
	# (あけない)
	# 機関,名詞,一般,*,*,*,*,機関,キカン,キカン,1/3,C1
	# （,記号,括弧開,*,*,*,*,（,（,（,*/*,*
	if prev_mo.hinshi1 == '名詞' and mo.hinshi2 == '括弧開' and mo.nhyouki != '(': return True

	# 間違い,間違い,名詞,ナイ形容詞語幹,*,*,マチガイ,マチガイ,3/4,マチガイ,1
	# なし,なし,助動詞,*,*,*,ナシ,ナシ,0/2,ナシ,0
	#
	# 味気,味気,名詞,ナイ形容詞語幹,*,*,アジケ,アジケ,0/3,アジケ,0
	# ない,ない,助動詞,*,*,*,ナイ,ナイ,1/2,ナイ,0
	#
	# 良く,形容詞,自立,*,*,形容詞・アウオ段,連用テ接続,良い,ヨク,ヨク,1/2,C3
	# ない,助動詞,*,*,*,特殊・ナイ,基本形,ない,ナイ,ナイ,1/2,動詞%F3@0/形容詞%F2@1
	#
	# で,で,助動詞,*,*,*,デ,デ,1/1,デ,0
	# は,は,助詞,係助詞,*,*,ハ,ワ,0/1,ワ,1
	# なく,なく,助動詞,*,*,*,ナク,ナク,0/2,ナク,1
	#
	# 「問題ない」の「ない」は「点訳のてびき」では形容詞だがMecabでは助動詞
	if mo.hinshi1 == '形容詞' and mo.kihon in ('ない', '無い'):
		# 形容詞「ない」は区切る
		# ただし前の語と複合している場合は前に続ける
		if prev_mo.kihon in ('隈', '心置き', '満遍'):
			return False
		return True
	if mo.hinshi1 == '助動詞' and mo.kihon in ('ない', '無い'):
		if prev_mo.hinshi1 == '助詞' and prev_mo.kihon == 'は':
			return True
		if prev_mo.hinshi1 == '形容詞' and prev_mo.kihon == '良い':
			return True
		if prev_mo.hinshi1 == '名詞' and prev_mo.hinshi2 == 'ナイ形容詞語幹' and \
				prev_mo.kihon in ('問題', '間違い'):
			return True
		if prev_mo.hinshi2 == '副助詞': # じゃない
			return True
		if prev_mo.hinshi1 == '動詞' and prev_mo.hinshi2 == '非自立' and \
				prev_mo.kihon in ('てる'): # てない
			return True
		if prev_mo.hinshi1 == '助動詞' and \
				prev_mo.kihon in ('だ'): # でない
			return True
		return False

	# お,黙り,なさい
	# 「お」がついて名詞化した語に「なさい・なさる」が続く場合は区切ってよい
	if prev2_mo and prev2_mo.hinshi1 == '接頭詞' and prev2_mo.hyouki == 'お' and \
			prev_mo.hinshi1 == '動詞' and prev_mo.type2 == '連用形' and \
			mo.kihon == 'なさる':
		return True

	# 労,せ,ず
	if prev_mo.hinshi1 == '名詞' and mo.hyouki == 'せ' and mo.kihon == 'する':
		return False

	# 不幸,に,し,て
	# 今,に,し,て
	# 居,ながら,に,し,て
	# 労,せ,ず,し,て
	# 若く,し,て
	# 私,を,し,て
	# 「して」が文語的表現の助詞である場合は前に続けて書く
	if mo.hyouki == 'し' and mo.kihon == 'する':
		if prev_mo.hyouki == 'ず' and prev_mo.hinshi1 == '助動詞':
			return False
		if prev_mo.hinshi1 == '形容詞' and prev_mo.type2 == '連用テ接続':
			return False
		if prev_mo.hinshi2 == '接続助詞':
			return False
		if prev_mo.type1 == '文語・ベシ':
			return False
		if next_mo and next_mo.hyouki == 'て':
			if prev_mo.hyouki == 'に' and prev_mo.hinshi1 == '助詞':
				return False
			if prev2_mo and prev2_mo.hyouki == '私' and prev_mo.hyouki == 'を':
				return False

	# 「・・ですこと」の「こと」は接尾語なので前に続ける
	if prev_mo.hyouki == 'です' and mo.hyouki == 'こと':
		return False

	# 「この程」「この度」
	# 「そのくせ」
	# 後ろの語と結びついて1語になっている場合は続ける
	if prev_mo.hyouki == 'この' and mo.hyouki in ('程', '度'):
		return False
	if prev_mo.hyouki == 'その' and mo.hyouki in ('くせ', 'うち', 'まま'):
		return False
	if prev_mo.hyouki == 'わが' and mo.hyouki == 'まま':
		return False

	if prev_mo.hinshi1 == '名詞' and mo.hinshi1 == '名詞':
		if mo.hinshi2 == '数': return False
		# 人名
		if prev_mo.hinshi4 in ('姓', '名') and mo.hinshi2 == '接尾' and mo.hinshi3 == '人名': return True
		# 複合名詞内部の2拍以下は切らない
		if not prev_mo.hinshi2 in ('数', 'アルファベット') and not mo.hinshi2 in ('数', 'アルファベット'):
			if len(prev_mo.yomi) <= 2 and len(mo.yomi) >= 3: return False
			if len(prev_mo.yomi) >= 3 and len(mo.yomi) <= 2: return False
		if mo.hinshi2 != '接尾': return True

	if prev_mo.hinshi1 == '形容詞' and mo.hyouki == 'ん': return False # いいんですけど

	if prev_mo.hinshi1 == '動詞' and prev_mo.hyouki == '見': return False # 見/まごう
	if prev_mo.hinshi1 == '動詞' and prev_mo.hinshi2 == '自立':
		if mo.hyouki == 'および': return True
		if mo.hinshi1 == '動詞' and mo.hinshi2 == '非自立': return False

	# その,その,連体詞,*,*,*,ソノ,ソノ,0/2,ソノ,1
	# よう,よう,名詞,非自立,助動詞語幹,*,ヨウ,ヨー,1/2,ヨー,0
	if prev_mo.hinshi1 == '連体詞' and mo.hinshi3 == '助動詞語幹': return False

	if prev_mo.hinshi1 == '接頭詞' and prev_mo.hyouki == '超' and mo.hinshi1 == '名詞': return True
	
	# お兄さん, お姉さん
	if prev_mo.hinshi1 == '接頭詞' and prev_mo.hyouki == 'お': return False
	# 新/東京/名所
	if prev_mo.hinshi1 == '接頭詞' and prev_mo.hinshi2 == '名詞接続' and \
			mo.hinshi1 == '名詞' and mo.hinshi2 == '固有名詞':
		return True
	if prev_mo.hinshi1 == '接頭詞' and mo.hinshi1 == '名詞': return False

	if prev_mo.hinshi1 == '助動詞' and prev_mo.hyouki == 'で' and mo.hinshi1 == '助動詞': return True

	if prev_mo.hinshi1 == '助詞' and mo.hyouki == 'よう': return False # のように
	if prev_mo.hinshi1 == '助詞' and mo.hinshi1 == '接頭詞': return True

	if prev_mo.is_substantive_word() and mo.is_independent_word(): return True
	if prev_mo.is_independent_word() and mo.is_independent_word(): return True
	return False

def morphs_to_string(li, inbuf, logwrite):
	outbuf = ''
	inpos2 = []
	p = 0
	for i in range(0, len(li)):
		if not li[i].output:
			continue
		out = li[i].output
		outlen = len(out)
		outbuf += out
		hyolen = len(li[i].hyouki)
		if hyolen == outlen:
			inpos2.extend(range(p, p + outlen))
		elif out[:2] == '⠠⠦' and out[-2:] == '⠠⠴':
			# 情報処理用点字の内側
			c = outlen - 4
			inpos2.extend([p] * 2)
			inpos2.extend(range(p, p + c))
			inpos2.extend([p + c - 1] * 2)
		elif out[:1] == '⠦' and out[-1:] == '⠴':
			# 外国語引用符の内側
			c = outlen - 2
			inpos2.extend([p])
			inpos2.extend(range(p, p + c))
			inpos2.extend([p + c - 1])
		else:
			# 表記と出力の文字数が変化する場合
			for x in range(outlen):
				inpos2.append(p + int(float(x) * hyolen / outlen))
		p += hyolen
		if li[i].sepflag:
			outbuf += ' '
			if p > 0:
				inpos2.append(p - 1) # マスアケは直前の文字に対応
			else:
				inpos2.append(p)
	# rstrip with inpos2
	if inbuf[-1] != ' ':
		while outbuf[-1:] == ' ':
			outbuf = outbuf[:-1]
			inpos2.pop()
	return (outbuf, inpos2)

RE_MB_ALPHA_NUM_SPACE = re.compile('^[0-9A-Za-z ０-９Ａ-Ｚａ-ｚ　]+$')
RE_ASCII_CHARS = re.compile('^[A-Za-z0-9\.\,\-\+\:\/\~\?\&\%\#\*\$\; ]+$')
RE_INFOMATION = re.compile('^[A-Za-z0-9\+\@\/\#\$\%\&\*\;\.\<\>\-\_\{\}\[\] ]+$')
RE_GAIJI = re.compile('^[A-Za-z][A-Za-z0-9\,\.\+\- ]+$')
RE_KATAKANA = re.compile('^[ァ-ヾ]+$')
RE_HIRAGANA = re.compile('^[ぁ-ゞ]+$')

def japanese_braille_separate(inbuf, logwrite):
	text = inbuf
	if RE_MB_ALPHA_NUM_SPACE.match(text):
		outbuf = unicode_normalize(text)
		inpos2 = range(len(outbuf))
		return (outbuf, inpos2)

	# 'あ゛ー' Unicode 正規化されて空白が入るので事前に補正する
	text = text.replace('あ゛', 'あ')
	text = text.replace('ヱ゛', 'ヴェ')
	text = text.replace('ヲ゛', 'ヴォ')
	text = text.replace('ワ゛', 'ヴァ')

	# 'ふにゃ～'
	text = text.replace('ゃ～', 'ゃー')

	text = Mecab_text2mecab(text)
	mf = MecabFeatures()
	Mecab_analysis(text, mf)
	Mecab_correctFeatures(mf)
	Mecab_print(mf, logwrite, output_header = False)
	li = mecab_to_morphs(mf)
	mf = None

	for mo in li:
		if mo.hinshi1 == '空白':
			mo.output = ' '
		elif mo.hinshi2 == '数' and mo.nhyouki.isdigit():
			# digit numbers (not kanji characters)
			mo.output = mo.nhyouki

	li = replace_morphs(li, CONNECTED_MORPHS)
	li = replace_digit_morphs(li)
	li = rewrite_number(li)

	# before: う,う,助動詞,*,*,*,ウ,ウ,0/1,ウ,0
	# after:  う,う,助動詞,*,*,*,ウ,ウ,0/1,ー,0
	for mo in li:
		if mo.hyouki == 'う' and mo.hinshi1 == '助動詞':
			mo.output = 'ー'

	# before: ａ,a,記号,アルファベット,*,*,エイ,エイ,1/2,エイ,0
	# after:  ａ,a,記号,アルファベット,*,*,エイ,エイ,1/2,a,0
	for mo in li:
		if mo.hinshi2 == 'アルファベット':
			mo.output = mo.nhyouki

	li = replace_alphabet_morphs(li)

	for mo in li:
		if mo.hyouki == '〝':
			mo.hinshi1 = '記号'
			mo.hinshi2 = '括弧開'
		if mo.hyouki == '〟':
			mo.hinshi1 = '記号'
			mo.hinshi2 = '括弧閉'

	for mo in li:
		if mo.hinshi2 in ('括弧開', '括弧閉'):
			mo.output = mo.nhyouki

	# before: 　, ,記号,空白,*,*,　,　,*/*,　,0
	# after:  　, ,記号,空白,*,*,　,　,*/*, ,0
	for mo in li:
		if mo.hyouki == '　': # full shape space
			mo.output = ' '

	# 数字の前の全角アポストロフィを半角にする
	# before:
	# ’,’,記号,括弧閉,*,*,’,’,*/*,’,0
	# ０,0,名詞,数,*,*,ゼロ,ゼロ,1/2,0,0
	# after:
	# ’,’,記号,括弧閉,*,*,’,’,*/*,',0
	# ０,0,名詞,数,*,*,ゼロ,ゼロ,1/2,0,0
	for pos in range(0, len(li) - 1):
		if li[pos].hyouki == '’' and li[pos+1].hinshi2 == '数':
			li[pos].output = "'"

	# 算用数字ではさまれた読点と中点を数符にする
	# before:
	# 二,二,名詞,数,*,*,2,2,1/2,2,0
	# 、,、,記号,読点,*,*,、,、,*/*,、,0
	# 三,三,名詞,数,*,*,3,3,1/2,3,0
	# after:
	# 二,二,名詞,数,*,*,2,2,1/2,2,0
	# 、,、,記号,読点,*,*,、,、,*/*,⠼,0
	# 三,三,名詞,数,*,*,3,3,1/2,3,0
	for pos in range(1, len(li) - 1):
		if li[pos-1].output.isdigit() and \
				li[pos].hyouki in ('、', '・') and \
				li[pos+1].output.isdigit():
			li[pos].output = '⠼'

	# 記号を Unicode 正規化
	for mo in li:
		if mo.hinshi1 == '記号' and mo.hinshi2 == '一般':
			mo.output = mo.nhyouki
		if mo.hyouki == '．' and mo.hinshi1 == '名詞' and mo.hinshi2 == '数':
			mo.output = '.'
		if mo.hyouki == '，' and mo.hinshi1 == '名詞' and mo.hinshi2 == '数':
			mo.output = ','
		if mo.hinshi1 == '記号' and mo.hinshi2 == '句点' and mo.nhyouki == '.':
			mo.output = '.'
		if mo.hinshi1 == '記号' and mo.hinshi2 == '読点' and mo.nhyouki == ',':
			mo.output = ','

	# before: ａｂ,ab,名詞,一般,*,*,アブ,アブ,1/2,アブ,0
	# after:  ａｂ,ab,名詞,一般,*,*,アブ,アブ,1/2,ab,0
	# before: Ｎｏ．,No.,接頭詞,数接続,*,*,ナンバー,ナンバー,1/4,ナンバー,0
	# after:  Ｎｏ．,No.,接頭詞,数接続,*,*,ナンバー,ナンバー,1/4,No.,0
	for mo in li:
		if RE_ASCII_CHARS.match(mo.nhyouki):
			mo.output = mo.nhyouki

	# before: ヒロイノ,ヒロイノ,名詞,一般,*,*,,,,,0
	# after:  ヒロイノ,ヒロイノ,名詞,一般,*,*,,,,ヒロイノ,0
	# before: ィ,ィ,名詞,一般,*,*,,,,,0
	# after:  ィ,ィ,名詞,一般,*,*,,,,ィ,0
	# before: ぁ,ぁ,名詞,一般,*,*,,,,,0
	# after:  ぁ,ぁ,名詞,一般,*,*,,,,ァ,0
	for mo in li:
		if not mo.output and mo.nhyouki != 'ー':
			if RE_KATAKANA.match(mo.nhyouki):
				mo.output = mo.nhyouki
			elif RE_HIRAGANA.match(mo.nhyouki):
				mo.output = ''.join([unichr(ord(c) + 0x60) for c in mo.nhyouki])

	# 単語が小文字カタカナのみであれば修正
	# 表記は修正せず should_separate() で小文字として判定される
	for mo in li:
		if mo.output == 'ァ': mo.output = 'ア'
		if mo.output == 'ィ': mo.output = 'イ'
		if mo.output == 'ゥ': mo.output = 'ウ'
		if mo.output == 'ェ': mo.output = 'エ'
		if mo.output == 'ォ': mo.output = 'オ'
		if mo.output == 'ッ': mo.output = 'ツ'
		if mo.output == 'ャ': mo.output = 'ヤ'
		if mo.output == 'ュ': mo.output = 'ユ'
		if mo.output == 'ョ': mo.output = 'ヨ'
		if mo.output == 'ヮ': mo.output = 'ワ'
		if mo.output == 'ヵ': mo.output = 'カ'
		if mo.output == 'ヶ': mo.output = 'ケ'

	for mo in li:
		# 情報処理点字の開始記号と終了記号
		if RE_INFOMATION.match(mo.nhyouki) and \
				('@' in mo.nhyouki) or ('://' in mo.nhyouki) or ('\\' in mo.nhyouki):
			mo.output = '⠠⠦' + mo.nhyouki + '⠠⠴'
		# 外国語引用符
		# 空白をはさまない1単語は外国語引用符ではなく外字符で
		elif RE_GAIJI.match(mo.nhyouki) and \
				(' ' in mo.nhyouki) or ('.' in mo.nhyouki and len(mo.nhyouki) > 3):
			mo.output = '⠦' + mo.nhyouki + '⠴'

	for mo in li:
		# 情報処理点字でも外国語引用符でもなく output が & を含む場合は前後をあける
		if not mo.output.startswith('⠠⠦') and not mo.output.startswith('⠦'):
			# &
			if mo.output == '&':
				continue
			# &xx
			elif mo.output.startswith('&'):
				mo.output = mo.output.replace('&', '& ')
			# xx&
			elif mo.output.endswith('&'):
				mo.output = mo.output.replace('&', ' &')
			# xx&xx
			else:
				mo.output = mo.output.replace('&', ' & ')
	
	# 日付の和語読み処理
	li = fix_japanese_date_morphs(li)

	# 分かち書き判定
	for i in xrange(1, len(li)):
		prev2_mo = li[i-2] if i-2 >= 0 else None
		prev_mo = li[i-1]
		next_mo = li[i+1] if i+1 < len(li) else None
		li[i-1].sepflag = should_separate(prev2_mo, prev_mo, li[i], next_mo)

	for mo in li:
		mo.write(logwrite)
	logwrite('')

	outbuf, inpos2 = morphs_to_string(li, inbuf, logwrite)
	return (outbuf, inpos2)

mecab_initialized = False

def initialize(jtalk_dir=None, logwrite=_logwrite):
	global mecab_initialized
	if jtalk_dir:
		Mecab_initialize(logwrite, jtalk_dir)
	else:
		Mecab_initialize(logwrite)
	if logwrite: logwrite("initialize() done.")
	mecab_initialized = True

def terminate():
	global _logwrite
	if _logwrite: _logwrite("terminate() done.")
	global mecab_initialized
	mecab_initialized = False

def translateWithInPos2(inbuf, logwrite=_logwrite):
	if not mecab_initialized:
		initialize()
	outbuf, inpos2 = japanese_braille_separate(inbuf, logwrite)
	result, inpos1 = translator1.translateWithInPos(outbuf)
	result = result.replace('□', ' ')
	return (outbuf, result, inpos1, inpos2)

# for brailleViewer
def getReadingAndBraille(text, logwrite=_logwrite):
	return translateWithInPos2(text, logwrite=logwrite)[0:2]

# returns '\u2801\u2802\u2803\u2804\u2805\u2806\u2807'
def japaneseToUnicodeBraille(text, logwrite=_logwrite):
	return translateWithInPos2(text, logwrite=logwrite)[0]

def makeOutPos(inPos, inlen, outlen):
	# make outPos
	outPos = [-1] * inlen
	for p in range(outlen):
		if inPos[p] < len(outPos) and (outPos[ inPos[p] ] == -1 or inPos[p] == 0):
			outPos[ inPos[p] ] = p
	# fill skipped outPos
	prev = 0
	for p in range(inlen):
		if outPos[p] == -1:
			outPos[p] = prev
		else:
			prev = outPos[p]
	return outPos

def mergePositionMap(inpos1, inpos2, outlen, inlen):
	inPos = [0] * outlen
	for p in range(outlen):
		inPos[p] = inpos2[ inpos1[p] ]
	outPos = makeOutPos(inPos, inlen, outlen)
	return inPos, outPos

# louis-compatible method
# tableList, typeform are not supported.
# mode=dotsIO is default.
def translate(inbuf, cursorPos=0, logwrite=_logwrite, unicodeIO=False):
	"""Translate a string of characters, providing position information.
	@param inbuf: The string to translate.
	@type inbuf: str
	@param cursorPos: The position of the cursor in inbuf.
	@type cursorPos: int
	@return: A tuple of:
		the translated string,
		a list of input positions for each position in the output,
		a list of output positions for each position in the input, and
		the position of the cursor in the output.
	@rtype: (str, list of int, list of int, int)
	@raise RuntimeError: If a complete translation could not be done.
	"""
	sp, outbuf, inpos1, inpos2 = translateWithInPos2(inbuf, logwrite=logwrite)
	if not unicodeIO:
		pat = outbuf.replace(' ', '\u2800')
		outbuf = ''.join([unichr((ord(c) - 0x2800) + 0x8000) for c in pat])
	inPos, outPos = mergePositionMap(inpos1, inpos2, len(outbuf), len(inbuf))
	cursorPos = outPos[cursorPos]
	return (outbuf, inPos, outPos, cursorPos)
