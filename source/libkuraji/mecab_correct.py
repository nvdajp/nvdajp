# coding: UTF-8
# mecab_correct.py
# Copyright (C) 2010-2026 Takuya Nishimoto
# License: BSD 3-Clause. See LICENSE.
#
# Originally part of NVDA Japanese (nvdajp), covered by the GPL.
# Re-licensed to BSD 3-Clause by the copyright holder for libkuraji.
#
# This module post-processes raw MeCab feature lines to match the
# analysis recorded in tests/mecabFixture.json. It implements the same
# corrections as nvdajp's Mecab_correctFeatures, but operates on
# list[str] (one CSV feature line per morpheme) instead of the ctypes
# MeCab wrapper, so it works with fugashi.

import re
import unicodedata
from typing import Optional

# romanji -> katakana table (from roma2kana.py, re-licensed BSD)
_romadic = [
	["ccha", "ッチャ", 2], ["cchi", "ッチ", 2], ["cchu", "ッチュ", 2],
	["cche", "ッチェ", 2], ["ccho", "ッチョ", 2],
	["bba", "ッバ", 2], ["bbi", "ッビ", 2], ["bbu", "ッブ", 2],
	["bbe", "ッベ", 2], ["bbo", "ッボ", 2],
	["dda", "ッダ", 2], ["ddi", "ッジ", 2], ["ddu", "ッヅ", 2],
	["dde", "ッデ", 2], ["ddo", "ッド", 2],
	["ffa", "ッファ", 2], ["ffi", "ッフィ", 2], ["ffu", "ッフ", 2],
	["ffe", "ッフェ", 2], ["ffo", "ッフォ", 2],
	["gga", "ッガ", 2], ["ggi", "ッギ", 2], ["ggu", "ッグ", 2],
	["gge", "ッゲ", 2], ["ggo", "ッゴ", 2],
	["hha", "ッハ", 2], ["hhi", "ッヒ", 2], ["hhu", "ッフ", 2],
	["hhe", "ッヘ", 2], ["hho", "ッホ", 2],
	["jja", "ッジャ", 2], ["jji", "ッジ", 2], ["jju", "ッジュ", 2],
	["jje", "ッジェ", 2], ["jjo", "ッジョ", 2],
	["kka", "ッカ", 2], ["kki", "ッキ", 2], ["kku", "ック", 2],
	["kke", "ッケ", 2], ["kko", "ッコ", 2],
	["ppa", "ッパ", 2], ["ppi", "ッピ", 2], ["ppu", "ップ", 2],
	["ppe", "ッペ", 2], ["ppo", "ッポ", 2],
	["ssa", "ッサ", 2], ["ssi", "ッシ", 2], ["ssu", "ッス", 2],
	["sse", "ッセ", 2], ["sso", "ッソ", 2],
	["tta", "ッタ", 2], ["tti", "ッチ", 2], ["ttu", "ッツ", 2],
	["tte", "ッテ", 2], ["tto", "ット", 2],
	["zza", "ッザ", 2], ["zzi", "ッジ", 2], ["zzu", "ッズ", 2],
	["zze", "ッゼ", 2], ["zzo", "ッゾ", 2],
	["cha", "チャ", 1], ["chu", "チュ", 1], ["cho", "チョ", 1],
	["tsu", "ツ", 1],
	["tya", "チャ", 1], ["tyu", "チュ", 1], ["tyo", "チョ", 1],
	["jya", "ジャ", 1], ["jyu", "ジュ", 1], ["jyo", "ジョ", 1],
	["kya", "キャ", 1], ["kyu", "キュ", 1], ["kyo", "キョ", 1],
	["gya", "ギャ", 1], ["gyu", "ギュ", 1], ["gyo", "ギョ", 1],
	["shi", "シ", 1],
	["sya", "シャ", 1], ["syu", "シュ", 1], ["syo", "ショ", 1],
	["sha", "シャ", 1], ["shu", "シュ", 1], ["sho", "ショ", 1],
	["chi", "チ", 1],
	["nya", "ニャ", 1], ["nyu", "ニュ", 1], ["nyo", "ニョ", 1],
	["hya", "ヒャ", 1], ["hyu", "ヒュ", 1], ["hyo", "ヒョ", 1],
	["pya", "ピャ", 1], ["pyu", "ピュ", 1], ["pyo", "ピョ", 1],
	["mya", "ミャ", 1], ["myu", "ミュ", 1], ["myo", "ミョ", 1],
	["rya", "リャ", 1], ["ryu", "リュ", 1], ["ryo", "リョ", 1],
	["sa", "サ", 1], ["si", "シ", 1], ["ka", "カ", 1], ["ki", "キ", 1],
	["ku", "ク", 1], ["ke", "ケ", 1], ["ko", "コ", 1],
	["ga", "ガ", 1], ["gi", "ギ", 1], ["gu", "グ", 1], ["ge", "ゲ", 1], ["go", "ゴ", 1],
	["su", "ス", 1], ["se", "セ", 1], ["so", "ソ", 1],
	["za", "ザ", 1], ["zi", "ジ", 1], ["ji", "ジ", 1], ["zu", "ズ", 1],
	["ze", "ゼ", 1], ["zo", "ゾ", 1],
	["ja", "ジャ", 1], ["ju", "ジュ", 1], ["jo", "ジョ", 1],
	["ta", "タ", 1], ["ti", "チ", 1], ["tu", "ツ", 1], ["te", "テ", 1], ["to", "ト", 1],
	["da", "ダ", 1], ["di", "ヂ", 1], ["du", "ヅ", 1], ["de", "デ", 1], ["do", "ド", 1],
	["na", "ナ", 1], ["ni", "ニ", 1], ["nu", "ヌ", 1], ["ne", "ネ", 1], ["no", "ノ", 1],
	["nn", "ン", 1],
	["ha", "ハ", 1], ["hi", "ヒ", 1], ["hu", "フ", 1], ["he", "ヘ", 1], ["ho", "ホ", 1],
	["fa", "ファ", 1], ["fi", "フィ", 1], ["fu", "フ", 1], ["fe", "フェ", 1], ["fo", "フォ", 1],
	["ba", "バ", 1], ["bi", "ビ", 1], ["bu", "ブ", 1], ["be", "ベ", 1], ["bo", "ボ", 1],
	["pa", "パ", 1], ["pi", "ピ", 1], ["pu", "プ", 1], ["pe", "ペ", 1], ["po", "ポ", 1],
	["ma", "マ", 1], ["mi", "ミ", 1], ["mu", "ム", 1], ["me", "メ", 1], ["mo", "モ", 1],
	["ya", "ヤ", 1], ["yu", "ユ", 1], ["yo", "ヨ", 1],
	["ra", "ラ", 1], ["ri", "リ", 1], ["ru", "ル", 1], ["re", "レ", 1], ["ro", "ロ", 1],
	["wa", "ワ", 1], ["wi", "ウィ", 1], ["wo", "オ", 1],
	["a", "ア", 1], ["i", "イ", 1], ["u", "ウ", 1], ["e", "エ", 1], ["o", "オ", 1],
	["n", "ン", 1],
]


