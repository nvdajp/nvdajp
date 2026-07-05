# coding: UTF-8
# translator2.py (Japanese Braille translator Phase 2)
# Copyright (C) 2012-2026 Takuya Nishimoto
# License: BSD 3-Clause. See LICENSE.
#
# Originally developed as part of NVDA Japanese (nvdajp); relicensed
# from GPL to BSD 3-Clause by the copyright holder for libkuraji.
#
# This stage performs word separation (masuake) using morphological
# analysis. The analyzer is injected via initialize(); the reference
# configuration uses MeCab with the JTalk extended dictionary (see
# nvdajp's mecabAnalyzer.py). The feature-line format, including the
# optional braille-notation field, is part of that dictionary contract.

import re
from typing import Callable

from .unicodeutil import unicode_normalize, nfkc_normalize_with_map
from . import kana as translator1


def _noop_log(s):
	pass


_logwrite = _noop_log

CONNECTED_MORPHS = {
	"について": [
		["に", "ニ", "0/1", None, None, "*"],
		["ついて", "ツイテ", "1/3", "動詞", "*", "*"],
	],
	"により": [
		["に", "ニ", "0/1", None, None, "*"],
		["より", "ヨリ", "0/2", "動詞", "*", "*"],
	],
	"による": [
		["に", "ニ", "0/1", None, None, "*"],
		["よる", "ヨル", "0/2", "動詞", "*", "*"],
	],
	"において": [
		["に", "ニ", "0/1", None, None, "*"],
		["おいて", "オイテ", "0/3", "動詞", "*", "*"],
	],
	"における": [
		["に", "ニ", "0/1", None, None, "*"],
		["おける", "オケル", "0/3", "動詞", "*", "*"],
	],
	"によって": [
		["に", "ニ", "0/1", None, None, "*"],
		["よって", "ヨッテ", "0/3", "動詞", "*", "*"],
	],
	"にとって": [
		["に", "ニ", "0/1", None, None, "*"],
		["とって", "トッテ", "0/3", "動詞", "*", "*"],
	],
	"に対して": [
		["に", "ニ", "0/1", None, None, "*"],
		["対して", "タイシテ", "1/4", "動詞", "*", "*"],
	],
	"に関して": [
		["に", "ニ", "0/1", None, None, "*"],
		["関して", "カンシテ", "1/4", "動詞", "*", "*"],
	],
	"につき": [
		["に", "ニ", "0/1", None, None, "*"],
		["つき", "ツキ", "1/2", "動詞", "*", "*"],
	],
	"という": [
		["と", "ト", "0/1", None, None, "*"],
		["いう", "イウ", "0/2", "動詞", "*", "*"],
	],
	"どうして": [
		["どう", "ドー", "0/2", None, None, "*"],
		["して", "シテ", "0/2", "動詞", "*", "*"],
	],
	"として": [
		["と", "ト", "1/1", None, None, "*"],
		["して", "シテ", "0/2", "動詞", "*", "*"],
	],
	"なくなる": [
		["なく", "ナク", "2/2", None, None, None],
		["なる", "ナル", "1/2", "動詞", "自立", None],
	],
	"（日）": [
		["（", "(", "*/*", "記号", "括弧開", "*"],
		["日", "ニチ", "1/2", "名詞", "一般", None],
		["）", ")", "*/*", "記号", "括弧閉", "*"],
	],
	"（月）": [
		["（", "(", "*/*", "記号", "括弧開", "*"],
		["月", "ゲツ", "1/2", "名詞", "一般", None],
		["）", ")", "*/*", "記号", "括弧閉", "*"],
	],
	"（火）": [
		["（", "(", "*/*", "記号", "括弧開", "*"],
		["火", "カ", "1/1", "名詞", "一般", None],
		["）", ")", "*/*", "記号", "括弧閉", "*"],
	],
	"（水）": [
		["（", "(", "*/*", "記号", "括弧開", "*"],
		["水", "スイ", "1/2", "名詞", "一般", None],
		["）", ")", "*/*", "記号", "括弧閉", "*"],
	],
	"（木）": [
		["（", "(", "*/*", "記号", "括弧開", "*"],
		["木", "モク", "1/2", "名詞", "一般", None],
		["）", ")", "*/*", "記号", "括弧閉", "*"],
	],
}


class MecabMorph(object):
	__slots__ = (
		"hyouki",
		"nhyouki",
		"hinshi1",
		"hinshi2",
		"hinshi3",
		"hinshi4",
		"type1",
		"type2",
		"kihon",
		"kana",
		"yomi",
		"accent",
		"output",
		"sepflag",
	)

	def __init__(self):
		self.hyouki = ""  # 表記
		self.nhyouki = ""  # Unicode 正規化された表記
		self.hinshi1 = ""
		self.hinshi2 = ""
		self.hinshi3 = ""
		self.hinshi4 = ""
		self.type1 = ""
		self.type2 = ""
		self.kihon = ""
		self.kana = ""
		self.yomi = ""
		self.accent = ""
		self.output = ""
		self.sepflag = False  # この後でマスアケをするか？

	def clone(self) -> "MecabMorph":
		# all slots hold immutable values, so attribute copy is enough
		new = MecabMorph.__new__(MecabMorph)
		for name in MecabMorph.__slots__:
			setattr(new, name, getattr(self, name))
		return new

	# 付属語
	def is_substantive_word(self) -> bool:
		if self.hinshi1 == "記号":
			return False
		if self.hinshi2 == "接頭":
			return True
		if self.hinshi2 == "接尾":
			return True
		if self.hinshi1 == "助動詞" and self.hyouki == "ない":
			return False
		if self.hinshi1 == "名詞" and self.hyouki == "の":
			return True
		if self.hinshi1 == "形容詞" and self.hyouki == "なく":
			return True
		if self.hinshi1 in ("助動詞", "助詞"):
			return True
		return False

	# 自立語
	def is_independent_word(self) -> bool:
		if self.hinshi1 == "記号":
			return False
		return not self.is_substantive_word()

	def write(self, logwrite: Callable[[str], None]) -> None:
		logwrite(
			"%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%d"
			% (
				self.hyouki,
				self.nhyouki,
				self.hinshi1,
				self.hinshi2,
				self.hinshi3,
				self.hinshi4,
				self.type1,
				self.type2,
				self.kihon,
				self.kana,
				self.yomi,
				self.accent,
				self.output,
				self.sepflag,
			),
		)


def update_phonetic_symbols(mo: MecabMorph) -> None:
	for p in range(0, len(mo.yomi)):
		# 点訳のてびき第3版 第2章 その1 1 5
		# ５、長音の書き表し方 (1), (2)
		# before: ああ,ああ,感動詞,*,*,*,アア,アー,1/2,アー,0
		# after:  ああ,ああ,感動詞,*,*,*,アア,アー,1/2,アア,0
		if mo.yomi[p] == "ー" and p < len(mo.kana) and mo.kana[p] in "アイエオ":
			mo.output = mo.output[:p] + mo.kana[p] + mo.output[p + 1 :]

		# 点訳のてびき第3版 第2章 その1 1 6
		# ６、「ジ　ズ　ジャ　ジュ　ジョ」と「ヂ　ヅ　ヂャ　ヂョ」の使い分け
		# before: 綴る,綴る,動詞,自立,*,*,ツヅル,ツズル,0/3,ツズル,0
		# after:  綴る,綴る,動詞,自立,*,*,ツヅル,ツズル,0/3,ツヅル,0
		if (mo.yomi[p] == "ジ" and mo.kana[p] == "ヂ") or (mo.yomi[p] == "ズ" and mo.kana[p] == "ヅ"):
			mo.output = mo.output[:p] + mo.kana[p] + mo.output[p + 1 :]


def mecab_to_morphs(feature_lines: list[str] | None) -> list[MecabMorph]:
	li: list[MecabMorph] = []
	if not feature_lines:
		return li
	for s in feature_lines:
		if s:
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
				mo.kana = unicode_normalize(ar[8])  # "（ニチ）" -> "(ニチ)"
				# ありがとうございますー,感動詞,*,*,*,*,*,ありがとうございますー,アリガトウゴザイマスー,アリガトーゴザイマス’ー,0/1,C0
				mo.yomi = unicode_normalize(ar[9]).replace("’", "")
				mo.accent = ar[10]
				if len(ar) > 12:
					# Mecab辞書の拡張フィールドの点訳表記があれば使用する
					mo.output = unicode_normalize(ar[12])
				else:
					mo.output = mo.yomi
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
				m = mo.clone()
				m.hyouki = i[0]  # に
				m.nhyouki = unicode_normalize(i[0])  # に
				if i[3]:
					m.hinshi1 = i[3]
				if i[4]:
					m.hinshi2 = i[4]
				if i[5]:
					m.hinshi3 = i[5]
				m.kana = i[0]
				m.output = m.yomi = unicode_normalize(i[1])  # ニ
				m.accent = i[2]  # 0/1
				new_li.append(m)
		else:
			new_li.append(mo)
	return new_li


RE_KANSUJI = re.compile("^[一二三四五六七八九〇零十拾百千壱二参]+$")


