# coding: UTF-8
#translator1.py (Japanese Braille translator Phase 1)
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2012 Masataka.Shinke, Takuya Nishimoto
#Copyright (C) 2013 Takuya Nishimoto (NVDA Japanese Team)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

from __future__ import unicode_literals
import unicodedata
import re

kana1_dic = {
	'ア':'⠁',
	'イ':'⠃',
	'ウ':'⠉',
	'エ':'⠋',
	'オ':'⠊',
	'カ':'⠡',
	'キ':'⠣',
	'ク':'⠩',
	'ケ':'⠫',
	'コ':'⠪',
	'サ':'⠱',
	'シ':'⠳',
	'ス':'⠹',
	'セ':'⠻',
	'ソ':'⠺',
	'タ':'⠕',
	'チ':'⠗',
	'ツ':'⠝',
	'テ':'⠟',
	'ト':'⠞',
	'ナ':'⠅',
	'ニ':'⠇',
	'ヌ':'⠍',
	'ネ':'⠏',
	'ノ':'⠎',
	'ハ':'⠥',
	'ヒ':'⠧',
	'フ':'⠭',
	'ヘ':'⠯',
	'ホ':'⠮',
	'マ':'⠵',
	'ミ':'⠷',
	'ム':'⠽',
	'メ':'⠿',
	'モ':'⠾',
	'ヤ':'⠌',
	'ユ':'⠬',
	'ヨ':'⠜',
	'ラ':'⠑',
	'リ':'⠓',
	'ル':'⠙',
	'レ':'⠛',
	'ロ':'⠚',
	'ワ':'⠄',
	'ヰ':'⠆',
	'ヱ':'⠖',
	'ヲ':'⠔',
	'ン':'⠴',
	'ッ':'⠂',
	'ヴ':'⠐⠉',
	'ガ':'⠐⠡',
	'ギ':'⠐⠣',
	'グ':'⠐⠩',
	'ゲ':'⠐⠫',
	'ゴ':'⠐⠪',
	'ザ':'⠐⠱',
	'ジ':'⠐⠳',
	'ズ':'⠐⠹',
	'ゼ':'⠐⠻',
	'ゾ':'⠐⠺',
	'ダ':'⠐⠕',
	'ヂ':'⠐⠗',
	'ヅ':'⠐⠝',
	'デ':'⠐⠟',
	'ド':'⠐⠞',
	'バ':'⠐⠥',
	'ビ':'⠐⠧',
	'ブ':'⠐⠭',
	'ベ':'⠐⠯',
	'ボ':'⠐⠮',
	'パ':'⠠⠥',
	'ピ':'⠠⠧',
	'プ':'⠠⠭',
	'ペ':'⠠⠯',
	'ポ':'⠠⠮',
	}