def getKanaFromRoma(roma: str) -> Optional[str]:
	kana = unicodedata.normalize("NFKC", roma)
	if kana in ("youtube",):
		return None
	for item in _romadic:
		kana = kana.replace(item[0], item[1])
	if all(re.search("[ァ-ヾ]", c) for c in kana):
		return kana
	return None


# spellchar table (from _nvdajp_spellchar.py, re-licensed BSD)
_spellchar_patterns: list[tuple[re.Pattern, str]] = []
for _p, _r in [
	("Ａ", "A"), ("Ｂ", "B"), ("Ｃ", "C"), ("Ｄ", "D"), ("Ｅ", "E"), ("Ｆ", "F"),
	("Ｇ", "G"), ("Ｈ", "H"), ("Ｉ", "I"), ("Ｊ", "J"), ("Ｋ", "K"), ("Ｌ", "L"),
	("Ｍ", "M"), ("Ｎ", "N"), ("Ｏ", "O"), ("Ｐ", "P"), ("Ｑ", "Q"), ("Ｒ", "R"),
	("Ｓ", "S"), ("Ｔ", "T"), ("Ｕ", "U"), ("Ｖ", "V"), ("Ｗ", "W"), ("Ｘ", "X"),
	("Ｙ", "Y"), ("Ｚ", "Z"),
	("ａ", "a"), ("ｂ", "b"), ("ｃ", "c"), ("ｄ", "d"), ("ｅ", "e"), ("ｆ", "f"),
	("ｇ", "g"), ("ｈ", "h"), ("ｉ", "i"), ("ｊ", "j"), ("ｋ", "k"), ("ｌ", "l"),
	("ｍ", "m"), ("ｎ", "n"), ("ｏ", "o"), ("ｐ", "p"), ("ｑ", "q"), ("ｒ", "r"),
	("ｓ", "s"), ("ｔ", "t"), ("ｕ", "u"), ("ｖ", "v"), ("ｗ", "w"), ("ｘ", "x"),
	("ｙ", "y"), ("ｚ", "z"),
	("０", "0"), ("１", "1"), ("２", "2"), ("３", "3"), ("４", "4"), ("５", "5"),
	("６", "6"), ("７", "7"), ("８", "8"), ("９", "9"),
	("0", "ゼロ "), ("1", "イチ "), ("2", "ニイ "), ("3", "サン "), ("4", "ヨン "),
	("5", "ゴオ "), ("6", "ロク "), ("7", "ナナ "), ("8", "ハチ "), ("9", "キュウ "),
	("(a|A)", "エイ "), ("(b|B)", "ビイー "), ("(c|C)", "シイ "), ("(d|D)", "ディイ "),
	("(e|E)", "イイー "), ("(f|F)", "エフ "), ("(g|G)", "ジイ "), ("(h|H)", "エイチ "),
	("(i|I)", "アイ "), ("(j|J)", "ジェイ "), ("(k|K)", "ケイ "), ("(l|L)", "エル "),
	("(m|M)", "エム "), ("(n|N)", "エヌ "), ("(o|O)", "オオ "), ("(p|P)", "ピイイ "),
	("(q|Q)", "キュウ "), ("(r|R)", "アール "), ("(s|S)", "エス "), ("(t|T)", "ティイ "),
	("(u|U)", "ユウ "), ("(v|V)", "ブイ "), ("(w|W)", "ダブリュウ "),
	("(x|X)", "エックス "), ("(y|Y)", "ワイ "), ("(z|Z)", "ゼッド "),
]:
	_spellchar_patterns.append((re.compile(_p), _r))