# http://programminblog.blogspot.jp/2010/11/python.html
def kansuji2arabic(text: str, logwrite: Callable[[str], None] | None = None) -> tuple[int, str | None]:
	if not RE_KANSUJI.match(text):
		return (0, None)  # 漢数字ではない場合
	result = 0
	prevDigit = 0
	digit = 1
	numgroup = 1
	kanindex = len(text)
	if logwrite:
		logwrite("kansuji2arabic: " + text)
	while kanindex > 0:
		c = text[(kanindex - 1) : kanindex]
		c1 = text[kanindex : (kanindex + 1)]
		kanindex -= 1
		if c in "〇零":
			digit *= 10
		elif c in "十拾":
			digit = 10
		elif c == "百":
			if digit == 10 and c1 and c1 in "十拾":
				result += digit * numgroup
			digit = 100
		elif c == "千":
			if (digit == 10 and c1 and c1 in "十拾") or (digit == 100 and c1 and c1 in "百"):
				result += digit * numgroup
			digit = 1000
		else:
			if c in "壱一":
				result += digit * numgroup
			elif c in "二弐":
				result += 2 * digit * numgroup
			elif c in "三参":
				result += 3 * digit * numgroup
			elif c in "四":
				result += 4 * digit * numgroup
			elif c in "五":
				result += 5 * digit * numgroup
			elif c in "六":
				result += 6 * digit * numgroup
			elif c in "七":
				result += 7 * digit * numgroup
			elif c in "八":
				result += 8 * digit * numgroup
			elif c in "九":
				result += 9 * digit * numgroup
			digit *= 10
		if logwrite:
			logwrite(
				"kansuji2arabic c(%s) c1(%s) kanindex(%d) prevDigit(%d) digit(%d) result(%d) numgroup(%d)"
				% (c, c1, kanindex, prevDigit, digit, result, numgroup),
			)
		if prevDigit > digit:
			return (2, None)  # およその数で数が重なる場合
		prevDigit = digit
	if (
		(digit == 10 and text[:1] in "十拾")
		or (digit == 100 and text[:1] in "百")
		or (digit == 1000 and text[:1] in "千")
	):
		result += digit * numgroup
	text = "%d" % result
	return (1, text)  # 漢数字の場合


def rewrite_number(li: list[MecabMorph], logwrite: Callable[[str], None] | None = None) -> list[MecabMorph]:
	new_li: list[MecabMorph] = []
	for mo in li:
		m = mo.clone()
		if m.hinshi2 != "固有名詞":
			flag, num = kansuji2arabic(m.hyouki, logwrite)
			if flag == 1:
				m.output = str(num)
			elif flag == 2 and len(m.hyouki) >= 2:
				# 「二十二三」のような場合「二十二」「三」に分割
				h1 = m.hyouki[:-1]
				flag1, num1 = kansuji2arabic(h1, logwrite)
				h2 = m.hyouki[-1:]
				flag2, num2 = kansuji2arabic(h2, logwrite)
				if flag1 == 1 and flag2 == 1:
					m.output = str(num1) + "⠼" + str(num2)
		new_li.append(m)
	return new_li


def concatinate_morphs(li: list[MecabMorph]) -> MecabMorph:
	mo = li[0].clone()
	s = ""
	y = ""
	for i in li:
		s += i.hyouki
		y += i.yomi
	mo.hyouki = mo.nhyouki = s
	# mo.nhyouki = unicode_normalize(mo.nhyouki)
	mo.yomi = mo.kana = mo.output = y
	return mo


def replace_digit_morphs(li: list[MecabMorph]) -> list[MecabMorph]:
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
		if mo.hinshi2 == "数" and mo.hyouki == "，" and num_morphs:
			# カンマ
			new_li.append(concatinate_morphs(num_morphs))
			m = mo.clone()
			m.yomi = m.output = ","
			new_li.append(concatinate_morphs([m]))
			num_morphs = []
		elif (
			mo.hinshi2 == "数"
			and not mo.output.isdigit()
			and mo.hyouki not in ("・", "万", "億", "兆", "京", "．")
		):
			# 漢数字の結合
			num_morphs.append(mo)
		elif mo.hinshi2 == "数" and mo.hyouki in "０１２３４５６７８９":
			# 算用数字の結合
			m = mo.clone()
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


RE_ALPHA_OR_SINGLE = re.compile("^[A-Za-z']+$")


def is_alpha_or_single(s: str) -> bool:
	return RE_ALPHA_OR_SINGLE.match(s) is not None


RE_ASCII_SYMBOLS = re.compile(r"^[\,\.\:\;\!\?\@\#\\\$\%\&\*\|\+\-\/\=\<\>\"'\^\`\_\~]+$")


def replace_alphabet_morphs(
	li: list[MecabMorph], nabcc: bool = False, use_foreign_quotes: bool = False
) -> list[MecabMorph]:
	# アルファベットまたは記号だけで表記されている語を結合する
	# 情報処理点字の部分文字列になる記号を前後にまとめる
	# input:
	#  Ｂ,B,記号,アルファベット,*,*,ビー,ビー,1/2,B
	#  ａｓｉ,asi,名詞,一般,*,*,アシー,アシー,0/3,asi
	#  ｃ,c,記号,アルファベット,*,*,シー,シー,1/2,c
	# output:
	#  Ｂａｓｉｃ,Basic,名詞,アルファベット,*,*,ビーアシーシー,ビーアシーシー,1/2,Basic
	new_li: list[MecabMorph] = []
	alp_morphs: list[MecabMorph] = []
	for pos in range(len(li)):
		mo = li[pos]
		if pos < len(li) - 1:
			next_mo = li[pos + 1]
		else:
			next_mo = None
		if is_alpha_or_single(mo.nhyouki):
			alp_morphs.append(mo)
		elif mo.nhyouki and mo.nhyouki in r",+@/#$%&*;<":
			alp_morphs.append(mo)
		elif mo.nhyouki == "\\":
			alp_morphs.append(mo)
		elif mo.nhyouki and mo.nhyouki[0] in r",+@/#$%&*;" and RE_ASCII_SYMBOLS.match(mo.nhyouki):
			alp_morphs.append(mo)
		elif (
			alp_morphs
			and mo.nhyouki in ",."
			and (
				(next_mo and next_mo.nhyouki == " ")
				or (next_mo and next_mo.hinshi1 in ("助詞", "助動詞"))
				or (not next_mo)
			)
		):
			alp_morphs.append(mo)
		elif alp_morphs and mo.nhyouki == " " and next_mo and is_alpha_or_single(next_mo.nhyouki):
			alp_morphs.append(mo)
		elif alp_morphs and mo.nhyouki.isdigit():
			alp_morphs.append(mo)
		elif alp_morphs and mo.nhyouki in ",.:;!?@#\\$%&*|+-/=<>\"'^`_~{}[]，":
			alp_morphs.append(mo)
		elif nabcc and mo.nhyouki in "”’‘＿":
			alp_morphs.append(mo)
		elif not alp_morphs and mo.nhyouki in "[]":
			alp_morphs.append(mo)
		else:
			if alp_morphs:
				m = concatinate_morphs(alp_morphs)
				m.nhyouki = m.output = unicode_normalize(m.nhyouki)
				set_pos_of_alphabets(m)
				new_li.append(m)
				alp_morphs = []
			new_li.append(mo)
	if alp_morphs:
		m = concatinate_morphs(alp_morphs)
		m.nhyouki = m.output = unicode_normalize(m.nhyouki)
		set_pos_of_alphabets(m)
		new_li.append(m)
	return new_li


def set_pos_of_alphabets(m):
	if m.nhyouki in (",", "]["):
		m.hinshi1 = "記号"
		m.hinshi2 = "*"
	elif m.nhyouki not in "[]":
		m.hinshi1 = "名詞"
		m.hinshi2 = "アルファベット"


def merge_parenthesized_alphabet_morphs(li: list[MecabMorph]) -> list[MecabMorph]:
	"""英語句 + 括弧内英字（例: "NonVisual Desktop Access (NVDA)"）を 1 形態素にまとめる。"""
	new_li: list[MecabMorph] = []
	pos = 0
	while pos < len(li):
		# "foo (BAR)" pattern
		if pos + 4 < len(li):
			mo0, mo1, mo2, mo3, mo4 = li[pos], li[pos + 1], li[pos + 2], li[pos + 3], li[pos + 4]
			if (
				RE_GAIJI.match(mo0.nhyouki)
				and (" " in mo0.nhyouki)
				and mo1.nhyouki == " "
				and mo2.nhyouki == "("
				and RE_PAREN_ASCII_BODY.match(mo3.nhyouki)
				and mo4.nhyouki == ")"
			):
				m = concatinate_morphs(li[pos : pos + 5])
				m.nhyouki = m.output = unicode_normalize(m.nhyouki)
				set_pos_of_alphabets(m)
				new_li.append(m)
				pos += 5
				continue
		# "foo(BAR)" pattern
		if pos + 3 < len(li):
			mo0, mo1, mo2, mo3 = li[pos], li[pos + 1], li[pos + 2], li[pos + 3]
			if (
				RE_GAIJI.match(mo0.nhyouki)
				and mo1.nhyouki == "("
				and RE_PAREN_ASCII_BODY.match(mo2.nhyouki)
				and mo3.nhyouki == ")"
			):
				m = concatinate_morphs(li[pos : pos + 4])
				m.nhyouki = m.output = unicode_normalize(m.nhyouki)
				set_pos_of_alphabets(m)
				new_li.append(m)
				pos += 4
				continue
		new_li.append(li[pos])
		pos += 1
	return new_li


# 日付の和語読み処理
# すでに output 属性に半角数字が格納されている前提

# 後続する '日' と形態素を結合する
WAGO_DIC = {
	"1": "ツイタチ",
	"2": "フツカ",
	"3": "ミッカ",
	"4": "ヨッカ",
	"5": "イツカ",
	"6": "ムイカ",
	"7": "ナノカ",
	"8": "ヨーカ",
	"9": "ココノカ",
	"10": "トオカ",
	"20": "ハツカ",
}