kana2_dic = {
	'イェ':'⠈⠋',
	'キャ':'⠈⠡',
	'キュ':'⠈⠩',
	'キェ':'⠈⠫',
	'キョ':'⠈⠪',
	'シャ':'⠈⠱',
	'スィ':'⠈⠳',
	'シュ':'⠈⠹',
	'シェ':'⠈⠻',
	'ショ':'⠈⠺',
	'チャ':'⠈⠕',
	'ティ':'⠈⠗',
	'チュ':'⠈⠝',
	'チェ':'⠈⠟',
	'チョ':'⠈⠞',
	'ニャ':'⠈⠅',
	'ニュ':'⠈⠍',
	'ニェ':'⠈⠏',
	'ニョ':'⠈⠎',
	'ヒャ':'⠈⠥',
	'ヒュ':'⠈⠭',
	'ヒェ':'⠈⠯',
	'ヒョ':'⠈⠮',
	'ミャ':'⠈⠵',
	'ミュ':'⠈⠽',
	'ミェ':'⠈⠿',
	'ミョ':'⠈⠾',
	'リャ':'⠈⠑',
	'リュ':'⠈⠙',
	'リェ':'⠈⠛',
	'リョ':'⠈⠚',
	'ギャ':'⠘⠡',
	'ギュ':'⠘⠩',
	'ギェ':'⠘⠫',
	'ギョ':'⠘⠪',
	'ジャ':'⠘⠱',
	'ズィ':'⠘⠳',
	'ジュ':'⠘⠹',
	'ジェ':'⠘⠻',
	'ジョ':'⠘⠺',
	'ヂャ':'⠘⠕',
	'ディ':'⠘⠗',
	'ヂュ':'⠘⠝',
	'ヂェ':'⠘⠟',
	'ヂョ':'⠘⠞',
	'ビャ':'⠘⠥',
	'ビュ':'⠘⠭',
	'ビェ':'⠘⠯',
	'ビョ':'⠘⠮',
	'テュ':'⠨⠝',
	'ピャ':'⠨⠥',
	'ピュ':'⠨⠭',
	'ピョ':'⠨⠮',
	'フュ':'⠨⠬',
	'フョ':'⠨⠜',
	'デュ':'⠸⠝',
	'ヴュ':'⠸⠬',
	'ヴョ':'⠸⠜',
	'ウァ':'⠢⠁',
	'ウィ':'⠢⠃',
	'ウェ':'⠢⠋',
	'ウォ':'⠢⠊',
	'クァ':'⠢⠡',
	'クィ':'⠢⠣',
	'クェ':'⠢⠫',
	'クォ':'⠢⠪',
	'ツァ':'⠢⠕',
	'ツィ':'⠢⠗',
	'トゥ':'⠢⠝',
	'ツェ':'⠢⠟',
	'ツォ':'⠢⠞',
	'ファ':'⠢⠥',
	'フィ':'⠢⠧',
	'フェ':'⠢⠯',
	'フォ':'⠢⠮',
	'グァ':'⠲⠡',
	'グィ':'⠲⠣',
	'グェ':'⠲⠫',
	'グォ':'⠲⠪',
	'ヅァ':'⠲⠕',
	'ヅィ':'⠲⠗',
	'ドゥ':'⠲⠝',
	'ヅェ':'⠲⠟',
	'ヅォ':'⠲⠞',
	'ヴァ':'⠲⠥',
	'ヴィ':'⠲⠧',
	'ヴェ':'⠲⠯',
	'ヴォ':'⠲⠮',
	}
jp_symbol_dic = {
	'+':'⠢',
	'-':'⠤',
	':':'⠐⠂',
	'\\':'⠫', # yen mark
	'?':'⠢ ', # one space
	'@':'⠪',
	'<':'⠔⠔',
	'>':'⠢⠢',
	'=':'⠒⠒',
	'#':'⠰⠩',
	'$':'⠹',
	'%':'⠰⠏',
	'&':'⠰⠯',
	'*':'⠰⠡',
	';':'⠆',
	'|':'⠳',
	'"':'⠶',
	# "'":'⠄',
	#'/':'⠌',
	'.':'⠲',
	'!':'⠖ ', # one space
	'^':'⠘',
	'`':'⠐⠑',
	'_':'⠐⠤',
	'~':'⠐⠉',
	'ー':'⠒',
	'、':'⠰ ', # one space
	'。':'⠲  ', # two spaces
	'・':'⠐ ', # one space
	'｜':'⠶',
	'＿':'⠤',
	'「':'⠤',
	'」':'⠤',
	'『':'⠰⠤',
	'』':'⠤⠆',
	'｢':'⠤',
	'｣':'⠤',
	'(':'⠶',
	')':'⠶',
	'（':'⠶',
	'）':'⠶',
	'[':'⠐⠶',
	']':'⠶⠂',
	'“':'⠐⠶',
	'”':'⠶⠂',
	'{':'⠐⠶',
	'}':'⠶⠂',
	'‘':'⠐⠶',
	'’':'⠶⠂',
	'〔':'⠐⠶',
	'〕':'⠶⠂',
	'〈':'⠐⠶',
	'〉':'⠶⠂',
	'《':'⠐⠶',
	'》':'⠶⠂',
	'【':'⠐⠶',
	'】':'⠶⠂',
	'〝':'⠐⠶',
	'〟':'⠶⠂',
	'☆':'⠰⠮⠂',
	'★':'⠰⠮⠆',
	'○':'⠠⠵⠂',
	'●':'⠠⠵⠆',
	'◎':'⠠⠵⠲',
	'□':'⠠⠳⠂',
	'■':'⠠⠳⠆',
	'△':'⠠⠱⠂',
	'▲':'⠠⠱⠆',
	'▽':'⠰⠱⠂',
	'×':'⠰⠡⠂',
	'▼':'⠰⠱⠆',
	'◇':'⠨⠧⠂',
	'◆':'⠨⠧⠆',
	'※':'⠔⠔ ', # 第1星印 35-35 (後ろを1マスあける)
	'→':' ⠒⠒⠕ ', # 矢印 前後に1マスあける
	'←':' ⠪⠒⠒ ', # 矢印 前後に1マスあける
	}
