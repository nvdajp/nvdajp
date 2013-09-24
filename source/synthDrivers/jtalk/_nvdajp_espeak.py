# _nvdajp_espeak.py 
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import translator2
from logHandler import log
import re
import copy
from _nvdajp_unicode import unicode_normalize

_logwrite = log.debug

def guessLang(msg):
	for i in xrange(len(msg)):
		c = ord(msg[i])
		if (0x3040 <= c <= 0x30ff) or (0x3100 <= c <= 0x9fff):
			return 'ja'
	return None

kanadic = None

def load_kanadic():
	return [
		[re.compile('ニュー'), 'nyuu'],
		[re.compile('キー'), 'kii'],

		[re.compile('カ'), 'ka'],
		[re.compile('キ'), 'ki'],
		[re.compile('ク'), 'ku'],
		[re.compile('ケ'), 'ke'],
		[re.compile('コ'), 'ko'],

		[re.compile('ガ'), 'ga'],
		[re.compile('ギ'), 'gi'],
		[re.compile('グ'), 'gu'],
		[re.compile('ゲ'), 'ge'],
		[re.compile('ゴ'), 'go'],

		[re.compile('サ'), 'sa'],
		[re.compile('シ'), 'shi'],
		[re.compile('ス'), 'su'],
		[re.compile('セ'), 'se'],
		[re.compile('ソ'), 'so'],

		[re.compile('ザ'), 'za'],
		[re.compile('ジ'), 'zi'],
		[re.compile('ズ'), 'zu'],
		[re.compile('ゼ'), 'ze'],
		[re.compile('ゾ'), 'zo'],

		[re.compile('タ'), 'ta'],
		[re.compile('チ'), 'chi'],
		[re.compile('ツ'), 'tsu'],
		[re.compile('テ'), 'te'],
		[re.compile('ト'), 'to'],

		[re.compile('ダ'), 'da'],
		[re.compile('ヂ'), 'di'],
		[re.compile('ヅ'), 'du'],
		[re.compile('デ'), 'de'],
		[re.compile('ド'), 'do'],

		[re.compile('ナ'), 'na'],
		[re.compile('ニ'), 'ni'],
		[re.compile('ヌ'), 'nu'],
		[re.compile('ネ'), 'ne'],
		[re.compile('ノ'), 'no'],

		[re.compile('ハ'), 'ha'],
		[re.compile('ヒ'), 'hi'],
		[re.compile('フ'), 'fu'],
		[re.compile('ヘ'), 'he'],
		[re.compile('ホ'), 'ho'],

		[re.compile('バ'), 'ba'],
		[re.compile('ビ'), 'bi'],
		[re.compile('ブ'), 'bu'],
		[re.compile('ベ'), 'be'],
		[re.compile('ボ'), 'bo'],

		[re.compile('パ'), 'pa'],
		[re.compile('ピ'), 'pi'],
		[re.compile('プ'), 'pu'],
		[re.compile('ペ'), 'pe'],
		[re.compile('ポ'), 'po'],

		[re.compile('マ'), 'ma'],
		[re.compile('ミ'), 'mi'],
		[re.compile('ム'), 'mu'],
		[re.compile('メ'), 'me'],
		[re.compile('モ'), 'mo'],

		[re.compile('ヤ'), 'ya'],
		[re.compile('ユ'), 'yu'],
		[re.compile('ヨ'), 'yo'],

		[re.compile('ラ'), 'ra'],
		[re.compile('リ'), 'ri'],
		[re.compile('ル'), 'ru'],
		[re.compile('レ'), 're'],
		[re.compile('ロ'), 'ro'],

		[re.compile('ワ'), 'wa'],
		[re.compile('ヲ'), 'wo'],

		[re.compile('ン'), 'n'],

		[re.compile('ア'), 'a'],
		[re.compile('イ'), 'i'],
		[re.compile('ウ'), 'u'],
		[re.compile('エ'), 'e'],
		[re.compile('オ'), 'o'],

		[re.compile('ー'), ' '],
		# Braille
		[re.compile('[\u2800-\u28ff]+'), ''],
		# Japanese & CJK
		[re.compile('[\u3040-\u9fff]+'), ''],
		]

def replaceJapanese(msg):
	if not translator2.mecab_initialized:
		translator2.initialize()
	msg = translator2.japanese_braille_separate(msg, _logwrite)[0]

	global kanadic
	if kanadic is None:
		kanadic = load_kanadic()
	for p in kanadic:
		try:
			msg = re.sub(p[0], p[1], msg)
		except:
			pass
	return msg

def replaceJapaneseFromSpeechSequence(speechSequence):
	a = []
	for item in speechSequence:
		item = copy.deepcopy(item)
		if isinstance(item,basestring):
			item = unicode_normalize(item)
			if guessLang(item):
				item = replaceJapanese(item)
		a.append(item)
	return a