def fix_japanese_date_morphs(li):
	new_li = []
	for i in range(0, len(li)):
		prev2_mo = li[i - 2] if i - 2 >= 0 else None
		prev_mo = li[i - 1] if i - 1 >= 0 else None
		mo = li[i]
		if mo.hyouki == "日" and mo.hinshi3 == "助数詞" and prev_mo is not None:
			if prev_mo.hyouki in ("14", "24", "十四", "一四", "二四", "二十四"):
				li[i].output = "カ"
				new_li.append(li[i])
			elif (prev2_mo is None or prev2_mo.hyouki != "、") and prev_mo.output in WAGO_DIC:
				m = mo.clone()
				m.hyouki = prev_mo.hyouki + mo.hyouki
				m.nhyouki = prev_mo.nhyouki + mo.nhyouki
				m.output = WAGO_DIC[prev_mo.output]
				m.kana = m.yomi = m.output
				m.hinshi2 = "日付"
				m.hinshi3 = "*"
				# FIXME: m.accent
				new_li.pop()
				new_li.append(m)
			else:
				new_li.append(li[i])
		else:
			new_li.append(li[i])
	return new_li


def should_separate(prev2_mo, prev_mo, mo, next_mo, nabcc=False, logwrite=_logwrite):
	################################
	# True
	################################

	# 括弧開の前
	# (あける)
	# 映画,映画,名詞,一般,*,*,エイガ,エイガ,0/3,エイガ,1
	# 「,「,記号,括弧開,*,*,「,「,*/*,「,0
	# (あけない)
	# 機関,名詞,一般,*,*,*,*,機関,キカン,キカン,1/3,C1
	# （,記号,括弧開,*,*,*,*,（,（,（,*/*,*
	if prev_mo.hinshi1 == "名詞" and mo.hinshi2 == "括弧開" and mo.nhyouki != "(":
		return True

	# )( -> あける
	# )陽が -> あける
	# '02 -> あけない
	if prev_mo.hinshi2 == "括弧閉" and prev_mo.nhyouki != "’":
		if mo.hinshi2 == "括弧開":
			return True
		if mo.hinshi1 == "名詞":
			return True

	# 数字の前のマスアケ
	mo_output_isdigit = mo.output.isdigit()
	if (
		mo_output_isdigit
		and not nabcc
		and prev_mo.output != "⠼"
		and prev_mo.nhyouki
		not in ("-", "，", ".", "’", "、", ":", "：", ",", "ー", "(", "第", "築", "二男", "中")
	):
		return True

	# 1月/1日
	if mo_output_isdigit and prev_mo.nhyouki and prev_mo.nhyouki[0].isdigit() and prev_mo.nhyouki[-1] == "月":
		return True

	# 三,三,名詞,数,*,*,サン,サン,0/2,3,0
	# 兆,兆,名詞,数,*,*,チョウ,チョー,1/2,チョー,1
	# 二千四百,二千四百,名詞,数,*,*,ニセンヨンヒャク,ニセンヨンヒャク,1/1,2400,0
	# 万,万,名詞,数,*,*,マン,マン,1/2,マン,0
	if mo_output_isdigit and prev_mo.hyouki in ("億", "兆", "京"):
		return True

	# 外国語引用符、マスアケ、助詞、助動詞
	is_mo_hinshi1_joshi_or_jodoshi = mo.hinshi1 in ("助詞", "助動詞")
	if is_mo_hinshi1_joshi_or_jodoshi and prev_mo.output and prev_mo.output.endswith("⠴"):
		return True

	# アルファベットの後の助詞、助動詞
	# ＣＤ,CD,名詞,一般,*,*,シーディー,シーディー,3/4,シーディー,0
	# を,を,助詞,格助詞,一般,*,ヲ,ヲ,0/1,ヲ,0
	is_prev_mo_nhyouki_alpha_or_single = is_alpha_or_single(prev_mo.nhyouki)
	if is_prev_mo_nhyouki_alpha_or_single and is_mo_hinshi1_joshi_or_jodoshi:
		return True
	if nabcc and prev_mo.hinshi2 == "アルファベット" and is_mo_hinshi1_joshi_or_jodoshi:
		return True

	# ピリオドの後の助詞
	if prev_mo.nhyouki.endswith(".") and mo.hinshi1 == "助詞":
		return True

	# ナンバーマークの後の助詞
	if prev_mo.nhyouki == "#" and mo.hinshi1 == "助詞":
		return True

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
	if mo_output_isdigit and prev_mo.hinshi1 == "名詞" and prev_mo.hinshi2 == "接尾":
		return True

	if prev_mo.hinshi1 == "助詞" and mo.hinshi1 == "接頭詞":
		return True

	# 新/東京/名所
	if (
		prev_mo.hinshi1 == "接頭詞"
		and prev_mo.hinshi2 == "名詞接続"
		and mo.hinshi1 == "名詞"
		and mo.hinshi2 == "固有名詞"
	):
		# 後白河
		if not (prev_mo.hyouki == "後" and prev_mo.yomi == "ゴ"):
			return True

	# 多かれ/少なかれ
	if prev_mo.hinshi1 == "形容詞" and mo.hinshi1 == "形容詞":
		if prev_mo.type2 == "命令ｅ" and mo.type2 == "命令ｅ":
			return True

	# 複合語（接頭語・接尾語・造語要素）【備考１】
	# 接頭語・接尾語・造語要素であっても、意味の理解を助ける場合には、
	# 発音上の切れ目を考慮して区切って書いてよい。
	if (
		prev_mo.hinshi1 == "接頭詞"
		and prev_mo.hyouki in ("貴", "前", "当", "反", "非", "新", "要", "肝", "逆", "超")
		and mo.hinshi1 == "名詞"
		and mo.hinshi2 != "数"
	):
		return True

	# 人名に続く「さん」「様」「君」「殿」「氏（し）」「氏（うじ）」は区切って書く
	# (名詞,固有名詞,人名 -> 名詞,接尾,人名)
	if prev_mo.hinshi2 == "固有名詞" and prev_mo.hinshi3 == "人名":
		if mo.hinshi2 == "接尾" and mo.hinshi3 == "人名":
			return True
		if mo.hyouki in ("さん", "知事"):
			return True

	# 地域
	# 永田町 １
	# 「岬」「峠」「半島」はマス空けが原則
	if (
		prev_mo.hinshi2 == "固有名詞"
		and prev_mo.hinshi3 == "地域"
		and (mo.hinshi2 == "数" or mo.hyouki in ("岬", "峠", "半島"))
	):
		return True

	# 伊豆/大島
	if prev_mo.hinshi2 == "固有名詞" and mo.hinshi2 == "固有名詞":
		return True

	# 日/独/伊/3国同盟
	if (
		prev_mo.hinshi2 == "固有名詞"
		and prev_mo.hinshi3 == "地域"
		and mo.hinshi1 == "名詞"
		and mo.hinshi2 == "一般"
	):
		if not (mo.hyouki == "卿" and mo.yomi == "キョー") and not (mo.hyouki == "市" and mo.yomi == "シ"):
			return True

	# 東京/都 千代田/区
	if (
		prev_mo.hinshi2 == "接尾"
		and prev_mo.hinshi3 == "地域"
		and mo.hinshi2 == "固有名詞"
		and mo.hinshi3 == "地域"
	):
		return True

	# 東京/都 交通/局
	if (
		prev_mo.hinshi2 == "接尾"
		and prev_mo.hinshi3 == "地域"
		and mo.hinshi1 == "名詞"
		and mo.hinshi2 == "一般"
	):
		return True

	# 聞き捨てならない キキズテ ナラナイ
	if prev_mo.hinshi1 == "動詞" and mo.hinshi1 == "動詞" and mo.hyouki == "なら":
		return True

	# お,黙り,なさい
	# 「お」がついて名詞化した語に「なさい・なさる」が続く場合は区切ってよい
	if (
		prev2_mo
		and prev2_mo.hinshi1 == "接頭詞"
		and prev2_mo.hyouki == "お"
		and prev_mo.hinshi1 == "動詞"
		and prev_mo.type2 == "連用形"
		and mo.kihon == "なさる"
	):
		return True

	if prev_mo.hinshi1 == "動詞" and prev_mo.hinshi2 == "自立" and mo.hyouki == "および":
		return True

	# 障害,者/協会
	if prev2_mo and prev2_mo.hinshi1 == "名詞" and prev_mo.hyouki == "者" and mo.hinshi1 == "名詞":
		return True

	# 世界/初
	if prev_mo.hinshi1 == "名詞" and prev_mo.hinshi2 == "一般" and mo.hyouki == "初":
		return True

	# 40キロ レース
	if prev_mo.hinshi3 == "助数詞" and mo.hyouki == "レース":
		return True

	# 1回こっきり 1カイ コッキリ
	if prev_mo.hyouki == "回" and mo.hyouki == "こっきり":
		return True

	# Ｈ形コンベアー Hガタ コンベアー
	if prev_mo.hyouki[-1] == "形" and mo.hyouki == "コンベアー":
		return True

	# 漢字仮名交じり文 カンジ カナマジリブン
	if mo.hyouki == "仮名" and mo.output == "カナ":
		if prev_mo.hyouki == "漢字":
			return True

	# 晴れ/所に より
	if prev_mo.hinshi1 == "名詞" and mo.hyouki == "所により":
		return True

	# 右/斜め/上
	if mo.hyouki == "斜め":
		return True
	if prev_mo.hyouki == "斜め":
		return True

	# 一番/上
	if prev_mo.hyouki == "一番" and mo.hinshi1 == "名詞":
		return True

	# 一時/雨
	if prev_mo.hyouki == "一時" and mo.hinshi1 == "名詞":
		return True

	# とは/言う/ものの
	if prev_mo.hyouki == "言う" and mo.hyouki == "ものの":
		return True

	# 一脈/相通じる/ものが/ある
	if prev_mo.hyouki == "相通じる" and mo.hyouki == "もの":
		return True

	# 一審/判決
	if prev_mo.hyouki == "審" and mo.hyouki == "判決":
		return True

	# 意図/不明
	# 意味/不明
	if mo.hyouki == "不明":
		return True

	# 今/現在
	if prev_mo.hyouki == "今" and mo.hyouki == "現在":
		return True

	# 癌予防 ガン ヨボー
	if prev_mo.hyouki == "癌" and mo.hyouki == "予防":
		return True

	# 旧華族 キュー カゾク
	# 旧街道 キューカイドー 点訳のてびき第3版 第3章 その2 2
	if prev_mo.hyouki == "旧" and mo.hyouki != "街道":
		return True

	# 禁転載 キン テンサイ
	if prev_mo.hyouki == "禁" and prev_mo.output == "キン":
		return True

	# 休暇届 キューカ トドケ
	if mo.hyouki == "届" and mo.output == "トドケ":
		return True

	# 500円強 500エン キョー
	if mo.hyouki == "強" and mo.output == "キョー":
		return True

	# 父太郎 チチ タロー
	if prev_mo.hyouki == "父" and mo.hinshi2 == "固有名詞":
		return True

	if prev_mo.hinshi1 == "助動詞" and prev_mo.hyouki == "で" and mo.hinshi1 == "助動詞":
		return True

	# 「の」（名詞,非自立）の後に名詞が続く場合にスペースを挿入
	# 例1: 映画「ラヂオの時間」 → エイガ 「ラジオノ ジカン」
	#  ラヂオ,名詞,一般 → ラジオ
	#  の,名詞,非自立 → ノ
	#  時間,名詞,副詞可能 → ジカン
	# 例2: 気を付けの姿勢 → キヲツケノ シセイ
	#  気を付け,名詞,一般 → キヲツケ
	#  の,名詞,非自立 → ノ
	#  姿勢,名詞,一般 → シセイ
	if (
		prev_mo.hinshi1 == "名詞"
		and prev_mo.hinshi2 == "非自立"
		and prev_mo.hyouki == "の"
		and mo.hinshi1 == "名詞"
		and mo.hinshi2 in ("一般", "副詞可能")
	):
		return True

	# 感動詞の後に助動詞「ござい」が続く場合にスペースを挿入
	# 例: 有り難うございました → アリガトー ゴザイマシタ
	#  有り難う,感動詞 → アリガトー
	#  ござい,助動詞 → ゴザイ
	if (
		prev_mo.hinshi1 == "感動詞"
		and prev_mo.hyouki == "有り難う"
		and mo.hinshi1 == "助動詞"
		and mo.hyouki == "ござい"
	):
		return True

	# 仮名文字 カナモジ
	# 仮名タイプ カナタイプ
	# 仮名変換 カナ ヘンカン
	if prev_mo.hyouki == "仮名" and prev_mo.output == "カナ":
		if len(mo.output.split(" ")[-1]) >= 4:
			return True

	if prev_mo.hyouki == "擬似" and mo.hyouki == "コレラ":
		return True
	if prev_mo.hyouki == "火事" and mo.hyouki == "見舞い":
		return True
	if prev_mo.hyouki in ("危機", "機器", "記紀", "記事", "義務"):
		return True
	if mo.hyouki in ("危機", "機器", "記紀", "記事", "義務"):
		return True

	# 人名に造語要素が続く場合で、2拍以下の場合は続ける
	# 自立性が強く、意味の理解を助ける場合は、前を区切って書く
	if prev_mo.hinshi1 == "名詞" and mo.hinshi1 == "名詞":
		if prev_mo.hinshi4 in ("姓", "名") or prev_mo.hinshi3 == "人名":
			if mo.hinshi2 == "接尾" and mo.hinshi3 == "人名":
				return True
			if mo.hyouki in ("訳", "作", "談", "曲", "記", "絵", "アナ", "プロ"):
				return True

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
	# 形容詞「ない」は区切る
	# ただし前の語と複合している場合は前に続ける
	if mo.hinshi1 == "助動詞" and mo.kihon in ("ない", "無い"):
		if prev_mo.hinshi1 == "助詞" and prev_mo.kihon == "は":
			return True
		if prev_mo.hinshi1 == "形容詞" and prev_mo.kihon == "良い":
			return True
		if (
			prev_mo.hinshi1 == "名詞"
			and prev_mo.hinshi2 == "ナイ形容詞語幹"
			and prev_mo.kihon in ("問題", "間違い")
		):
			return True
		if prev_mo.hinshi2 == "副助詞":  # じゃない
			return True
		if prev_mo.hinshi1 == "動詞" and prev_mo.hinshi2 == "非自立" and prev_mo.kihon == "てる":  # てない
			return True
		if prev_mo.hinshi1 == "助動詞" and prev_mo.kihon == "だ":  # でない
			return True
	if mo.hinshi1 == "形容詞" and mo.kihon in ("ない", "無い", "悪い"):
		if prev_mo.kihon not in ("隈", "心置き", "満遍", "決まり", "限"):
			return True

	################################
	# False
	################################

	if prev_mo.hyouki.endswith("　"):
		return False

	if prev_mo.hyouki == "ー":
		return False

	# ち,ち,名詞,一般,*,*,チ,チ,0/1,チ,0
	# ゅうりっぷ,ゅうりっぷ,名詞,一般,*,*,,,,ュウリップ,0
	if mo.hyouki and (mo.hyouki[0] in "ーぁぃぅぇぉっゃゅょゎァィゥェォッャュョヮヵヶ"):
		return False

	# 0/4月 -> 04月
	prev_mo_output_isdigit = prev_mo.output.isdigit()
	if prev_mo_output_isdigit and mo.nhyouki and mo.nhyouki[0].isdigit():
		return False
	# 3/03
	if prev_mo_output_isdigit and mo.nhyouki and mo.nhyouki[0] == "/":
		return False
	if prev_mo_output_isdigit and mo.hinshi3 == "助数詞":
		return False
	if prev_mo_output_isdigit and mo.nhyouki == "#":
		return False

	# アラビア数字のあとに単位がきたら続ける
	# 三十,三十,名詞,数,*,*,30,30,1/4,30,1
	# センチメートル,センチメートル,名詞,一般,*,*,センチメートル,センチメートル,4/7,センチメートル,0
	if prev_mo_output_isdigit and mo.hyouki in ("センチメートル", "楽章"):
		return False

	# カナ名詞の後のアルファベット名詞
	if prev_mo.hinshi1 == "名詞" and is_alpha_or_single(mo.nhyouki):
		# キラーＴ細胞 キラー Tサイボー
		if prev_mo.hyouki != "キラー":
			return False

	# アルファベットの後の名詞
	# V字
	if is_prev_mo_nhyouki_alpha_or_single and mo.hyouki in ("細胞", "字"):
		return False

	# https://github.com/nvdajp/nvdajpmiscdep/issues/67
	if (
		nabcc
		and prev_mo.hinshi2 == "アルファベット"
		and (prev_mo.nhyouki.endswith("(") or prev_mo.nhyouki.endswith("[") or prev_mo.nhyouki.endswith("{"))
		and mo.hinshi1 == "名詞"
	):
		return False

	# 数字の後のアルファベット
	if prev_mo.hinshi2 == "数" and mo.hinshi2 == "アルファベット":
		if nabcc:
			return False
		elif RE_ASCII_CHARS.match(mo.nhyouki):
			return False

	if prev_mo.hinshi1 == "名詞" and mo.hinshi1 == "名詞" and mo.hinshi2 == "数":
		return False
	if mo.hyouki == "嬢" and (prev_mo.hinshi4 in ("姓", "名") or prev_mo.hinshi3 == "人名"):
		return False
	# 京急,線 東急,線
	if mo.hyouki == "線" and prev_mo.hinshi3 == "組織":
		return False

	if prev_mo.hinshi1 == "動詞" and prev_mo.hinshi2 == "自立":
		if mo.hinshi1 == "動詞" and mo.hinshi2 == "非自立":
			return False

	if prev_mo.hinshi1 == "接頭詞" and mo.hinshi1 == "名詞":
		return False

	# その,その,連体詞,*,*,*,ソノ,ソノ,0/2,ソノ,1
	# よう,よう,名詞,非自立,助動詞語幹,*,ヨウ,ヨー,1/2,ヨー,0
	if prev_mo.hinshi1 == "連体詞" and mo.hinshi3 == "助動詞語幹":
		return False

	# 数%
	if prev_mo.hyouki == "数" and prev_mo.yomi == "スー" and mo.hyouki == "％":
		return False

	if prev_mo.hyouki == "フェア" and mo.hyouki == "キャッチ":
		return False
	if prev_mo.hyouki == "擬古" and mo.hyouki == "文":
		return False
	if prev_mo.hyouki == "白" and mo.hyouki == "生地":
		return False
	if prev_mo.hyouki == "今日" and mo.hyouki == "限り":
		return False

	# 334万画素 334マンガソ
	if prev_mo.hyouki == "万" and mo.hyouki == "画素":
		return False

	# 薄ら笑い ウスラワライ
	if prev_mo.hyouki == "薄ら" and mo.hinshi1 == "名詞":
		return False

	# 扱い始め
	if prev_mo.hinshi1 == "名詞" and mo.hyouki == "始め":
		return False

	# 岩倉卿
	if mo.hyouki == "卿" and mo.yomi == "キョー":
		return False

	# 京言葉
	if prev_mo.hyouki == "京" and prev_mo.yomi == "キョー":
		return False

	# そう.な.ん.です.もの
	# そう.なん.だって
	if prev_mo.hyouki == "な" and mo.hyouki == "ん":
		return False
	if prev_mo.hyouki == "です" and mo.hyouki == "もの":
		return False
	if prev_mo.hyouki == "そう" and mo.hyouki == "なん":
		return False

	# 「・・ですこと」の「こと」は接尾語なので前に続ける
	if prev_mo.hyouki == "です" and mo.hyouki == "こと":
		return False

	# 否が/応でも
	if prev_mo.hyouki == "応" and mo.hyouki == "でも":
		return False

	# 「この程」「この度」
	# 「そのくせ」
	# 後ろの語と結びついて1語になっている場合は続ける
	if prev_mo.hyouki == "この" and mo.hyouki in ("程", "度"):
		return False
	if prev_mo.hyouki == "その" and mo.hyouki in ("くせ", "うち", "まま"):
		return False
	if prev_mo.hyouki == "わが" and mo.hyouki == "まま":
		return False

	# 労,せ,ず
	if prev_mo.hinshi1 == "名詞" and mo.hyouki == "せ" and mo.kihon == "する":
		return False

	# いいんですけど
	if prev_mo.hinshi1 == "形容詞" and mo.hyouki == "ん":
		return False

	# 見/まごう
	if prev_mo.hinshi1 == "動詞" and prev_mo.hyouki == "見":
		return False

	# お兄さん, お姉さん
	if prev_mo.hinshi1 == "接頭詞" and prev_mo.hyouki == "お":
		return False

	# のように
	if prev_mo.hinshi1 == "助詞" and mo.hyouki == "よう":
		return False

	# 利かぬ気, 利かん気
	if prev_mo.hinshi1 == "助動詞" and mo.hyouki == "気":
		return False

	# 器量よし
	if prev_mo.hinshi1 == "名詞" and mo.hyouki == "よし":
		return False

	# 行ったきり
	if prev_mo.hinshi1 == "助動詞" and mo.hyouki == "きり":
		return False

	# 鍛冶,職人 カジショクニン
	if len(prev_mo.output) <= 2 and mo.hyouki == "職人":
		return False

	# 金の減り.加減 カネノ ヘリカゲン
	# 馬鹿さ.加減 バカサ カゲン
	if mo.hyouki == "加減" and mo.yomi == "カゲン":
		if len(prev_mo.output.split(" ")[-1]) < 3:
			return False

	if mo.hinshi1 == "助動詞" and mo.kihon in ("ない", "無い"):
		return False

	# 仮名文字 カナモジ
	# 仮名タイプ カナタイプ
	# 仮名変換 カナ ヘンカン
	if prev_mo.hyouki == "仮名" and prev_mo.output == "カナ":
		return False

	# 面白おかしい (点訳のてびき第3版 第3章 その2 10. 複合形容詞は続ける)
	if prev_mo.hinshi1 == "形容詞" and mo.hinshi1 == "形容詞":
		return False

	if mo.hinshi1 == "形容詞" and mo.kihon in ("ない", "無い", "悪い"):
		return False

	# 不幸,に,し,て
	# 今,に,し,て
	# 居,ながら,に,し,て
	# 労,せ,ず,し,て
	# 若く,し,て
	# 私,を,し,て
	# 「して」が文語的表現の助詞である場合は前に続けて書く
	if mo.hyouki == "し" and mo.kihon == "する":
		if prev_mo.hyouki == "ず" and prev_mo.hinshi1 == "助動詞":
			return False
		if prev_mo.hinshi1 == "形容詞" and prev_mo.type2 == "連用テ接続":
			return False
		if prev_mo.hinshi2 == "接続助詞":
			return False
		if prev_mo.type1 == "文語・ベシ":
			return False
		if next_mo and next_mo.hyouki == "て":
			if prev_mo.hyouki == "に" and prev_mo.hinshi1 == "助詞":
				return False
			if prev2_mo and prev2_mo.hyouki == "私" and prev_mo.hyouki == "を":
				return False

	################################
	# False/True
	################################

	# ２字漢語 母子/年金 幾何/模様 基礎/医学 騎馬/武者
	if (
		mo.hinshi1 == "名詞"
		and mo.hinshi2 == "一般"
		and len(prev_mo.hyouki) == 2
		and len(prev_mo.yomi) == 2
		and len(mo.yomi) >= 3
		and not RE_KATAKANA.match(mo.nhyouki)
	):
		return True

	# 複合名詞内部の2拍以下は切らない
	if (
		prev_mo.hinshi1 == "名詞"
		and prev_mo.hinshi2 not in ("数", "アルファベット")
		and mo.hinshi1 == "名詞"
		and mo.hinshi2 not in ("数", "アルファベット", "接尾")
	):
		if len(prev_mo.yomi) >= 4 and len(mo.yomi) >= 2:
			if mo.hyouki != "鍛冶":
				return True
		if len(mo.yomi) >= 4:
			if prev_mo.hyouki not in ("右", "花"):
				return True
		if len(prev_mo.yomi) <= 2 and len(mo.yomi) >= 3:
			return False
		if len(prev_mo.yomi) >= 3 and len(mo.yomi) <= 2:
			return False

	if prev_mo.is_substantive_word() and mo.is_independent_word():
		return True
	if prev_mo.is_independent_word() and mo.is_independent_word():
		return True
	return False