def convertSpellChar(msg: str) -> str:
	for p, r in _spellchar_patterns:
		try:
			msg = re.sub(p, r, msg)
		except Exception:
			pass
	return msg


RE_FULLSHAPE_ALPHA = re.compile("^[Ａ-Ｚａ-ｚ]+$")

# Single fullwidth characters that fugashi's libmecab emits as 名詞,サ変接続
# (unknown word) but the nvdajp MeCab fork emits as 記号,括弧閉 via unk.dic.
# Used by correct_features to restore the 記号 class for these characters.
_BRACKET_CLOSE_CHARS = frozenset("＂＇")

_FALLBACK_TABLE = {
	"＂": "”,記号,括弧閉,*,*,*,*,”,”,”,*/*,*",
	"＇": "’,記号,括弧閉,*,*,*,*,’,’,’,*/*,*",
	"｀": "‘,記号,括弧開,*,*,*,*,‘,‘,‘,*/*,*",
}


def _split_surface(surface: str) -> list[str]:
	chunks = []
	current_chunk = []
	for c in surface:
		if c.isalnum():
			current_chunk.append(c)
		else:
			if current_chunk:
				chunks.append("".join(current_chunk))
				current_chunk = []
			chunks.append(c)
	if current_chunk:
		chunks.append("".join(current_chunk))
	return chunks


