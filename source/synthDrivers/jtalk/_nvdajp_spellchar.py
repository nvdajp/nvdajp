# _nvdajp_spellchar.py 
# -*- coding: utf-8 -*-
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2010-2011 Takuya Nishimoto (nishimotz.com)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

# workaround for msspeech Haruka with "Use spelling functionality"

import re
_dic = None

def init():
	global _dic
	if _dic : return
	_dic = [
		### zenkaku alphabet convert
		[re.compile(u'Ａ'), u'A'],
		[re.compile(u'Ｂ'), u'B'],
		[re.compile(u'Ｃ'), u'C'],
		[re.compile(u'Ｄ'), u'D'],
		[re.compile(u'Ｅ'), u'E'],
		[re.compile(u'Ｆ'), u'F'],
		[re.compile(u'Ｇ'), u'G'],
		[re.compile(u'Ｈ'), u'H'],
		[re.compile(u'Ｉ'), u'I'],
		[re.compile(u'Ｊ'), u'J'],
		[re.compile(u'Ｋ'), u'K'],
		[re.compile(u'Ｌ'), u'L'],
		[re.compile(u'Ｍ'), u'M'],
		[re.compile(u'Ｎ'), u'N'],
		[re.compile(u'Ｏ'), u'O'],
		[re.compile(u'Ｐ'), u'P'],
		[re.compile(u'Ｑ'), u'Q'],
		[re.compile(u'Ｒ'), u'R'],
		[re.compile(u'Ｓ'), u'S'],
		[re.compile(u'Ｔ'), u'T'],
		[re.compile(u'Ｕ'), u'U'],
		[re.compile(u'Ｖ'), u'V'],
		[re.compile(u'Ｗ'), u'W'],
		[re.compile(u'Ｘ'), u'X'],
		[re.compile(u'Ｙ'), u'Y'],
		[re.compile(u'Ｚ'), u'Z'],
		
		[re.compile(u'ａ'), u'a'],
		[re.compile(u'ｂ'), u'b'],
		[re.compile(u'ｃ'), u'c'],
		[re.compile(u'ｄ'), u'd'],
		[re.compile(u'ｅ'), u'e'],
		[re.compile(u'ｆ'), u'f'],
		[re.compile(u'ｇ'), u'g'],
		[re.compile(u'ｈ'), u'h'],
		[re.compile(u'ｉ'), u'i'],
		[re.compile(u'ｊ'), u'j'],
		[re.compile(u'ｋ'), u'k'],
		[re.compile(u'ｌ'), u'l'],
		[re.compile(u'ｍ'), u'm'],
		[re.compile(u'ｎ'), u'n'],
		[re.compile(u'ｏ'), u'o'],
		[re.compile(u'ｐ'), u'p'],
		[re.compile(u'ｑ'), u'q'],
		[re.compile(u'ｒ'), u'r'],
		[re.compile(u'ｓ'), u's'],
		[re.compile(u'ｔ'), u't'],
		[re.compile(u'ｕ'), u'u'],
		[re.compile(u'ｖ'), u'v'],
		[re.compile(u'ｗ'), u'w'],
		[re.compile(u'ｘ'), u'x'],
		[re.compile(u'ｙ'), u'y'],
		[re.compile(u'ｚ'), u'z'],
		
		### zenkaku numbers convert
		[re.compile(u'０'), u'0'],
		[re.compile(u'１'), u'1'],
		[re.compile(u'２'), u'2'],
		[re.compile(u'３'), u'3'],
		[re.compile(u'４'), u'4'],
		[re.compile(u'５'), u'5'],
		[re.compile(u'６'), u'6'],
		[re.compile(u'７'), u'7'],
		[re.compile(u'８'), u'8'],
		[re.compile(u'９'), u'9'],
		
		[re.compile(u'0'), u'ゼロ '],
		[re.compile(u'1'), u'イチ '],
		[re.compile(u'2'), u'ニイ '],
		[re.compile(u'3'), u'サン '],
		[re.compile(u'4'), u'ヨン '],
		[re.compile(u'5'), u'ゴオ '],
		[re.compile(u'6'), u'ロク '],
		[re.compile(u'7'), u'ナナ '],
		[re.compile(u'8'), u'ハチ '],
		[re.compile(u'9'), u'キュウ '],
		
		[re.compile(u'(a|A)'), u'エイ '],
		[re.compile(u'(b|B)'), u'ビイー '],
		[re.compile(u'(c|C)'), u'シイ '],
		[re.compile(u'(d|D)'), u'ディイ '],
		[re.compile(u'(e|E)'), u'イイー '],
		[re.compile(u'(f|F)'), u'エフ '],
		[re.compile(u'(g|G)'), u'ジイ '],
		[re.compile(u'(h|H)'), u'エイチ '],
		[re.compile(u'(i|I)'), u'アイ '],
		[re.compile(u'(j|J)'), u'ジェイ '],
		[re.compile(u'(k|K)'), u'ケイ '],
		[re.compile(u'(l|L)'), u'エル '],
		[re.compile(u'(m|M)'), u'エム '],
		[re.compile(u'(n|N)'), u'エヌ '],
		[re.compile(u'(o|O)'), u'オオ '],
		[re.compile(u'(p|P)'), u'ピイイ '],
		[re.compile(u'(q|Q)'), u'キュウ '],
		[re.compile(u'(r|R)'), u'アール '],
		[re.compile(u'(s|S)'), u'エス '],
		[re.compile(u'(t|T)'), u'ティイ '],
		[re.compile(u'(u|U)'), u'ユウ '],
		[re.compile(u'(v|V)'), u'ブイ '],
		[re.compile(u'(w|W)'), u'ダブリュウ '],
		[re.compile(u'(x|X)'), u'エックス '],
		[re.compile(u'(y|Y)'), u'ワイ '],
		[re.compile(u'(z|Z)'), u'ゼッド '],
	]

def convert(msg):
	global _dic
	if _dic is None: init()
	for p in _dic:
		try:
			msg = re.sub(p[0], p[1], msg)
		except:
			pass
	return msg