def morphs_to_string(li, inbuf, logwrite):
	outbuf = ""
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
		elif out[:2] == "⠠⠦" and out[-2:] == "⠠⠴":
			# 情報処理用点字の内側
			c = outlen - 4
			inpos2.extend([p] * 2)
			inpos2.extend(range(p, p + c))
			inpos2.extend([p + c - 1] * 2)
		elif out[:1] == "⠦" and out[-1:] == "⠴":
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
			outbuf += " "
			if p > 0:
				inpos2.append(p - 1)  # マスアケは直前の文字に対応
			else:
				inpos2.append(p)
	# rstrip with inpos2
	if inbuf[-1] != " ":
		while outbuf[-1:] == " ":
			outbuf = outbuf[:-1]
			inpos2.pop()
	return (outbuf, inpos2)


RE_MB_ALPHA_NUM_SPACE = re.compile(r"^[0-9A-Za-z\- ０-９Ａ-Ｚａ-ｚ　]+$")
# Greek (U+0370-U+03FF) and Cyrillic (U+0400-U+04FF) letters
RE_GREEK_CYRILLIC = re.compile(r"^[\u0370-\u04FF]+$")
RE_ASCII_CHARS = re.compile(r"^[A-Za-z0-9\.\,\-\+\:\/\~\?\&\%\#\*\$\; ]+$")
RE_ASCII_AND_SYMBOLS = re.compile(r"^[A-Za-z0-9\.\,\-\+\:\/\~\?\&\%\#\*\$\; \u00d7]+$")
RE_INFORMATION = re.compile(r"^[A-Za-z0-9\+\@\/\#\$\%\&\*\;\.\<\>\-\_\{\}\[\] ]+$")
RE_GAIJI = re.compile(r"^[A-Za-z][A-Za-z0-9\,\.\+\-'\!\? ]+$")
RE_GAIJI_WITH_PARENS = re.compile(r"^[A-Za-z][A-Za-z0-9\,\.\+\-'\!\? ]*\([A-Za-z0-9\,\.\+\-'\!\? ]+\)$")
RE_PAREN_ASCII_BODY = re.compile(r"^[A-Za-z0-9\,\.\+\-'\!\? ]+$")
# US 2級で前置符・インジケータが入りやすい「ドット区切り英数字トークン」
# 例: www.example.com, example.co.jp, v1.4, 1.0, Dr.Smith, 192.168.0.1
# - 空白を含まない
# - ドット `.` で区切られたラベルが 2 個以上
# - 各ラベルは先頭が英数字、以降は英数字・ハイフン・アンダースコア
RE_US_G2_DOTTED_TOKEN = re.compile(
	r"^[A-Za-z0-9][A-Za-z0-9_-]*(?:\.[A-Za-z0-9][A-Za-z0-9_-]*)+$"
)
RE_KATAKANA = re.compile("^[ァ-ヾ]+$")
RE_HIRAGANA = re.compile("^[ぁ-ゞ]+$")
RE_HALF_KATAKANA = re.compile("^[ｦ-ﾟ]+$")  # ff66 .. ff9f
RE_DIGIT_SINGLE_ALPHA = re.compile("^[0-9]+'[A-Za-z]+$")