def getMoraCount(s: str) -> int:
	m = s.split("/")
	if len(m) == 2:
		m2 = m[1]
		if m2 != "*":
			return int(m2)
	return 0


def _shouldWorkAroundLatinWordPostfix(ar3, ar2, ar) -> bool:
	return (
		(not (ar3 and ar3[0] == "\u3000" and ar2 and ar2[0] == "’"))
		and ar2
		and ar[0] in ("ｓ", "ｄ", "ｅｄ", "ｒ", "ｔｉｎｇ", "ｔ")
	)


def _makeFeatureFromLatinWordAndPostfix(org, ar, symbol=""):
	_hyoki = ar[0]
	_yomi = ar[8] if len(ar) > 8 else convertSpellChar(_hyoki).replace(" ", "")
	_pron = ar[9] if len(ar) > 9 else convertSpellChar(_hyoki).replace(" ", "")
	hin1 = ar[1]
	hin2 = ar[2]
	hin3 = ar[3]
	postfix = ""
	if org == "ｓ":
		postfix = "ズ"
		if _hyoki.endswith("ｐ") or _hyoki.endswith("ｋｅ") or _hyoki.endswith("ｒｋ"):
			postfix = "ス"
		elif _hyoki.endswith("ｔｈａｔ"):
			postfix = "ツ"
			_yomi = _yomi[:-2]
			_pron = _pron[:-2]
		elif _hyoki.endswith("ｗｏｒｄ"):
			postfix = "ズ"
			_yomi = _yomi[:-1]
			_pron = _pron[:-1]
	elif org == "ｔ":
		postfix = "ト"
	elif org in ("ｄ", "ｅｄ"):
		if _hyoki.endswith("ｔｅ") and _yomi.endswith("ト"):
			postfix = "ティド"
			_yomi = _yomi[:-1]
			_pron = _pron[:-1]
		else:
			postfix = "ド"
	elif org == "ｒ":
		postfix = "ア"
		if _hyoki.endswith("ｓｅ"):
			postfix = "ザー"
			_yomi = _yomi[:-1]
			_pron = _pron[:-1]
	elif _hyoki.endswith("ｔ") and _yomi.endswith("ト") and org == "ｔｉｎｇ":
		postfix = "ティング"
		_yomi = _yomi[:-1]
		_pron = _pron[:-1]
	hyoki = _hyoki + symbol + org
	yomi = _yomi + postfix
	pron = _pron + postfix
	mora = getMoraCount(ar[10]) + 1 if len(ar) > 10 else len(pron)
	feature = "{h},{h1},{h2},{h3},*,*,*,{h},{y},{p},0/{m},C0".format(
		h=hyoki, h1=hin1, h2=hin2, h3=hin3, y=yomi, p=pron, m=mora,
	)
	return feature


def _makeBraillePatternReading(s: str) -> str:
	n = ord(s) - 0x2800
	if n == 0:
		return "マスアケ"
	ar = []
	if n & 0x01:
		ar.append("イチ")
	if n & 0x02:
		ar.append("ニー")
	if n & 0x04:
		ar.append("サン")
	if n & 0x08:
		ar.append("ヨン")
	if n & 0x10:
		ar.append("ゴー")
	if n & 0x20:
		ar.append("ロク")
	if n & 0x40:
		ar.append("ナナ")
	if n & 0x80:
		ar.append("ハチ")
	return "".join(ar) + "ノテン"


