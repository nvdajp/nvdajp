# _nvdajp_predic.py 
# -*- coding: utf-8 -*-
# A part of speech engine nvdajp_jtalk
# Copyright (C) 2010-2011 Takuya Nishimoto (nishimotz.com)

import re

predic = None
camel_word_separator = re.compile(u'([a-z])([A-Z])')

def setup():
	global predic
	if predic is None:
		predic = load()

def convert(msg):
	for p in predic:
		try:
			msg = re.sub(p[0], p[1], msg)
		except:
			pass
	msg = re.sub(camel_word_separator, u'\\1 \\2', msg) # HelloWorld -> Hello World
	msg = msg.lower()
	return msg

def load():
	return [
		### Unicode REPLACEMENT CHARACTER
		[re.compile(u'\ufffd'), u' '],
		### zenkaku space normalize
		[re.compile(u'　'), u' '],
		
		## 人々 昔々 家々 山々 
 		[re.compile(u'(.)々'), u'\\1\\1'],
		## Welcome to NVDA
		[re.compile('Welcome to'), u'ウェルカムトゥー'],

		### 
		## nvdajp interfaces and documents
		[re.compile(u'上矢印'), u'ウエヤジルシ'],
		[re.compile(u'下矢印'), u'シタヤジルシ'],
		[re.compile(u'同梱'), u'ドーコン'],
		[re.compile(u'最上行'), u'サイジョーギョー'],
		[re.compile(u'単一文字'), u'タンイツモジ'],
		[re.compile(u'現在行'), u'ゲンザイギョー'],
		[re.compile(u'正しく'), u'ただしく'],
		[re.compile(u'初期値'), u'しょきち'],
		[re.compile(u'既定値'), u'きていち'],
		[re.compile(u'メモ帳'), u'めもちょー'],
		[re.compile(u'仮名文字'), u'かなもじ'],
		## 行をブックマーク 行を隠す
		[re.compile(u'行をブックマーク'), u'ギョーをブックマーク'],
		[re.compile(u'行を隠す'), u'ギョーを隠す'],
		## 被災された方へ 圏内の方へ 支援をお考えの方へ 少しでも
		[re.compile(u'された方'), u'されたかた'],
		[re.compile(u'圏内の方'), u'圏内のかた'],
		[re.compile(u'お考えの方'), u'お考えのかた'],
		[re.compile(u'少しでも'), u'すこしでも'],
		## 
		[re.compile(u'大見出し'), u'オーミダシ'],
		[re.compile(u'拡張子'), u'カクチョーシ'],
		[re.compile(u'前景色'), u'ゼンケーショク'],
		[re.compile(u'小文字'), u'コモジ'],
		[re.compile(u'親オブジェクト'), u'オヤオブジェクト'],
		[re.compile(u'表計算'), u'ヒョーケーサン'],
		[re.compile(u'八ッ場'), u'ヤンバ'],
		[re.compile(u'初音ミク'), u'ハツネミク'],
		[re.compile(u'金正日'), u'キムジョンイル'],
		[re.compile(u'正恩'), u'ジョンウン'],
		[re.compile(u'急きょ'), u'キューキョ'],
		
		### trim space
		[re.compile(u'マイ '), u'マイ'],
		[re.compile(u'コントロール パネル'), u'コントロールパネル'],
		[re.compile(u'タスク バー'), u'タスクバー'],
		[re.compile(u'の '), u'の'], # remove space "1の 7" -> "1の7"
		[re.compile(u' 側'), u' ガワ'],
		
		## isolated hiragana HA (mecab replaces to WA)
		## は 
		[re.compile(u'^は$'), u'ハ'],
		[re.compile(u'\\sは$'), u'ハ'],
		
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
		
		# Tween
		[re.compile(u'[Tt]ween'), u'トゥイーン'],
		# msspeech
		[re.compile(u'[Mm]sspeech'), u'エムエススピーチ'],
		#
		#[re.compile(u'[Yy]ou[Tt]ube'), u'ユーチューブ'],
		#[re.compile(u'[Mm]ixi'), u'ミクシー'],

		# ぼらんてぃあ
		[re.compile(u'ぼらんてぃあ'), u'ボランティア'],
		## 59 名
		[re.compile(u'(\\d) 名'), u'\\1名'],
		## 4行 ヨンコー -> ヨンギョー
		[re.compile(u'(\\d)行'), u'\\1ギョー'],
		## 1都5県
		[re.compile(u'1都(\\d)+県'), u'イット\\1ケン'],
		## 2 分前更新
		[re.compile(u'(\\d)+ 分前更新'), u'\\1分マエコーシン'],
		
		## 1MB 10MB 1.2MB 0.5MB 321.0MB 123.45MB 2.7GB
		[re.compile(u'(\\d+)MB'), u'\\1メガバイト'],
		[re.compile(u'(\\d+)GB'), u'\\1ギガバイト'],
		[re.compile(u'(\\d+)MHz'), u'\\1メガヘルツ'],
		[re.compile(u'(\\d+)GHz'), u'\\1ギガヘルツ'],

		### zenkaku symbols convert
		## ２０１１．０３．１１
		## １，２３４円
		[re.compile(u'．'), u'.'],
		[re.compile(u'，'), u','],

		## 1,234
		## 1,234,567
		## 1,234,567,890
		## 1,23 = ichi comma niju san
		## 1,0 = ichi comma zero
		[re.compile(u'(\\d)\\,(\\d{3})'), u'\\1\\2'],
		[re.compile(u'(\\d{2})\\,(\\d{3})'), u'\\1\\2'],
		[re.compile(u'(\\d{3})\\,(\\d{3})'), u'\\1\\2'],
		[re.compile(u'(\\d)\\,(\\d{1,2})'), u'\\1カンマ\\2'],

		[re.compile(u'\\b0(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)'), u'  ０0  ０\\1  ０\\2  ０\\3  ０\\4  ０\\5  ０\\6  ０\\7  ０\\8  ０\\9 '],
		[re.compile(u'\\b0(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)'), u'  ０0  ０\\1  ０\\2  ０\\3  ０\\4  ０\\5  ０\\6  ０\\7  ０\\8 '],
		[re.compile(u'\\b0(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)'), u'  ０0  ０\\1  ０\\2  ０\\3  ０\\4  ０\\5  ０\\6  ０\\7 '],
		[re.compile(u'\\b0(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)'), u'  ０0  ０\\1  ０\\2  ０\\3  ０\\4  ０\\5  ０\\6 '],
		[re.compile(u'\\b0(\\d)(\\d)(\\d)(\\d)(\\d)'), u'  ０0  ０\\1  ０\\2  ０\\3  ０\\4  ０\\5 '],
		[re.compile(u'\\b0(\\d)(\\d)(\\d)(\\d)'), u'  ０0  ０\\1  ０\\2  ０\\3  ０\\4 '],
		[re.compile(u'\\b0(\\d)(\\d)(\\d)'), u'  ０0  ０\\1  ０\\2  ０\\3 '],
		[re.compile(u'\\b0(\\d)(\\d)'), u'  ０0  ０\\1  ０\\2 '],
		[re.compile(u'\\b0(\\d)'), u'  ０0  ０\\1 '],

		[re.compile(u' ０0'), u'ゼロ'],
		[re.compile(u' ０1'), u'イチ'],
		[re.compile(u' ０2'), u'ニー'],
		[re.compile(u' ０3'), u'サン'],
		[re.compile(u' ０4'), u'ヨン'],
		[re.compile(u' ０5'), u'ゴー'],
		[re.compile(u' ０6'), u'ロク'],
		[re.compile(u' ０7'), u'ナナ'],
		[re.compile(u' ０8'), u'ハチ'],
		[re.compile(u' ０9'), u'キュー'],

		# TODO: 
		# MeCab dictionary is currently not UTF-8, so we add the characters here.
		# After the dictionary is migrated to UTF-8,
		# it should include the characters.
		[re.compile(u'鈹'), u'ヒ'],
		#
		[re.compile(u'噯'), u'アイ'],
		[re.compile(u'呃'), u'アク'],
		[re.compile(u'瘂'), u'ア'],
		[re.compile(u'蹻'), u'キョー'],
		[re.compile(u'脘'), u'カン'],
		[re.compile(u'譆'), u'キ'],
		[re.compile(u'蟜'), u'キョー'],
		[re.compile(u'郄'), u'ゲキ'],
		[re.compile(u'噦'), u'エツ'],
		[re.compile(u'瘀'), u'オ'],
		[re.compile(u'痹'), u'ヒ'],
		[re.compile(u'瘈'), u'ケイ'],
		[re.compile(u'髃'), u'グー'],
		[re.compile(u'焠'), u'サイ'],
		[re.compile(u'鑱'), u'ザン'],
		[re.compile(u'饞'), u'ザン'],
		[re.compile(u'瀆'), u'トク'],
		[re.compile(u'濼'), u'レキ'],
		[re.compile(u'濇'), u'ショク'],
		[re.compile(u'鞕'), u'コウ'],
		[re.compile(u'涿'), u'タク'],
		[re.compile(u'璇'), u'セン'],
		[re.compile(u'璣'), u'キ'],
		[re.compile(u'髎'), u'リョー'],
		[re.compile(u'囊'), u'ノー'],
		[re.compile(u'膻'), u'ダン'],
		[re.compile(u'鍉'), u'テイ'],
		[re.compile(u'癃'), u'リュー'],
	]

