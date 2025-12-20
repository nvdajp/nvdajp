# coding: UTF-8
# text2mecab.py for python-jtalk

import re
import unicodedata

CODE = "utf-8"

predic = None


def text2mecab_setup():
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
            [re.compile("\?"), "？"],
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


def text2mecab_convert(s):
    for p in predic:
        try:
            s = re.sub(p[0], p[1], s)
        except:
            pass
    return s


def text2mecab(txt, CODE_=CODE):
    text2mecab_setup()
    txt = unicodedata.normalize("NFKC", txt)
    txt = text2mecab_convert(txt)
    return txt.encode(CODE_, "ignore")
