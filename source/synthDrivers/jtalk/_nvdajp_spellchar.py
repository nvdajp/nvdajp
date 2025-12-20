# _nvdajp_spellchar.py
# -*- coding: utf-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2010-2011 Takuya Nishimoto (nishimotz.com)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.

# workaround for msspeech Haruka with "Use spelling functionality"

import re

_dic = None


def init():
    global _dic
    if _dic:
        return
    _dic = [
        ### zenkaku alphabet convert
        [re.compile("Ａ"), "A"],
        [re.compile("Ｂ"), "B"],
        [re.compile("Ｃ"), "C"],
        [re.compile("Ｄ"), "D"],
        [re.compile("Ｅ"), "E"],
        [re.compile("Ｆ"), "F"],
        [re.compile("Ｇ"), "G"],
        [re.compile("Ｈ"), "H"],
        [re.compile("Ｉ"), "I"],
        [re.compile("Ｊ"), "J"],
        [re.compile("Ｋ"), "K"],
        [re.compile("Ｌ"), "L"],
        [re.compile("Ｍ"), "M"],
        [re.compile("Ｎ"), "N"],
        [re.compile("Ｏ"), "O"],
        [re.compile("Ｐ"), "P"],
        [re.compile("Ｑ"), "Q"],
        [re.compile("Ｒ"), "R"],
        [re.compile("Ｓ"), "S"],
        [re.compile("Ｔ"), "T"],
        [re.compile("Ｕ"), "U"],
        [re.compile("Ｖ"), "V"],
        [re.compile("Ｗ"), "W"],
        [re.compile("Ｘ"), "X"],
        [re.compile("Ｙ"), "Y"],
        [re.compile("Ｚ"), "Z"],
        [re.compile("ａ"), "a"],
        [re.compile("ｂ"), "b"],
        [re.compile("ｃ"), "c"],
        [re.compile("ｄ"), "d"],
        [re.compile("ｅ"), "e"],
        [re.compile("ｆ"), "f"],
        [re.compile("ｇ"), "g"],
        [re.compile("ｈ"), "h"],
        [re.compile("ｉ"), "i"],
        [re.compile("ｊ"), "j"],
        [re.compile("ｋ"), "k"],
        [re.compile("ｌ"), "l"],
        [re.compile("ｍ"), "m"],
        [re.compile("ｎ"), "n"],
        [re.compile("ｏ"), "o"],
        [re.compile("ｐ"), "p"],
        [re.compile("ｑ"), "q"],
        [re.compile("ｒ"), "r"],
        [re.compile("ｓ"), "s"],
        [re.compile("ｔ"), "t"],
        [re.compile("ｕ"), "u"],
        [re.compile("ｖ"), "v"],
        [re.compile("ｗ"), "w"],
        [re.compile("ｘ"), "x"],
        [re.compile("ｙ"), "y"],
        [re.compile("ｚ"), "z"],
        ### zenkaku numbers convert
        [re.compile("０"), "0"],
        [re.compile("１"), "1"],
        [re.compile("２"), "2"],
        [re.compile("３"), "3"],
        [re.compile("４"), "4"],
        [re.compile("５"), "5"],
        [re.compile("６"), "6"],
        [re.compile("７"), "7"],
        [re.compile("８"), "8"],
        [re.compile("９"), "9"],
        [re.compile("0"), "ゼロ "],
        [re.compile("1"), "イチ "],
        [re.compile("2"), "ニイ "],
        [re.compile("3"), "サン "],
        [re.compile("4"), "ヨン "],
        [re.compile("5"), "ゴオ "],
        [re.compile("6"), "ロク "],
        [re.compile("7"), "ナナ "],
        [re.compile("8"), "ハチ "],
        [re.compile("9"), "キュウ "],
        [re.compile("(a|A)"), "エイ "],
        [re.compile("(b|B)"), "ビイー "],
        [re.compile("(c|C)"), "シイ "],
        [re.compile("(d|D)"), "ディイ "],
        [re.compile("(e|E)"), "イイー "],
        [re.compile("(f|F)"), "エフ "],
        [re.compile("(g|G)"), "ジイ "],
        [re.compile("(h|H)"), "エイチ "],
        [re.compile("(i|I)"), "アイ "],
        [re.compile("(j|J)"), "ジェイ "],
        [re.compile("(k|K)"), "ケイ "],
        [re.compile("(l|L)"), "エル "],
        [re.compile("(m|M)"), "エム "],
        [re.compile("(n|N)"), "エヌ "],
        [re.compile("(o|O)"), "オオ "],
        [re.compile("(p|P)"), "ピイイ "],
        [re.compile("(q|Q)"), "キュウ "],
        [re.compile("(r|R)"), "アール "],
        [re.compile("(s|S)"), "エス "],
        [re.compile("(t|T)"), "ティイ "],
        [re.compile("(u|U)"), "ユウ "],
        [re.compile("(v|V)"), "ブイ "],
        [re.compile("(w|W)"), "ダブリュウ "],
        [re.compile("(x|X)"), "エックス "],
        [re.compile("(y|Y)"), "ワイ "],
        [re.compile("(z|Z)"), "ゼッド "],
    ]


def convert(msg):
    global _dic
    if _dic is None:
        init()
    for p in _dic:
        try:
            msg = re.sub(p[0], p[1], msg)
        except:
            pass
    return msg