NO_DAKUON_DIC = {
	"ガ": "カ",
	"ギ": "キ",
	"グ": "ク",
	"ゲ": "ケ",
	"ゴ": "コ",
	"ザ": "サ",
	"ジ": "シ",
	"ズ": "ス",
	"ゼ": "セ",
	"ゾ": "ソ",
	"ダ": "タ",
	"ヂ": "チ",
	"ヅ": "ツ",
	"デ": "テ",
	"ド": "ト",
	"バ": "ハ",
	"ビ": "ヒ",
	"ブ": "フ",
	"ベ": "ヘ",
	"ボ": "ホ",
}

DAKUON_DIC = {
	"カ": "ガ",
	"キ": "ギ",
	"ク": "グ",
	"ケ": "ゲ",
	"コ": "ゴ",
	"サ": "ザ",
	"シ": "ジ",
	"ス": "ズ",
	"セ": "ゼ",
	"ソ": "ゾ",
	"タ": "ダ",
	"チ": "ヂ",
	"ツ": "ヅ",
	"テ": "デ",
	"ト": "ド",
	"ハ": "バ",
	"ヒ": "ビ",
	"フ": "ブ",
	"ヘ": "ベ",
	"ホ": "ボ",
}


def is_gaiji(s):
	return RE_GAIJI.match(s)


