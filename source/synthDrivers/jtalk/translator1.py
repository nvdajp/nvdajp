# coding: UTF-8
# translator1.py (Japanese Braille translator Phase 1)
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012 Masataka.Shinke, Takuya Nishimoto
# Copyright (C) 2013 Takuya Nishimoto (NVDA Japanese Team)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.


import unicodedata
from copy import deepcopy

kana1_dic = {
	"ア": "⠁",
	"イ": "⠃",
	"ウ": "⠉",
	"エ": "⠋",
	"オ": "⠊",
	"カ": "⠡",
	"キ": "⠣",
	"ク": "⠩",
	"ケ": "⠫",
	"コ": "⠪",
	"サ": "⠱",
	"シ": "⠳",
	"ス": "⠹",
	"セ": "⠻",
	"ソ": "⠺",
	"タ": "⠕",
	"チ": "⠗",
	"ツ": "⠝",
	"テ": "⠟",
	"ト": "⠞",
	"ナ": "⠅",
	"ニ": "⠇",
	"ヌ": "⠍",
	"ネ": "⠏",
	"ノ": "⠎",
	"ハ": "⠥",
	"ヒ": "⠧",
	"フ": "⠭",
	"ヘ": "⠯",
	"ホ": "⠮",
	"マ": "⠵",
	"ミ": "⠷",
	"ム": "⠽",
	"メ": "⠿",
	"モ": "⠾",
	"ヤ": "⠌",
	"ユ": "⠬",
	"ヨ": "⠜",
	"ラ": "⠑",
	"リ": "⠓",
	"ル": "⠙",
	"レ": "⠛",
	"ロ": "⠚",
	"ワ": "⠄",
	"ヰ": "⠆",
	"ヱ": "⠖",
	"ヲ": "⠔",
	"ン": "⠴",
	"ッ": "⠂",
	"ヴ": "⠐⠉",
	"ガ": "⠐⠡",
	"ギ": "⠐⠣",
	"グ": "⠐⠩",
	"ゲ": "⠐⠫",
	"ゴ": "⠐⠪",
	"ザ": "⠐⠱",
	"ジ": "⠐⠳",
	"ズ": "⠐⠹",
	"ゼ": "⠐⠻",
	"ゾ": "⠐⠺",
	"ダ": "⠐⠕",
	"ヂ": "⠐⠗",
	"ヅ": "⠐⠝",
	"デ": "⠐⠟",
	"ド": "⠐⠞",
	"バ": "⠐⠥",
	"ビ": "⠐⠧",
	"ブ": "⠐⠭",
	"ベ": "⠐⠯",
	"ボ": "⠐⠮",
	"パ": "⠠⠥",
	"ピ": "⠠⠧",
	"プ": "⠠⠭",
	"ペ": "⠠⠯",
	"ポ": "⠠⠮",
}
kana2_dic = {
	"イェ": "⠈⠋",
	"キャ": "⠈⠡",
	"キュ": "⠈⠩",
	"キェ": "⠈⠫",
	"キョ": "⠈⠪",
	"シャ": "⠈⠱",
	"スィ": "⠈⠳",
	"シュ": "⠈⠹",
	"シェ": "⠈⠻",
	"ショ": "⠈⠺",
	"チャ": "⠈⠕",
	"ティ": "⠈⠗",
	"チュ": "⠈⠝",
	"チェ": "⠈⠟",
	"チョ": "⠈⠞",
	"ニャ": "⠈⠅",
	"ニュ": "⠈⠍",
	"ニェ": "⠈⠏",
	"ニョ": "⠈⠎",
	"ヒャ": "⠈⠥",
	"ヒュ": "⠈⠭",
	"ヒェ": "⠈⠯",
	"ヒョ": "⠈⠮",
	"ミャ": "⠈⠵",
	"ミュ": "⠈⠽",
	"ミェ": "⠈⠿",
	"ミョ": "⠈⠾",
	"リャ": "⠈⠑",
	"リュ": "⠈⠙",
	"リェ": "⠈⠛",
	"リョ": "⠈⠚",
	"ギャ": "⠘⠡",
	"ギュ": "⠘⠩",
	"ギェ": "⠘⠫",
	"ギョ": "⠘⠪",
	"ジャ": "⠘⠱",
	"ズィ": "⠘⠳",
	"ジュ": "⠘⠹",
	"ジェ": "⠘⠻",
	"ジョ": "⠘⠺",
	"ヂャ": "⠘⠕",
	"ディ": "⠘⠗",
	"ヂュ": "⠘⠝",
	"ヂェ": "⠘⠟",
	"ヂョ": "⠘⠞",
	"ビャ": "⠘⠥",
	"ビュ": "⠘⠭",
	"ビェ": "⠘⠯",
	"ビョ": "⠘⠮",
	"テュ": "⠨⠝",
	"ピャ": "⠨⠥",
	"ピュ": "⠨⠭",
	"ピョ": "⠨⠮",
	"フュ": "⠨⠬",
	"フョ": "⠨⠜",
	"デュ": "⠸⠝",
	"ヴュ": "⠸⠬",
	"ヴョ": "⠸⠜",
	"ウァ": "⠢⠁",
	"ウィ": "⠢⠃",
	"ウェ": "⠢⠋",
	"ウォ": "⠢⠊",
	"クァ": "⠢⠡",
	"クィ": "⠢⠣",
	"クェ": "⠢⠫",
	"クォ": "⠢⠪",
	"ツァ": "⠢⠕",
	"ツィ": "⠢⠗",
	"トゥ": "⠢⠝",
	"ツェ": "⠢⠟",
	"ツォ": "⠢⠞",
	"ファ": "⠢⠥",
	"フィ": "⠢⠧",
	"フェ": "⠢⠯",
	"フォ": "⠢⠮",
	"グァ": "⠲⠡",
	"グィ": "⠲⠣",
	"グェ": "⠲⠫",
	"グォ": "⠲⠪",
	"ヅァ": "⠲⠕",
	"ヅィ": "⠲⠗",
	"ドゥ": "⠲⠝",
	"ヅェ": "⠲⠟",
	"ヅォ": "⠲⠞",
	"ヴァ": "⠲⠥",
	"ヴィ": "⠲⠧",
	"ヴェ": "⠲⠯",
	"ヴォ": "⠲⠮",
}
info_symbol_dic = {
	"!": "⠖",
	'"': "⠶",
	"#": "⠩",
	"$": "⠹",
	"%": "⠻",
	"&": "⠯",
	"'": "⠄",
	"(": "⠦",
	")": "⠴",
	"*": "⠡",
	"+": "⠬",
	",": "⠂",
	"-": "⠤",
	".": "⠲",
	"/": "⠌",
	":": "⠐⠂",
	";": "⠆",
	"<": "⠔⠔",
	"=": "⠒⠒",
	">": "⠢⠢",
	"?": "⠐⠦",
	"@": "⠪",
	"[": "⠷",
	"\\": "⠫",  # yen mark
	"]": "⠾",
	"^": "⠘",
	"_": "⠐⠤",
	"`": "⠐⠑",
	"{": "⠣",
	"|": "⠳",
	"}": "⠜",
	"~": "⠐⠉",
}
jp_symbol_dic = deepcopy(info_symbol_dic)
jp_symbol_dic.update(
	{
		"+": "⠢",
		"-": "⠤",
		":": "⠐⠂",
		"\\": "⠫",  # yen mark
		"?": "⠢ ",  # one space
		"@": "⠰⠪",
		"<": "⠔⠔",
		">": "⠢⠢",
		"=": "⠒⠒",
		"#": "⠰⠩",
		"$": "⠹",
		"%": "⠰⠏",
		"&": "⠰⠯",
		"*": "⠰⠡",
		";": "⠆",
		"|": "⠳",
		'"': "⠶",
		# "'":'⠄',
		#'/':'⠌',
		".": "⠲",
		"!": "⠖ ",  # one space
		"^": "⠘",
		"`": "⠐⠑",
		"_": "⠐⠤",
		"~": "⠐⠉",
		"ー": "⠒",
		"、": "⠰ ",  # one space
		"。": "⠲  ",  # two spaces
		"・": "⠐ ",  # one space
		"｜": "⠶",
		"＿": "⠤",
		"「": "⠤",
		"」": "⠤",
		"『": "⠰⠤",
		"』": "⠤⠆",
		"｢": "⠤",
		"｣": "⠤",
		"(": "⠶",
		")": "⠶",
		"（": "⠶",
		"）": "⠶",
		"[": "⠐⠶",
		"]": "⠶⠂",
		"“": "⠐⠶",
		"”": "⠶⠂",
		"{": "⠐⠶",
		"}": "⠶⠂",
		"‘": "⠐⠶",
		"’": "⠶⠂",
		"〔": "⠐⠶",
		"〕": "⠶⠂",
		"〈": "⠐⠶",
		"〉": "⠶⠂",
		"《": "⠐⠶",
		"》": "⠶⠂",
		"【": "⠐⠶",
		"】": "⠶⠂",
		"〝": "⠐⠶",
		"〟": "⠶⠂",
		"☆": "⠰⠮⠂",
		"★": "⠰⠮⠆",
		"○": "⠠⠵⠂",
		"●": "⠠⠵⠆",
		"◎": "⠠⠵⠲",
		"□": "⠠⠳⠂",
		"■": "⠠⠳⠆",
		"△": "⠠⠱⠂",
		"▲": "⠠⠱⠆",
		"▽": "⠰⠱⠂",
		"×": "⠰⠡⠂",
		"▼": "⠰⠱⠆",
		"◇": "⠨⠧⠂",
		"◆": "⠨⠧⠆",
		"※": "⠔⠔ ",  # 第1星印 35-35 (後ろを1マスあける)
		"→": " ⠒⠒⠕ ",  # 矢印 前後に1マスあける
		"←": " ⠪⠒⠒ ",  # 矢印 前後に1マスあける
		",": "⠄",
		"〒": "⠰⠶⠬⠒⠐⠧⠴ ⠐⠥⠴⠐⠪⠒⠶⠆",  # ⠰⠶ユービン バンゴー⠶⠆
	},
)
num_dic = {
	"0": "⠚",
	"1": "⠁",
	"2": "⠃",
	"3": "⠉",
	"4": "⠙",
	"5": "⠑",
	"6": "⠋",
	"7": "⠛",
	"8": "⠓",
	"9": "⠊",
}
num_symbol_dic = {
	".": "⠂",
	",": "⠄",
}
alpha_symbol_dic = deepcopy(info_symbol_dic)
alpha_symbol_dic.update(
	{
		".": "⠲",
		",": "⠂",
		"'": "⠄",
		"?": "⠦",
		"!": "⠖",
		"(": "⠶",
		")": "⠶",
		"/": "⠌",
		"+": "⠢",
		"%": "⠰⠏",
		"*": "⠔⠔",
		"@": "⠪",
	},
)
alpha_dic = {
	"a": "⠁",
	"b": "⠃",
	"c": "⠉",
	"d": "⠙",
	"e": "⠑",
	"f": "⠋",
	"g": "⠛",
	"h": "⠓",
	"i": "⠊",
	"j": "⠚",
	"k": "⠅",
	"l": "⠇",
	"m": "⠍",
	"n": "⠝",
	"o": "⠕",
	"p": "⠏",
	"q": "⠟",
	"r": "⠗",
	"s": "⠎",
	"t": "⠞",
	"u": "⠥",
	"v": "⠧",
	"w": "⠺",
	"x": "⠭",
	"y": "⠽",
	"z": "⠵",
}
alpha_cap_dic = {
	"A": "⠁",
	"B": "⠃",
	"C": "⠉",
	"D": "⠙",
	"E": "⠑",
	"F": "⠋",
	"G": "⠛",
	"H": "⠓",
	"I": "⠊",
	"J": "⠚",
	"K": "⠅",
	"L": "⠇",
	"M": "⠍",
	"N": "⠝",
	"O": "⠕",
	"P": "⠏",
	"Q": "⠟",
	"R": "⠗",
	"S": "⠎",
	"T": "⠞",
	"U": "⠥",
	"V": "⠧",
	"W": "⠺",
	"X": "⠭",
	"Y": "⠽",
	"Z": "⠵",
}