def correct_features(
	lines: list[str],
	reparse: Optional[callable] = None,
) -> list[str]:
	"""Post-process MeCab feature lines (one CSV string per morpheme).

	``reparse`` is an optional callable ``reparse(text) -> list[str]`` used
	to re-analyze individual characters when filling in missing readings
	for unknown words (PATTERN 1/2). When None, those patterns are skipped.
	"""
	n = len(lines)
	# operate on a mutable copy of split fields
	parsed = [line.split(",") if line else [] for line in lines]

	new_parsed = []
	for pos in range(n):
		ar = parsed[pos]
		if not ar:
			continue
		if (
			len(ar) > 7
			and len(ar[0]) > 1
			and ar[1] == "名詞"
			and ar[2] == "サ変接続"
			and ar[7] == "*"
			and any(not c.isalnum() for c in ar[0])
			and len(set(ar[0])) > 1
		):
			for chunk in _split_surface(ar[0]):
				if len(chunk) == 1 and chunk in _FALLBACK_TABLE:
					new_parsed.append(_FALLBACK_TABLE[chunk].split(","))
				else:
					if reparse is not None:
						sub_lines = reparse(chunk)
						for sl in sub_lines:
							new_parsed.append(sl.split(","))
					else:
						new_parsed.append([chunk, "名詞", "サ変接続", "*", "*", "*", "*", "*"])
		else:
			new_parsed.append(ar)
	parsed = new_parsed
	n = len(parsed)

	for pos in range(n):
		ar = parsed[pos]
		if not ar:
			continue
		ar2 = parsed[pos - 1] if pos >= 1 and parsed[pos - 1] else None
		ar3 = parsed[pos - 2] if pos >= 2 and parsed[pos - 2] else None
		if (
			ar3 and ar2
			and RE_FULLSHAPE_ALPHA.match(ar3[0])
			and RE_FULLSHAPE_ALPHA.match(ar2[0])
			and RE_FULLSHAPE_ALPHA.match(ar[0])
		):
			hyoki = ar3[0] + ar2[0] + ar[0]
			hin1 = "名詞"
			hin2 = "固有名詞"
			yomi = getKanaFromRoma(hyoki)
			if yomi:
				pron = yomi
				mora = len(yomi)
				feature = "{h},{h1},{h2},*,*,*,*,{h},{y},{p},0/{m},C0".format(
					h=hyoki, h1=hin1, h2=hin2, y=yomi, p=pron, m=mora,
				)
				parsed[pos - 2] = feature.split(",")
				parsed[pos - 1] = ",,,*,*,*,*".split(",")
				parsed[pos] = feature.split(",")
		elif (
			len(ar) > 7
			and len(ar[0]) == 1
			and ar[1] == "名詞"
			and ar[2] == "サ変接続"
			and ar[7] == "*"
			and ar[0] in _FALLBACK_TABLE
		):
			parsed[pos] = _FALLBACK_TABLE[ar[0]].split(",")
		elif (len(ar) > 2 and ar[2] == "数" and len(ar) > 7 and ar[7] == "*") or (
			len(ar) > 2 and ar[1] == "名詞" and ar[2] == "サ変接続" and len(ar) > 7 and ar[7] == "*"
		):
			if reparse is not None:
				hyoki = ar[0]
				yomi = ""
				pron = ""
				mora = 0
				for c in hyoki:
					sub_lines = reparse(c)
					for sl in sub_lines:
						ar2 = sl.split(",")
						if len(ar2) > 7 and ar2[7] == "*" and c in _FALLBACK_TABLE:
							ar2 = _FALLBACK_TABLE[c].split(",")
						if len(ar2) > 10:
							yomi += ar2[8]
							pron += ar2[9]
							mora += getMoraCount(ar2[10])
				feature = "{h},名詞,普通名詞,*,*,*,*,{h},{y},{p},0/{m},C0".format(
					h=hyoki, y=yomi, p=pron, m=mora,
				)
				parsed[pos] = feature.split(",")
		elif (
			len(ar) > 7
			and len(ar[0]) == 1
			and ar[1] == "名詞"
			and ar[2] == "サ変接続"
			and ar[7] == "*"
		):
			# Single-character unknown words that should be 記号 (symbols).
			#
			# The fugashi-bundled libmecab emits some fullwidth punctuation
			# (notably ＂ U+FF02 and ＇ U+FF07) as 名詞,サ変接続 unknown words
			# instead of 記号, because its unk.dic lacks the mapping that the
			# nvdajp MeCab fork has. The fixture was recorded against the
			# nvdajp fork, which outputs these as 記号,括弧閉. Map them here
			# so the analysis matches.
			hyoki = ar[0]
			hin2 = "括弧閉" if hyoki in _BRACKET_CLOSE_CHARS else "一般"
			parsed[pos] = "{h},記号,{h2},*,*,*,*,{h},{h},{h},*/*,*".format(
				h=hyoki, h2=hin2,
			).split(",")
		elif ar2 and ar[0] == "ー" and len(ar) > 2 and ar[1] == "名詞" and ar[2] == "一般":
			if len(ar2) > 10:
				hyoki = ar2[0] + "ー"
				hin1 = ar2[1]
				hin2 = ar2[2]
				yomi = ar2[8] + "ー"
				pron = ar2[9] + "ー"
				mora = getMoraCount(ar2[10]) + 1
				feature = "{h},{h1},{h2},*,*,*,*,{h},{y},{p},0/{m},C0".format(
					h=hyoki, h1=hin1, h2=hin2, y=yomi, p=pron, m=mora,
				)
				parsed[pos - 1] = feature.split(",")
			elif ar3 and ar2 and len(ar3) > 10 and ar3[1] != "記号":
				hyoki = ar3[0] + ar2[0] + "ー"
				hin1 = ar3[1]
				hin2 = ar3[2]
				yomi = ar3[8] + ar2[0] + "ー"
				pron = ar3[9] + ar2[0] + "ー"
				mora = getMoraCount(ar3[10]) + len(ar2[0]) + 1
				feature = "{h},{h1},{h2},*,*,*,*,{h},{y},{p},0/{m},C0".format(
					h=hyoki, h1=hin1, h2=hin2, y=yomi, p=pron, m=mora,
				)
				parsed[pos - 2] = feature.split(",")
		elif _shouldWorkAroundLatinWordPostfix(ar3, ar2, ar):
			if ar3 and ar2 and ar2[0] in ("'", "’"):
				parsed[pos - 2] = ",,,*,*,*,*".split(",")
				parsed[pos - 1] = ",,,*,*,*,*".split(",")
				f = _makeFeatureFromLatinWordAndPostfix(ar[0], ar3, symbol="'")
				parsed[pos] = f.split(",")
			elif ar2 and len(ar2) > 10 and RE_FULLSHAPE_ALPHA.match(ar2[0]) and len(ar2[0]) > 1:
				parsed[pos - 1] = ",,,*,*,*,*".split(",")
				f = _makeFeatureFromLatinWordAndPostfix(ar[0], ar2)
				parsed[pos] = f.split(",")
		elif ar2 and RE_FULLSHAPE_ALPHA.match(ar[0]) and RE_FULLSHAPE_ALPHA.match(ar2[0]):
			hyoki = ar2[0] + ar[0]
			hin1 = "名詞"
			hin2 = "固有名詞"
			yomi = getKanaFromRoma(hyoki)
			if yomi:
				pron = yomi
				mora = len(yomi)
				feature = "{h},{h1},{h2},*,*,*,*,{h},{y},{p},0/{m},C0".format(
					h=hyoki, h1=hin1, h2=hin2, y=yomi, p=pron, m=mora,
				)
				parsed[pos - 1] = ",,,*,*,*,*".split(",")
				parsed[pos] = feature.split(",")
		elif RE_FULLSHAPE_ALPHA.match(ar[0]) and len(ar) > 7 and ar[7] == "*":
			roma = ar[0]
			kana = getKanaFromRoma(roma)
			if kana:
				c = len(kana)
				parsed[pos] = (
					"%s,名詞,固有名詞,*,*,*,*,%s,%s,%s,0/%d,C0" % (roma, roma, kana, kana, c)
				).split(",")
		elif len(ar[0]) == 1 and 0x2800 <= ord(ar[0]) <= 0x28FF:
			ar[8] = ar[9] = _makeBraillePatternReading(ar[0])
			parsed[pos] = ar
	# rejoin to CSV strings
	return [",".join(p) if p else "" for p in parsed]