def to_no_dakuon_kana(s):
	if s in NO_DAKUON_DIC:
		return NO_DAKUON_DIC[s]
	return s


def to_dakuon_kana(s):
	if s in DAKUON_DIC:
		return DAKUON_DIC[s]
	return s


TAB_CODE = chr(0x200B)


def japanese_braille_separate(inbuf, logwrite, nabcc=False, use_foreign_quotes=False):
	text = inbuf
	# NVDA focus/review strings may contain CR/LF; MeCab path rejects them.
	if "\r" in text or "\n" in text:
		if logwrite:
			logwrite(f"translator2: normalizing line breaks: {text!r}")
		text = text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", " ")
	if RE_HALF_KATAKANA.match(text):
		outbuf = text
		inpos2 = range(len(outbuf))
		return (outbuf, inpos2)

	if not nabcc and RE_MB_ALPHA_NUM_SPACE.match(text):
		outbuf = unicode_normalize(text)
		# fall through if contains alpha char (to be wrapped with foreign quote)
		if use_foreign_quotes and not any(c.isalpha() for c in outbuf):
			inpos2 = list(range(len(outbuf)))
			return (outbuf, inpos2)
		# legacy behavior: always return result here
		if not use_foreign_quotes:
			inpos2 = list(range(len(outbuf)))
			return (outbuf, inpos2)

	if not nabcc and is_gaiji(text) and " " in text.rstrip():
		rspaces = ""
		while text[-1] == " ":
			rspaces += " "
			text = text[:-1]
		outbuf = "⠦" + unicode_normalize(text) + "⠴" + rspaces
		inpos2 = [0] + list(range(len(outbuf)))
		inpos2.append(inpos2[-1])
		return (outbuf, inpos2)

	# 'あ゛ー' Unicode 正規化されて空白が入るので事前に補正する
	text = text.replace("あ゛", "あ")
	text = text.replace("ヱ゛", "ヴェ")
	text = text.replace("ヲ゛", "ヴォ")
	text = text.replace("ワ゛", "ヴァ")

	# tab code
	text = text.replace("\t", TAB_CODE)
	if TAB_CODE in text:
		logwrite(f"translator2: TAB_CODE present after tab replace: {text!r}")

	# 'ふにゃ～'
	text = text.replace("ゃ～", "ゃー")

	assert "\t" not in text and "\r" not in text and "\n" not in text, "translator2: unexpected tab/CR/LF"
	ascii_count = sum(1 for c in text if ord(c) < 0x80)
	non_ascii_count = len(text) - ascii_count
	if ascii_count and non_ascii_count:
		mixed_alnum = any(c.isalnum() and ord(c) < 0x80 for c in text)
		# Allow TAB_CODE (U+200B) in mixed text to continue investigation.
		if mixed_alnum and TAB_CODE not in text:
			if logwrite:
				logwrite(f"translator2: mixed ASCII alnum and non-ASCII: {text!r}")
	if "  " in text:
		if logwrite:
			logwrite("translator2: consecutive ASCII spaces detected")
	# NFKC normalization changes the character count for some characters
	# (U+2026 HORIZONTAL ELLIPSIS -> "...", U+2469 CIRCLED NUMBER TEN -> "10"),
	# so the normalization inside the analyzer (text2mecab) would make inpos2
	# drift from the original text. Normalize here with a position map
	# instead; NFKC is idempotent, so the second normalization inside the
	# analyzer no longer changes the length. nvdajp issues #117, #328
	text, nfkc_map = nfkc_normalize_with_map(text)
	analyzer = _analyzer
	if analyzer is None:
		raise RuntimeError("translator2 is not initialized; call initialize(analyzer=...)")
	li = mecab_to_morphs(analyzer.analyze(text, logwrite))

	li = [mo for mo in li if mo.hyouki]

	for mo in li:
		if TAB_CODE in mo.nhyouki:
			mo.hinshi1 = "記号"
			# mo.hinshi2 = '空白'
			mo.kana = mo.yomi = mo.output = mo.nhyouki

	for mo in li:
		if mo.hinshi1 == "空白":
			mo.output = " "
		elif mo.hinshi2 == "数" and mo.nhyouki.isdigit():
			# digit numbers (not kanji characters)
			mo.output = mo.nhyouki
		elif RE_GREEK_CYRILLIC.match(mo.nhyouki):
			# Greek and Cyrillic words are unknown to MeCab (no reading) and
			# would otherwise be dropped because their output stays empty.
			# Pass the characters through so that translator1 renders them
			# with Greek or Russian braille patterns. nvdajp issues #224, #456
			mo.output = mo.nhyouki

	li = replace_morphs(li, CONNECTED_MORPHS)

	# before:
	# たー,たー,助動詞,*,*,*,*,*,たー,ター,ター,1/2,ター,0
	# ー,ー,名詞,一般,*,*,*,*,*,,,,,0
	# after:
	# た,た,助動詞,*,*,*,*,*,た,タ,タ,1/2,タ,0
	# ー,ー,名詞,一般,*,*,*,*,*,,,,ー,0

	# before: ３ー,名詞,数,*,*,*,*,３ー,サンー,サンー,1/3,C0
	# after:  ３,名詞,数,*,*,*,*,３,サン,サン,1/3,C0
	for pos in range(len(li) - 1):
		mo = li[pos]
		mo2 = li[pos + 1]
		if "ー" in mo.hyouki and mo2.hyouki == "ー":
			mo.hyouki = mo.kihon = mo.hyouki.replace("ー", "")
			mo.nhyouki = unicode_normalize(mo.hyouki)
			mo.kana = mo.kana.replace("ー", "")
			mo.yomi = mo.yomi.replace("ー", "")
			if mo.hinshi2 == "数":
				mo.output = mo.nhyouki
			else:
				mo.output = mo.yomi

	# 動詞のウ音便
	# before:
	# 思う,思う,動詞,自立,*,*,五段・ワ行ウ音便,連用タ接続,思う,オモウ,オモウ,2/3,オモウ,0
	# て,て,助詞,接続助詞,*,*,*,*,て,テ,テ,0/1,テ,0
	# after:
	# 思う,思う,動詞,自立,*,*,五段・ワ行ウ音便,連用タ接続,思う,オモウ,オモウ,2/3,オモー,0
	# て,て,助詞,接続助詞,*,*,*,*,て,テ,テ,0/1,テ,0
	for pos in range(len(li) - 1):
		mo = li[pos]
		mo2 = li[pos + 1]
		if (
			mo.hinshi1 == "動詞"
			and mo.hyouki in ("思う", "吸う", "繕う")
			and len(mo.yomi) > 1
			and mo.yomi[-1] == "ウ"
			and mo2.yomi[:1] in ("タ", "テ")
		):
			mo.output = mo.yomi[:-1] + "ー"
			# https://github.com/nvdajp/nvdajpmiscdep/issues/42
			# https://github.com/nvdajp/nvdajpmiscdep/issues/63

	li = replace_digit_morphs(li)
	li = rewrite_number(li, logwrite)

	# before: う,う,助動詞,*,*,*,ウ,ウ,0/1,ウ,0
	# after:  う,う,助動詞,*,*,*,ウ,ウ,0/1,ー,0
	for mo in li:
		if mo.hyouki == "う" and mo.hinshi1 == "助動詞":
			mo.output = "ー"

	# before: ａ,a,記号,アルファベット,*,*,エイ,エイ,1/2,エイ,0
	# after:  ａ,a,記号,アルファベット,*,*,エイ,エイ,1/2,a,0
	for mo in li:
		if mo.hinshi2 == "アルファベット":
			mo.output = mo.nhyouki

	li = replace_alphabet_morphs(li, nabcc=nabcc, use_foreign_quotes=use_foreign_quotes)
	if use_foreign_quotes and not nabcc:
		li = merge_parenthesized_alphabet_morphs(li)

	for mo in li:
		if mo.hyouki == "〝":
			mo.hinshi1 = "記号"
			mo.hinshi2 = "括弧開"
		if mo.hyouki == "〟":
			mo.hinshi1 = "記号"
			mo.hinshi2 = "括弧閉"
		if mo.hyouki == "々々々々":
			mo.hinshi1 = "記号"
			mo.hinshi2 = "一般"
		if mo.hyouki == "〻":
			# 303b 二の字点（にのじてん）
			mo.hinshi1 = "記号"
			mo.hinshi2 = "一般"

	for mo in li:
		if mo.hinshi2 in ("括弧開", "括弧閉"):
			mo.output = mo.nhyouki

	# before: 　, ,記号,空白,*,*,　,　,*/*,　,0
	# after:  　, ,記号,空白,*,*,　,　,*/*, ,0
	for mo in li:
		if mo.hyouki == "　":  # full shape space
			mo.output = " "

	# before: ー,ー,名詞,一般,*,*,*,*,*,,,,,0
	# after:  ー,ー,名詞,一般,*,*,*,*,*,,,,ー,0
	for mo in li:
		if mo.hyouki == "ー" and mo.hinshi1 == "名詞":
			mo.hinshi1 = "記号"
			mo.output = "ー"

	# 数字の前の全角アポストロフィを半角にする
	# before:
	# ’,’,記号,括弧閉,*,*,’,’,*/*,’,0
	# ０,0,名詞,数,*,*,ゼロ,ゼロ,1/2,0,0
	# after:
	# ’,’,記号,括弧閉,*,*,’,’,*/*,',0
	# ０,0,名詞,数,*,*,ゼロ,ゼロ,1/2,0,0
	for pos in range(0, len(li) - 1):
		if li[pos].hyouki == "’" and li[pos + 1].hinshi2 == "数":
			li[pos].output = "'"

	# 算用数字ではさまれた読点を数符にする
	# before:
	# 二,二,名詞,数,*,*,2,2,1/2,2,0
	# 、,、,記号,読点,*,*,、,、,*/*,、,0
	# 三,三,名詞,数,*,*,3,3,1/2,3,0
	# after:
	# 二,二,名詞,数,*,*,2,2,1/2,2,0
	# 、,、,記号,読点,*,*,、,、,*/*,⠼,0
	# 三,三,名詞,数,*,*,3,3,1/2,3,0
	for pos in range(1, len(li) - 1):
		if li[pos - 1].output.isdigit() and li[pos].hyouki == "、" and li[pos + 1].output.isdigit():
			if nabcc:
				li[pos].output = "."
			else:
				li[pos].output = "⠼"

	# 算用数字ではさまれた中点を数符にする
	if not nabcc:
		for pos in range(1, len(li) - 1):
			if li[pos - 1].output.isdigit() and li[pos].hyouki == "・" and li[pos + 1].output.isdigit():
				li[pos].output = "⠼"

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
		if not mo.output and mo.nhyouki != "ー":
			if RE_KATAKANA.match(mo.nhyouki):
				mo.output = mo.nhyouki
			elif RE_HIRAGANA.match(mo.nhyouki):
				mo.output = "".join([chr(ord(c) + 0x60) for c in mo.nhyouki])
			elif RE_ASCII_AND_SYMBOLS.match(mo.nhyouki):
				# Fallback for ASCII letters/digits mixed with non-ASCII symbols
				# such as × (U+00D7): e.g. "a×b×c", "SEO×"
				# See https://github.com/nvdajp/nvdajp/issues/534
				mo.output = mo.nhyouki

	# 単語が小文字カタカナのみであれば修正
	# 表記は修正せず should_separate() で小文字として判定される
	for mo in li:
		if mo.output == "ァ":
			mo.output = "ア"
		if mo.output == "ィ":
			mo.output = "イ"
		if mo.output == "ゥ":
			mo.output = "ウ"
		if mo.output == "ェ":
			mo.output = "エ"
		if mo.output == "ォ":
			mo.output = "オ"
		if mo.output == "ッ":
			mo.output = "ツ"
		if mo.output == "ャ":
			mo.output = "ヤ"
		if mo.output == "ュ":
			mo.output = "ユ"
		if mo.output == "ョ":
			mo.output = "ヨ"
		if mo.output == "ヮ":
			mo.output = "ワ"
		if mo.output == "ヵ":
			mo.output = "カ"
		if mo.output == "ヶ":
			mo.output = "ケ"

	# 記号を Unicode 正規化
	# 踊り字の処理
	for i in range(0, len(li)):
		mo = li[i]
		if mo.hinshi1 == "記号" and mo.hinshi2 == "一般":
			if mo.hyouki == "〻":
				mo.output = "ニノジテン"
			elif mo.hyouki == "ゝ" and i > 0:
				mo.output = to_no_dakuon_kana(li[i - 1].output[-1:])
			elif mo.hyouki == "ゞ" and i > 0:
				mo.output = to_dakuon_kana(li[i - 1].output[-1:])
			elif mo.hyouki == "ヽ" and i > 0:
				mo.output = to_no_dakuon_kana(li[i - 1].output[-1:])
			elif mo.hyouki == "ヾ" and i > 0:
				mo.output = to_dakuon_kana(li[i - 1].output[-1:])
			elif mo.hyouki == "々々々々" and i > 0:
				mo.output = li[i - 1].output * 4
			elif mo.hyouki == "々々" and i > 0:
				mo.output = li[i - 1].output * 2
			elif mo.hyouki == "々" and i > 0:
				if li[i - 1].hyouki[0] == "々" and i > 1:
					mo.output = li[i - 2].output
				elif len(li[i - 1].hyouki) == 1:
					mo.output = li[i - 1].output
				else:
					mo.output = ""  # FIXME
			else:
				mo.output = mo.nhyouki
		if mo.hyouki == "．" and mo.hinshi1 == "名詞" and mo.hinshi2 == "数":
			mo.output = "."
		if mo.hyouki == "，" and mo.hinshi1 == "名詞" and mo.hinshi2 == "数":
			mo.output = ","
		if mo.hinshi1 == "記号" and mo.hinshi2 == "句点" and mo.nhyouki == ".":
			mo.output = "."
		if mo.hinshi1 == "記号" and mo.hinshi2 == "読点" and mo.nhyouki == ",":
			mo.output = ","

	for mo in li:
		mo.nhyouki = unicode_normalize(mo.nhyouki)
		# 情報処理点字の開始記号と終了記号
		info = False
		if RE_INFORMATION.match(mo.nhyouki) and "@" in mo.nhyouki and len(mo.nhyouki) > 1:
			info = True
		if "://" in mo.nhyouki:
			info = True
		if "\\" in mo.nhyouki:
			info = True
		if mo.nhyouki[0] == "[" and mo.nhyouki[-1] == "]":
			info = True
		if info:
			if nabcc:
				mo.output = mo.nhyouki
			else:
				mo.output = "⠠⠦" + mo.nhyouki + "⠠⠴"
		# 外国語引用符
		# 空白をはさまない1単語は外国語引用符ではなく外字符で
		elif (
			(RE_GAIJI.match(mo.nhyouki) and ((" " in mo.nhyouki) or ("'" in mo.nhyouki)))
			or (use_foreign_quotes and RE_GAIJI_WITH_PARENS.match(mo.nhyouki))
			or (("." in mo.nhyouki) and len(mo.nhyouki) > 3)
			or (
				# "0's", "80's"
				RE_DIGIT_SINGLE_ALPHA.match(mo.nhyouki)
			)
		):
			if nabcc:
				mo.output = mo.nhyouki
			else:
				mo.output = "⠦" + mo.nhyouki + "⠴"

	if not nabcc:
		for mo in li:
			# 情報処理点字でも外国語引用符でもなく output が & を含む場合は前後をあける
			if not mo.output.startswith("⠠⠦") and not mo.output.startswith("⠦"):
				# &
				if mo.output == "&":
					continue
				# &xx
				elif mo.output.startswith("&"):
					mo.output = mo.output.replace("&", "& ")
				# xx&
				elif mo.output.endswith("&"):
					mo.output = mo.output.replace("&", " &")
					# xx&xx
				else:
					mo.output = mo.output.replace("&", " & ")

	if nabcc:
		for mo in li:
			mo.output = mo.output.replace("”", '"').replace("’", "'").replace("‘", "`")

	# 日付の和語読み処理
	li = fix_japanese_date_morphs(li)

	# 日本語の直後のコンマを '、' で解釈
	# before: ，,記号,読点,*,*,*,*,，,，,，,*/*,*
	# after:  、,記号,読点,*,*,*,*,、,、,、,*/*,*
	for pos in range(len(li) - 1):
		mo = li[pos]
		mo2 = li[pos + 1]
		if mo2.hyouki == "，" and mo.hinshi2 not in ("アルファベット", "数", "括弧閉"):
			mo2.hyouki = mo2.nhyouki = mo2.output = "、"

	# 分かち書き判定
	for i in range(1, len(li)):
		prev2_mo = li[i - 2] if i - 2 >= 0 else None
		prev_mo = li[i - 1]
		next_mo = li[i + 1] if i + 1 < len(li) else None
		li[i - 1].sepflag = should_separate(prev2_mo, prev_mo, li[i], next_mo, nabcc=nabcc, logwrite=logwrite)

	# do not translate if string is unicode braille
	for i in range(0, len(li)):
		mo = li[i]
		if all((0x2800 <= ord(c) <= 0x28FF or c == "\u3000") for c in mo.hyouki):
			mo.output = mo.hyouki.replace("\u3000", " ")
			mo.sepflag = False
			if i > 0:
				li[i - 1].sepflag = False

	for mo in li:
		mo.write(logwrite)
	logwrite("")

	outbuf, inpos2 = morphs_to_string(li, inbuf, logwrite)

	# inpos2 holds positions in the normalized text; map them back to
	# positions in the original text.
	if nfkc_map:
		last = len(nfkc_map) - 1
		inpos2 = [nfkc_map[min(p, last)] for p in inpos2]

	if nabcc:
		outbuf = outbuf.replace(TAB_CODE, "⡀")
	else:
		outbuf = outbuf.replace(TAB_CODE, " ")

	return (outbuf, inpos2)