def _dots_to_braille(dots: str) -> str:
	"""Convert a dot-number string such as "1247" to a Unicode braille
	character. Dots 1-8 map to bits 0-7 of the braille cell value."""
	cell = 0
	for d in dots:
		cell |= 1 << (int(d) - 1)
	return chr(0x2800 + cell)


# Cyrillic (Russian) letters. nvdajp-specific rendering (nvdajp issue #224):
# lowercase letters use the international Russian braille patterns and
# capital letters add dot 7, without any enclosure symbols.
# The specification is described in user_docs/ja/readmejp.md.
# Keys are lowercase letters; capitals are derived in make_cyrillic_dic().
_cyrillic_lower_dots = {
	"\u0430": "1",  # CYRILLIC SMALL LETTER A
	"\u0431": "12",  # CYRILLIC SMALL LETTER BE
	"\u0432": "2456",  # CYRILLIC SMALL LETTER VE
	"\u0433": "1245",  # CYRILLIC SMALL LETTER GHE
	"\u0434": "145",  # CYRILLIC SMALL LETTER DE
	"\u0435": "15",  # CYRILLIC SMALL LETTER IE
	"\u0451": "16",  # CYRILLIC SMALL LETTER IO
	"\u0436": "245",  # CYRILLIC SMALL LETTER ZHE
	"\u0437": "1356",  # CYRILLIC SMALL LETTER ZE
	"\u0438": "24",  # CYRILLIC SMALL LETTER I
	"\u0439": "12346",  # CYRILLIC SMALL LETTER SHORT I
	"\u043a": "13",  # CYRILLIC SMALL LETTER KA
	"\u043b": "123",  # CYRILLIC SMALL LETTER EL
	"\u043c": "134",  # CYRILLIC SMALL LETTER EM
	"\u043d": "1345",  # CYRILLIC SMALL LETTER EN
	"\u043e": "135",  # CYRILLIC SMALL LETTER O
	"\u043f": "1234",  # CYRILLIC SMALL LETTER PE
	"\u0440": "1235",  # CYRILLIC SMALL LETTER ER
	"\u0441": "234",  # CYRILLIC SMALL LETTER ES
	"\u0442": "2345",  # CYRILLIC SMALL LETTER TE
	"\u0443": "136",  # CYRILLIC SMALL LETTER U
	"\u0444": "124",  # CYRILLIC SMALL LETTER EF
	"\u0445": "125",  # CYRILLIC SMALL LETTER HA
	"\u0446": "14",  # CYRILLIC SMALL LETTER TSE
	"\u0447": "12345",  # CYRILLIC SMALL LETTER CHE
	"\u0448": "156",  # CYRILLIC SMALL LETTER SHA
	"\u0449": "1346",  # CYRILLIC SMALL LETTER SHCHA
	"\u044a": "12356",  # CYRILLIC SMALL LETTER HARD SIGN
	"\u044b": "2346",  # CYRILLIC SMALL LETTER YERU
	"\u044c": "23456",  # CYRILLIC SMALL LETTER SOFT SIGN
	"\u044d": "246",  # CYRILLIC SMALL LETTER E
	"\u044e": "1256",  # CYRILLIC SMALL LETTER YU
	"\u044f": "1246",  # CYRILLIC SMALL LETTER YA
	"\u0463": "345",  # CYRILLIC SMALL LETTER YAT
	"\u046b": "246",  # CYRILLIC SMALL LETTER BIG YUS
}


