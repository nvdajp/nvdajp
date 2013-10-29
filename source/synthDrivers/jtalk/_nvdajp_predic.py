# _nvdajp_predic.py 
# -*- coding: utf-8 -*-
# A part of speech engine nvdajp_jtalk
# Copyright (C) 2010-2011 Takuya Nishimoto (nishimotz.com)

import re

predic = None

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
	msg = msg.lower()
	return msg

def load():
	return [
		[re.compile(u'^ー$'), u'チョーオン'],
		[re.compile(u'^ン$'), u'ウン'],
		[re.compile(u'\\sー$'), u' チョーオン'],
		[re.compile(u'\\sン$'), u' ウン'],

		## 人々 昔々 家々 山々 
 		[re.compile(u'(.)々'), u'\\1\\1'],

		## isolated hiragana HA (mecab replaces to WA)
		## は 
		[re.compile(u'^は$'), u'ハ'],
		[re.compile(u'\\sは$'), u' ハ'],
		
		## 59 名
		[re.compile(u'(\\d) 名'), u'\\1名'],
		## 4行 ヨンコー -> ヨンギョー
		[re.compile(u'(\\d)行'), u'\\1ギョー'],
		## 2 分前更新
		[re.compile(u'(\\d)+ 分前更新'), u'\\1分マエコーシン'],
		
		## 1MB 10MB 1.2MB 0.5MB 321.0MB 123.45MB 2.7GB
		## 1 MB 10 MB 1.2 MB 0.5 MB 321.0 MB 123.45 MB 2.7 GB
		[re.compile(u'(\\d+)\\s*KB'), u'\\1キロバイト'],
		[re.compile(u'(\\d+)\\s*MB'), u'\\1メガバイト'],
		[re.compile(u'(\\d+)\\s*GB'), u'\\1ギガバイト'],
		[re.compile(u'(\\d+)\\s*MHz'), u'\\1メガヘルツ'],
		[re.compile(u'(\\d+)\\s*GHz'), u'\\1ギガヘルツ'],

		## 2013 年 1 月 2 日
		[re.compile(u'(\\d+)\\s+年\\s+(\\d+)\\s+月\\s+(\\d+)\\s+日'), u'\\1年\\2月\\3日'],

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

		[re.compile(u'(\\d{1,4})\\.(\\d{1,4})\\.(\\d{1,4})\\.(\\d{1,4})'), u'\\1テン\\2テン\\3テン\\4'],
		[re.compile(u'(\\d{1,4})\\.(\\d{1,4})\\.(\\d{1,4})'), u'\\1テン\\2テン\\3'],

		# do not replace '0' after '.' to phonetic symbols (prepare)
		[re.compile(u'\\.0'), u'.0０'],

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

		# do not replace '0' after '.' to phonetic symbols (finalize)
		[re.compile(u'\\.0０'), u'.0'],
	]