mecab_initialized = False
_analyzer = None


def initialize(analyzer=None, logwrite=_logwrite):
	"""Set the morphological analyzer (dependency injection).

	``analyzer`` must provide ``analyze(text, logwrite) -> list[str]``
	returning decoded MeCab-style feature lines, and ``is_ready() -> bool``.
	"""
	global mecab_initialized, _analyzer
	mecab_initialized = False
	if analyzer is None:
		raise ValueError("translator2.initialize() requires an analyzer")
	_analyzer = analyzer
	if logwrite:
		logwrite("initialize() done.")
	mecab_initialized = True


def terminate():
	global _logwrite
	if _logwrite:
		_logwrite("terminate() done.")
	global mecab_initialized, _analyzer
	mecab_initialized = False
	_analyzer = None


# 外国語引用符は ⠦ (U+2826) ... ⠴ (U+2834)。情報処理用 ⠠⠦...⠠⠴ は対象外。
FOREIGN_OPEN = "\u2826"  # ⠦
FOREIGN_CLOSE = "\u2834"  # ⠴
INFO_PREFIX = "\u2820"  # ⠠


def _louis_cells_to_braille_string(cells_str):
	"""liblouis translate の出力文字列を outbuf 用（スペース + U+280x）に変換する。"""
	result = []
	for c in cells_str:
		code = ord(c)
		if code == 0x20:
			result.append(" ")
		elif 0x2800 <= code <= 0x28FF:
			result.append(" " if code == 0x2800 else c)
		elif 0x8000 <= code <= 0x80FF:
			cell = code & 0xFF
			result.append(" " if cell == 0 else chr(0x2800 + cell))
		else:
			cell = code & 0xFF
			result.append(" " if cell == 0 else chr(0x2800 + cell))
	return "".join(result).replace("\u2800", " ")