def make_cyrillic_dic() -> dict[str, str]:
	dic = {}
	for lower, dots in _cyrillic_lower_dots.items():
		dic[lower] = _dots_to_braille(dots)
		upper = lower.upper()
		if upper != lower:
			dic[upper] = _dots_to_braille(dots + "7")
	return dic


cyrillic_dic = make_cyrillic_dic()


def is_ara(c: str) -> bool:
	# 数字の後につなぎ符が必要
	return c in "アイウエオラリルレロ"


def make_nabcc_dic() -> dict[str, str]:
	dic = {}
	for c in alpha_dic:
		dic[c] = alpha_dic[c]
	keys = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ,;:.!\"'()-_<=>%+~`&$?{[}]^@#\\|/*"
	vals = "⠴⠂⠆⠒⠲⠢⠖⠶⠦⠔⡁⡃⡉⡙⡑⡋⡛⡓⡊⡚⡅⡇⡍⡝⡕⡏⡟⡗⡎⡞⡥⡧⡺⡭⡽⡵⠠⠰⠱⠨⠮⠐⠄⠷⠾⠤⠸⠣⠿⠜⠩⠬⠘⠈⠯⠫⠹⠪⡪⠻⡻⡘⡈⠼⡳⠳⠌⠡"
	for pos in range(len(keys)):
		dic[keys[pos]] = vals[pos]
	return dic