info_symbol_dic = {
	',':'⠂',
	'?':'⠐⠦',
	'+':'⠬',
	"'":'⠄',
	'.':'⠲',
	'!':'⠖',
	'(':'⠦',
	')':'⠴',
	'{':'⠣',
	'}':'⠜',
	'[':'⠷',
	']':'⠾',
	'%': '⠻',
	'&':'⠯',
	'#':'⠩',
	'*':'⠡',
	}
num_dic = {
	'0':'⠚',
	'1':'⠁',
	'2':'⠃',
	'3':'⠉',
	'4':'⠙',
	'5':'⠑',
	'6':'⠋',
	'7':'⠛',
	'8':'⠓',
	'9':'⠊',
	}
num_symbol_dic = {
	'.':'⠂',
	',':'⠄',
	}
alpha_dic = {
	'a':'⠁',
	'b':'⠃',
	'c':'⠉',
	'd':'⠙',
	'e':'⠑',
	'f':'⠋',
	'g':'⠛',
	'h':'⠓',
	'i':'⠊',
	'j':'⠚',
	'k':'⠅',
	'l':'⠇',
	'm':'⠍',
	'n':'⠝',
	'o':'⠕',
	'p':'⠏',
	'q':'⠟',
	'r':'⠗',
	's':'⠎',
	't':'⠞',
	'u':'⠥',
	'v':'⠧',
	'w':'⠺',
	'x':'⠭',
	'y':'⠽',
	'z':'⠵',
	}
alpha_cap_dic = {
	'A':'⠁',
	'B':'⠃',
	'C':'⠉',
	'D':'⠙',
	'E':'⠑',
	'F':'⠋',
	'G':'⠛',
	'H':'⠓',
	'I':'⠊',
	'J':'⠚',
	'K':'⠅',
	'L':'⠇',
	'M':'⠍',
	'N':'⠝',
	'O':'⠕',
	'P':'⠏',
	'Q':'⠟',
	'R':'⠗',
	'S':'⠎',
	'T':'⠞',
	'U':'⠥',
	'V':'⠧',
	'W':'⠺',
	'X':'⠭',
	'Y':'⠽',
	'Z':'⠵',
	}

def is_ara(c):
	# 数字の後につなぎ符が必要
	return c in 'アイウエオラリルレロ'

