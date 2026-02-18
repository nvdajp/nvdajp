# coding: UTF-8
# text2mecab.py for python-jtalk

from typing import Any
import re
import unicodedata

CODE = "utf-8"

predic: list[list[Any]] | None = None


def text2mecab_setup() -> None:
	global predic
	if predic is None:
		predic = [
			[re.compile("\r"), ""],
			[re.compile("\n"), ""],
			[re.compile(" "), "　"],
			[re.compile("!"), "！"],
			[re.compile('"'), "”"],
			[re.compile("#"), "＃"],
			[re.compile("\\$"), "＄"],
			[re.compile("%"), "％"],
			[re.compile("&"), "＆"],
			[re.compile("'"), "’"],
			[re.compile("\\("), "（"],
			[re.compile("\\)"), "）"],
			[re.compile("\\*"), "＊"],
			[re.compile("\\+"), "＋"],
			[re.compile(","), "，"],
			[re.compile("\\-"), "−"],
			[re.compile("\\."), "．"],
			[re.compile("\\/"), "／"],
			[re.compile("0"), "０"],
			[re.compile("1"), "１"],
			[re.compile("2"), "２"],
			[re.compile("3"), "３"],
			[re.compile("4"), "４"],
			[re.compile("5"), "５"],
			[re.compile("6"), "６"],
			[re.compile("7"), "７"],
			[re.compile("8"), "８"],
			[re.compile("9"), "９"],
			[re.compile(":"), "："],
			[re.compile(";"), "；"],
			[re.compile("<"), "＜"],
			[re.compile("="), "＝"],
			[re.compile(">"), "＞"],
			[re.compile("\\?"), "？"],
			[re.compile("@"), "＠"],
			[re.compile("A"), "Ａ"],
			[re.compile("B"), "Ｂ"],
			[re.compile("C"), "Ｃ"],
			[re.compile("D"), "Ｄ"],
			[re.compile("E"), "Ｅ"],
			[re.compile("F"), "Ｆ"],
			[re.compile("G"), "Ｇ"],
			[re.compile("H"), "Ｈ"],
			[re.compile("I"), "Ｉ"],
			[re.compile("J"), "Ｊ"],
			[re.compile("K"), "Ｋ"],
			[re.compile("L"), "Ｌ"],
			[re.compile("M"), "Ｍ"],
			[re.compile("N"), "Ｎ"],
			[re.compile("O"), "Ｏ"],
			[re.compile("P"), "Ｐ"],
			[re.compile("Q"), "Ｑ"],
			[re.compile("R"), "Ｒ"],
			[re.compile("S"), "Ｓ"],
			[re.compile("T"), "Ｔ"],
			[re.compile("U"), "Ｕ"],
			[re.compile("V"), "Ｖ"],
			[re.compile("W"), "Ｗ"],
			[re.compile("X"), "Ｘ"],
			[re.compile("Y"), "Ｙ"],
			[re.compile("Z"), "Ｚ"],
			[re.compile("\\["), "［"],
			[re.compile("\\\\"), "￥"],
			[re.compile("\\]"), "］"],
			[re.compile("\\^"), "＾"],
			[re.compile("_"), "＿"],
			[re.compile("`"), "‘"],
			[re.compile("a"), "ａ"],
			[re.compile("b"), "ｂ"],
			[re.compile("c"), "ｃ"],
			[re.compile("d"), "ｄ"],
			[re.compile("e"), "ｅ"],
			[re.compile("f"), "ｆ"],
			[re.compile("g"), "ｇ"],
			[re.compile("h"), "ｈ"],
			[re.compile("i"), "ｉ"],
			[re.compile("j"), "ｊ"],
			[re.compile("k"), "ｋ"],
			[re.compile("l"), "ｌ"],
			[re.compile("m"), "ｍ"],
			[re.compile("n"), "ｎ"],
			[re.compile("o"), "ｏ"],
			[re.compile("p"), "ｐ"],
			[re.compile("q"), "ｑ"],
			[re.compile("r"), "ｒ"],
			[re.compile("s"), "ｓ"],
			[re.compile("t"), "ｔ"],
			[re.compile("u"), "ｕ"],
			[re.compile("v"), "ｖ"],
			[re.compile("w"), "ｗ"],
			[re.compile("x"), "ｘ"],
			[re.compile("y"), "ｙ"],
			[re.compile("z"), "ｚ"],
			[re.compile("{"), "｛"],
			[re.compile("\\|"), "｜"],
			[re.compile("}"), "｝"],
			[re.compile("~"), "〜"],
			[re.compile("�"), "？"],  # u+fffd
		]


def text2mecab_convert(s: str) -> str:
	if predic is None:
		text2mecab_setup()
	assert predic is not None  # type: ignore[unreachable]
	for p in predic:
		try:
			s = re.sub(p[0], p[1], s)
		except Exception:
			pass
	return s


def text2mecab(txt: str, CODE_: str = CODE) -> bytes:
	text2mecab_setup()
	txt = unicodedata.normalize("NFKC", txt)
	txt = text2mecab_convert(txt)
	# Detect mixed ASCII/non-ASCII or unusual whitespace patterns that may trigger crashes.
	assert "\t" not in txt, "text2mecab: unexpected tab after conversion"
	assert "\r" not in txt and "\n" not in txt, "text2mecab: unexpected newline after conversion"
	ascii_count = sum(1 for c in txt if ord(c) < 0x80)
	non_ascii_count = len(txt) - ascii_count
	if ascii_count and non_ascii_count:
		# Allow common punctuation but flag mixed alnum + non-ASCII as suspicious.
		mixed_alnum = any(c.isalnum() and ord(c) < 0x80 for c in txt)
		assert not mixed_alnum, "text2mecab: mixed ASCII alnum and non-ASCII"
	# Detect repeated ASCII spaces (double-space) which showed crashes in x64.
	assert "  " not in txt, "text2mecab: consecutive ASCII spaces detected"
	# Detect ASCII control characters (excluding space) after conversion.
	ctrl_chars = [c for c in txt if ord(c) < 0x20 and c != " "]
	assert not ctrl_chars, f"text2mecab: ASCII control chars detected: {ctrl_chars!r}"
	return txt.encode(CODE_, "ignore")