nabcc_dic = make_nabcc_dic()


def translateWithInPos(text: str, nabcc: bool = False) -> tuple[str, list[int]]:
	retval = ""
	pos = 0
	latin = False  # 外字符モード
	latin_sym = False  # 外国語の記号の直後
	num = False  # 数符モード
	capital = False  # 二重大文字符モード
	quote_mode = False  # 外国語引用符モード
	info_mode = False  # 情報処理点字モード
	text = unicodedata.normalize("NFKC", text)
	inPos: list[int] = []

	while pos < len(text):
		# space
		if text[pos] == " ":
			retval += " "
			inPos.append(pos)
			capital = latin = num = False
			latin_sym = False
			pos += 1
		# alpha_symbol_dic (comma in quote)
		elif quote_mode and not info_mode and text[pos] in alpha_symbol_dic:
			a = alpha_symbol_dic[text[pos]]
			retval += a
			inPos.extend([pos] * len(a))
			latin_sym = True
			pos += 1
		# alpha_symbol_dic (comma in latin or capital)
		elif (latin or capital) and not info_mode and text[pos] in alpha_symbol_dic:
			t = text[pos]
			a = alpha_symbol_dic[t]
			retval += a
			inPos.extend([pos] * len(a))
			capital = False
			if t not in ("/",):
				latin = False
			latin_sym = True
			pos += 1
		# nabcc
		elif nabcc and (text[pos] in nabcc_dic):
			retval += nabcc_dic[text[pos]]
			inPos.append(pos)
			latin_sym = False
			pos += 1
		# Numeric
		elif text[pos] in num_dic:
			latin = False
			latin_sym = False
			if not num:
				retval += "⠼"
				inPos.append(pos)
				num = True
			while text[pos] in num_dic:
				retval += num_dic[text[pos]]
				inPos.extend([pos] * len(num_dic[text[pos]]))
				pos += 1
				if pos >= len(text):
					break
		# info symbol
		elif info_mode and text[pos] in info_symbol_dic:
			retval += info_symbol_dic[text[pos]]
			inPos.extend([pos] * len(info_symbol_dic[text[pos]]))
			if text[pos] not in (",", "."):
				num = False
			capital = False
			latin_sym = False
			pos += 1
		# Numeric symbols
		elif (
			num
			and (text[pos] in num_symbol_dic)
			and ((pos == len(text) - 1) or (pos + 1 < len(text) and text[pos + 1].isdigit()))
		):
			retval += num_symbol_dic[text[pos]]
			inPos.extend([pos] * len(num_symbol_dic[text[pos]]))
			latin_sym = False
			pos += 1
		# halfshape apostrophe symbol
		elif text[pos] == "'":
			if pos + 1 < len(text) and text[pos + 1].isdigit():
				retval += "⠼⠄"
				inPos.extend([pos, pos])
				num = True
			latin_sym = False
			pos += 1
		# slash symbol
		elif text[pos] == "/":
			retval += "⠌"
			inPos.append(pos)
			num = capital = False
			latin_sym = False
			pos += 1
		# Japanese symbols
		elif text[pos] in jp_symbol_dic and not (quote_mode or info_mode):
			retval += jp_symbol_dic[text[pos]]
			inPos.extend([pos] * len(jp_symbol_dic[text[pos]]))
			latin = num = False
			latin_sym = False
			pos += 1
		# lower/upper case alphabet
		elif text[pos] in alpha_dic or text[pos] in alpha_cap_dic:
			if not latin and not quote_mode:
				retval += "⠰"
				inPos.append(pos)
			elif (
				(info_mode or quote_mode)
				and pos >= 1
				and text[pos - 1].isdigit()
				and text[pos] in "abcdefghij"
			):
				# 外国語引用符または情報処理で数字のあとにａ～ｊが続くときは小文字フラグ
				retval += "⠰"
				inPos.append(pos)
			elif (
				info_mode
				and pos >= 2
				and text[pos - 2].isdigit()
				and text[pos - 1] == "."
				and text[pos] in "abcdefghij"
			):
				# 情報処理で数字、ピリオドのあとにａ～ｊが続くときは小文字フラグ
				retval += "⠰"
				inPos.append(pos)
			latin = True
			num = False
			# 大文字または小文字が続く範囲の終点を tpos に格納
			tpos = pos
			upper_count = lower_count = 0
			while tpos < len(text):
				if text[tpos] in alpha_cap_dic:
					upper_count += 1
					tpos += 1
				elif text[tpos] in alpha_dic:
					lower_count += 1
					tpos += 1
				else:
					break
			# 大文字だけが2文字以上連続する場合は二重大文字符
			if upper_count > 1 and lower_count == 0:
				retval += "⠠⠠"
				inPos.extend([pos, pos])
				capital = True
			else:
				capital = False
			# アルファベットの続く部分を変換
			while pos < tpos:
				if not capital and text[pos] in alpha_cap_dic:
					retval += "⠠"
					inPos.append(pos)
				retval += alpha_dic[text[pos].lower()]
				inPos.append(pos)
				pos += 1
			latin_sym = False
		# Two kana characters
		elif pos + 1 < len(text) and text[pos : pos + 2] in kana2_dic:
			if latin and not latin_sym:
				retval += "⠤"
				inPos.append(pos - 1)  # つなぎ符は直前の文字に対応
			elif num and is_ara(text[pos : pos + 1]):
				retval += "⠤"
				inPos.append(pos - 1)  # つなぎ符は直前の文字に対応
			retval += kana2_dic[text[pos : pos + 2]]
			inPos.extend([pos, pos + 1])
			latin = num = False
			latin_sym = False
			pos += 2
		# One kana character
		elif text[pos] in kana1_dic:
			if latin and not latin_sym:
				retval += "⠤"
				inPos.append(pos - 1)  # つなぎ符は直前の文字に対応
			elif num:
				if is_ara(text[pos]):
					retval += "⠤"
					inPos.append(pos - 1)  # つなぎ符は直前の文字に対応
				elif (
					text[pos] == "ワ"
					and pos + 3 < len(text)
					and is_ara(text[pos + 1])
					and is_ara(text[pos + 2])
					and is_ara(text[pos + 3])
				):
					retval += "⠤"
					inPos.append(pos - 1)  # つなぎ符は直前の文字に対応
			retval += kana1_dic[text[pos]]
			inPos.extend([pos] * len(kana1_dic[text[pos]]))
			latin = num = False
			latin_sym = False
			pos += 1
		# Braille should not be changed
		elif 0x2800 <= ord(text[pos]) and ord(text[pos]) <= 0x28FF:
			latin = False
			# 数字モード
			if text[pos] == "⠼":
				num = True
			else:
				num = False
			# 外国語引用符モード切替
			if not quote_mode and text[pos] == "⠦":
				quote_mode = True
			if quote_mode and text[pos] == "⠴":
				quote_mode = False
			# 情報処理モード切替
			if text[pos] == "⠠" and pos + 1 < len(text):
				if text[pos + 1] == "⠦":
					info_mode = True
				elif text[pos + 1] == "⠴":
					info_mode = False

			if ord(text[pos]) == 0x2800:
				retval += " "  # use 0x20
				inPos.append(pos)
			else:
				retval += text[pos]
				inPos.append(pos)
			latin_sym = False
			pos += 1
		# Cyrillic letters: Russian braille patterns, capitals add dot 7,
		# no enclosure symbols (nvdajp-specific). nvdajp issue #224
		elif text[pos] in cyrillic_dic:
			retval += cyrillic_dic[text[pos]]
			inPos.append(pos)
			latin = num = False
			latin_sym = False
			pos += 1
		# Exception
		else:
			latin = num = False
			latin_sym = False
			retval += "□"
			inPos.append(pos)
			pos += 1
	# rstrip with inPos
	outbuf = retval
	if text and text[-1] != " ":
		while outbuf[-1:] == " ":
			outbuf = outbuf[:-1]
			inPos.pop()
	return (outbuf, inPos)