def translateWithInPos(text):
	retval = ''
	pos = 0
	latin = False # 外字符モード
	num = False # 数符モード
	capital = False # 二重大文字符モード
	quote_mode = False # 外国語引用符モード
	info_mode = False # 情報処理点字モード
	text = unicodedata.normalize('NFKC', text)
	inPos = []

	while pos < len(text):
		#space
		if text[pos] == ' ':
			retval += ' '
			inPos.append(pos)
			capital = latin = num = False
			pos += 1
		#Numeric
		elif text[pos] in num_dic:
			latin = False
			if not num:
				retval += '⠼'
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
			num = capital = False
			pos += 1
		#Numeric symbols
		elif num and text[pos] in num_symbol_dic and \
				pos+1 < len(text) and text[pos+1].isdigit():
			retval += num_symbol_dic[text[pos]]
			inPos.extend([pos] * len(num_symbol_dic[text[pos]]))
			pos += 1
		# halfshape apostrophe symbol
		elif text[pos] == "'":
			if pos+1 < len(text) and text[pos+1].isdigit():
				retval += '⠼⠄'
				inPos.extend([pos, pos])
				num = True
			pos += 1
		# slash symbol
		elif text[pos] == '/':
			retval += '⠌'
			inPos.append(pos)
			num = capital = False
			pos += 1
		#Japanese symbols
		elif text[pos] in jp_symbol_dic:
			retval += jp_symbol_dic[text[pos]]
			inPos.extend([pos] * len(jp_symbol_dic[text[pos]]))
			latin = num = False
			pos += 1
		# lower/upper case alphabet
		elif text[pos] in alpha_dic or text[pos] in alpha_cap_dic:
			if not latin and not quote_mode:
				retval += '⠰'
				inPos.append(pos)
			elif info_mode and pos >= 2 and \
					text[pos-2].isdigit() and \
					text[pos-1] == '.' and \
					text[pos] in 'abcdefghij':
				# 情報処理で数字、ピリオドのあとにａ～ｊが続くときは小文字フラグ
				retval += '⠰'
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
				retval += '⠠⠠'
				inPos.extend([pos, pos])
				capital = True
			else:
				capital = False
			# アルファベットの続く部分を変換
			while pos < tpos:
				if not capital and text[pos] in alpha_cap_dic:
					retval += '⠠'
					inPos.append(pos)
				retval += alpha_dic[text[pos].lower()]
				inPos.append(pos)
				pos += 1
		#Two kana characters
		elif pos+1 < len(text) and text[pos:pos+2] in kana2_dic:
			if latin:
				retval += '⠤'
				inPos.append(pos - 1) # つなぎ符は直前の文字に対応
			elif num and is_ara(text[pos:pos+1]):
				retval += '⠤'
				inPos.append(pos - 1) # つなぎ符は直前の文字に対応
			retval += kana2_dic[text[pos:pos+2]]
			inPos.extend([pos] * len(kana2_dic[text[pos:pos+2]]))
			latin = num = False
			pos += 2
		#One kana character
		elif text[pos] in kana1_dic:
			if latin:
				retval += '⠤'
				inPos.append(pos - 1) # つなぎ符は直前の文字に対応
			elif num:
				if is_ara(text[pos]):
					retval += '⠤'
					inPos.append(pos - 1) # つなぎ符は直前の文字に対応
				elif text[pos] == 'ワ' and pos+3 < len(text) and \
						is_ara(text[pos+1]) and is_ara(text[pos+2]) and is_ara(text[pos+3]):
					retval += '⠤'
					inPos.append(pos - 1) # つなぎ符は直前の文字に対応
			retval += kana1_dic[text[pos]]
			inPos.extend([pos] * len(kana1_dic[text[pos]]))
			latin = num = False
			pos += 1
		#Braille should not be changed
		elif 0x2800 <= ord(text[pos]) and ord(text[pos]) <= 0x28ff:
			latin = False
			#数字モード
			if text[pos] == '⠼':
				num = True
			else:
				num = False
			#外国語引用符モード切替
			if not quote_mode and text[pos] == '⠦':
				quote_mode = True
			if quote_mode and text[pos] == '⠴':
				quote_mode = False
			#情報処理モード切替
			if text[pos] == '⠠' and pos+1 < len(text):
				if text[pos+1] == '⠦':
					info_mode = True
				elif text[pos+1] == '⠴':
					info_mode = False

			if ord(text[pos]) == 0x2800:
				retval += ' ' # use 0x20
				inPos.append(pos)
			else:
				retval += text[pos]
				inPos.append(pos)
			pos += 1
		#Exception
		else:
			latin = num = False
			retval += '□'
			inPos.append(pos)
			pos += 1
	# rstrip with inPos
	outbuf = retval
	if text[-1] != ' ':
		while outbuf[-1:] == ' ':
			outbuf = outbuf[:-1]
			inPos.pop()
	return (outbuf, inPos)