def _find_foreign_quote_ranges(outbuf):
	"""情報処理用 ⠠⠦...⠠⠴ を除外して、外国語引用符の inner 範囲を返す。"""
	i = 0
	ranges = []
	while i < len(outbuf):
		open_idx = outbuf.find(FOREIGN_OPEN, i)
		while open_idx > 0 and outbuf[open_idx - 1] == INFO_PREFIX:
			open_idx = outbuf.find(FOREIGN_OPEN, open_idx + 1)
		if open_idx < 0:
			break
		close_search = open_idx + 1
		close_idx = -1
		while True:
			cand = outbuf.find(FOREIGN_CLOSE, close_search)
			if cand < 0:
				break
			if cand == 0 or outbuf[cand - 1] != INFO_PREFIX:
				close_idx = cand
				break
			close_search = cand + 1
		if close_idx < 0:
			break
		ranges.append((open_idx + 1, close_idx))
		i = close_idx + 1
	return ranges


def _map_louis_positions(old_segment_inpos, louis_in_pos, louis_out_pos, new_len):
	"""louis の inPos/outPos を使って inner 置換後の inpos2 セグメントを作る。"""
	if new_len <= 0:
		return []
	if not old_segment_inpos:
		return [0] * new_len
	max_input_idx = len(old_segment_inpos) - 1
	louis_in_pos = list(louis_in_pos) if louis_in_pos else []
	louis_out_pos = list(louis_out_pos) if louis_out_pos else []
	result = []

	def _fallback_from_out_pos(out_idx):
		if not louis_out_pos:
			return None
		candidate = 0
		for in_idx, mapped_out in enumerate(louis_out_pos):
			if mapped_out <= out_idx:
				candidate = in_idx
			else:
				break
		return candidate

	for out_idx in range(new_len):
		src_idx = louis_in_pos[out_idx] if out_idx < len(louis_in_pos) else None
		if src_idx is None or src_idx < 0:
			src_idx = _fallback_from_out_pos(out_idx)
		if src_idx is None:
			src_idx = 0 if new_len == 1 else (out_idx * max_input_idx) // (new_len - 1)
		src_idx = max(0, min(max_input_idx, int(src_idx)))
		result.append(old_segment_inpos[src_idx])
	return result


def _is_us_g2_louis_table(louisTableList):
	return any(str(table).replace("\\", "/").endswith("en-us-g2.ctb") for table in louisTableList)


def _should_skip_us_g2_louis_for_inner(inner):
	return RE_US_G2_DOTTED_TOKEN.match(inner) is not None


def _apply_louis_to_foreign_quotes(outbuf, inpos2, louisTranslate, louisTableList):
	"""outbuf 内の ⠦...⠴ の内側を louisTranslate(louisTableList, inner) で2級変換し、outbuf と inpos2 を更新する。"""
	inpos2 = list(inpos2)
	is_us_g2 = _is_us_g2_louis_table(louisTableList)
	try:
		import louis as _louis

		mode = getattr(_louis, "dotsIO", 0)
	except Exception:
		mode = 0
	ranges = _find_foreign_quote_ranges(outbuf)  # inner ranges (start..end, end exclusive)
	# Process from end to start so indices stay valid
	for start, end in reversed(ranges):
		inner = outbuf[start:end]
		if is_us_g2 and _should_skip_us_g2_louis_for_inner(inner):
			continue
		try:
			braille_out, louis_in_pos, louis_out_pos, _cur = louisTranslate(
				louisTableList,
				inner,
				cursorPos=0,
				mode=mode,
			)
		except Exception:
			continue  # leave this segment as-is on louis error
		grade2_str = _louis_cells_to_braille_string(braille_out)
		new_len = len(grade2_str)
		old_segment_inpos = inpos2[start:end] if start < len(inpos2) else []
		new_segment = _map_louis_positions(old_segment_inpos, louis_in_pos, louis_out_pos, new_len)
		outbuf = outbuf[:start] + grade2_str + outbuf[end:]
		inpos2 = inpos2[:start] + new_segment + inpos2[end:]
	return (outbuf, inpos2)


def translateWithInPos2(
	inbuf,
	logwrite=_logwrite,
	nabcc=False,
	louisTranslate=None,
	louisTableList=None,
	use_foreign_quotes=False,
):
	if not mecab_initialized or _analyzer is None or not _analyzer.is_ready():
		raise RuntimeError("translator2 is not initialized; call initialize(analyzer=...)")
	# do not translate if string is unicode braille
	if all((0x2800 <= ord(c) <= 0x28FF or c == " ") for c in inbuf):
		outbuf = inbuf
		inpos2 = [n for n in range(len(inbuf))]
		already_braille = True
	else:
		outbuf, inpos2 = japanese_braille_separate(
			inbuf, logwrite, nabcc=nabcc, use_foreign_quotes=use_foreign_quotes
		)
		already_braille = False
	# nvdajp: translator_louis — 外国語引用符内を liblouis 2級に変換。既に点字の入力はスキップ（no-op で位置がずれないように）。
	if louisTranslate is not None and louisTableList and not already_braille:
		outbuf, inpos2 = _apply_louis_to_foreign_quotes(outbuf, inpos2, louisTranslate, louisTableList)
	result, inpos1 = translator1.translateWithInPos(outbuf, nabcc=nabcc)
	result = result.replace("□", " ")
	return (outbuf, result, inpos1, inpos2)


# for brailleViewer
def getReadingAndBraille(text, logwrite=_logwrite, nabcc=False):
	return translateWithInPos2(text, logwrite=logwrite, nabcc=nabcc)[0:2]


# returns '\u2801\u2802\u2803\u2804\u2805\u2806\u2807'
def japaneseToUnicodeBraille(text, logwrite=_logwrite, nabcc=False):
	return translateWithInPos2(text, logwrite=logwrite, nabcc=nabcc)[0]


def makeOutPos(inPos, inlen, outlen):
	# make outPos
	outPos = [-1] * inlen
	for p in range(outlen - 1, -1, -1):
		if inPos[p] < len(outPos):
			outPos[inPos[p]] = p
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
		inPos[p] = inpos2[inpos1[p]]
	outPos = makeOutPos(inPos, inlen, outlen)
	return inPos, outPos


# louis-compatible method
# tableList, typeform are not supported.
# mode=dotsIO is default.
def translate(
	inbuf,
	cursorPos=0,
	logwrite=_logwrite,
	unicodeIO=False,
	nabcc=False,
	louisTranslate=None,
	louisTableList=None,
	use_foreign_quotes=False,
):
	"""Translate a string of characters, providing position information.
	@param inbuf: The string to translate.
	@type inbuf: str
	@param cursorPos: The position of the cursor in inbuf.
	@type cursorPos: int
	@param louisTranslate: If provided with louisTableList, 外国語引用符内をこの関数で2級変換する。
	@param louisTableList: e.g. ["en-ueb-g2.ctb"]
	@return: A tuple of:
	        the translated string,
	        a list of input positions for each position in the output,
	        a list of output positions for each position in the input, and
	        the position of the cursor in the output.
	@rtype: (str, list of int, list of int, int)
	@raise RuntimeError: If a complete translation could not be done.
	"""
	sp, outbuf, inpos1, inpos2 = translateWithInPos2(
		inbuf,
		logwrite=logwrite,
		nabcc=nabcc,
		louisTranslate=louisTranslate,
		louisTableList=louisTableList,
		use_foreign_quotes=use_foreign_quotes,
	)
	if not unicodeIO:
		pat = outbuf.replace(" ", "\u2800")
		outbuf = "".join([chr((ord(c) - 0x2800) + 0x8000) for c in pat])
	inPos, outPos = mergePositionMap(inpos1, inpos2, len(outbuf), len(inbuf))
	cursorPos = outPos[cursorPos]
	return (outbuf, inPos, outPos, cursorPos)
