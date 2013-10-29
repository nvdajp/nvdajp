# _nvdajp_espeak.py 
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import translator2
from logHandler import log
import re
import copy
from _nvdajp_unicode import unicode_normalize
from speech import CharacterModeCommand

_logwrite = log.debug

def isJapaneseLang(msg):
	for i in msg:
		c = ord(i)
		if (0x3040 <= c <= 0x30ff) or (0x3100 <= c <= 0x9fff):
			return True
	return False

kanadic = None

def load_kanadic():
	return [
		[re.compile('キュ'), 'cu'],
		[re.compile('キョ'), 'co'],
		[re.compile('ギャ'), 'ga'],
		[re.compile('ギュ'), 'gu'],
		[re.compile('ギョ'), 'go'],

		[re.compile('シャ'), 'sha'],
		[re.compile('シュ'), 'shu'],
		[re.compile('ショ'), 'sho'],

		[re.compile('ジャ'), 'jar'],
		[re.compile('ジュ'), 'ju'],
		[re.compile('ジョ'), 'jo'],
		[re.compile('ヂャ'), 'jar'],
		[re.compile('ヂュ'), 'ju'],
		[re.compile('ヂョ'), 'jo'],
		[re.compile('ニャ'), 'nyar'],
		[re.compile('ニュ'), 'new'],
		[re.compile('ニョ'), 'no'],

		[re.compile('ヒャ'), 'hyar'],
		[re.compile('ヒュ'), 'hu'],
		[re.compile('ヒョ'), 'ho'],
		[re.compile('ビャ'), 'bar'],
		[re.compile('ビュ'), 'bu'],
		[re.compile('ビョ'), 'bo'],
		[re.compile('ピャ'), 'pyar'],
		[re.compile('ピュ'), 'pew'],
		[re.compile('ピョ'), 'po'],

		[re.compile('ミャ'), 'ma'],
		[re.compile('ミュ'), 'mu'],
		[re.compile('ミョ'), 'mo'],
		[re.compile('リャ'), 'ra'],
		[re.compile('リュ'), 'ru'],
		[re.compile('リョ'), 'ro'],

		[re.compile('イェ'), 'yiay'],
		[re.compile('キェ'), 'kyay'],
		[re.compile('シェ'), 'shay'],
		[re.compile('チェ'), 'chay'],
		[re.compile('ニェ'), 'nyay'],
		[re.compile('ヒェ'), 'hyay'],
		[re.compile('スィ'), 'si'],
		[re.compile('ティ'), 'tee'],
		[re.compile('ジェ'), 'jay'],
		[re.compile('ズィ'), 'zee'],
		[re.compile('ディ'), 'di'],
		[re.compile('ウィ'), 'we'],
		[re.compile('ウェ'), 'way'],
		[re.compile('ウォ'), 'wo'],
		[re.compile('トゥ'), 'tu'],
		[re.compile('クァ'), 'kwa'],
		[re.compile('クィ'), 'kwee'],
		[re.compile('クェ'), 'kway'],
		[re.compile('クォ'), 'kwo'],
		[re.compile('ドゥ'), 'du'],
		[re.compile('グァ'), 'gwa'],
		[re.compile('グィ'), 'gwee'],
		[re.compile('グェ'), 'gway'],
		[re.compile('グォ'), 'gwo'],
		[re.compile('テュ'), 'tu'],
		[re.compile('フュ'), 'fu'],
		[re.compile('フョ'), 'fo'],
		[re.compile('ツァ'), 'tsar'],
		[re.compile('ツィ'), 'tsee'],
		[re.compile('ツェ'), 'tsay'],
		[re.compile('ツォ'), 'tso'],
		[re.compile('デュ'), 'du'],
		[re.compile('ヴュ'), 'vu'],
		[re.compile('ヴョ'), 'vo'],
		[re.compile('ファ'), 'far'],
		[re.compile('フィ'), 'fi'],
		[re.compile('フェ'), 'fe'],
		[re.compile('フォ'), 'fo'],
		[re.compile('ヴァ'), 'var'],
		[re.compile('ヴィ'), 'vee'],
		[re.compile('ヴェ'), 'vay'],
		[re.compile('ヴォ'), 'vo'],
		[re.compile('ヴ'), 'vu'],

		[re.compile('カ'), 'ca'],
		[re.compile('キ'), 'kee'],
		[re.compile('ク'), 'cu'],
		[re.compile('ケ'), 'kay'],
		[re.compile('コ'), 'co'],

		[re.compile('ガ'), 'ga'],
		[re.compile('ギ'), 'gi'],
		[re.compile('グ'), 'gu'],
		[re.compile('ゲ'), 'gay'],
		[re.compile('ゴ'), 'go'],

		[re.compile('サ'), 'sa'],
		[re.compile('シ'), 'shi'],
		[re.compile('ス'), 'su'],
		[re.compile('セ'), 'say'],
		[re.compile('ソ'), 'so'],

		[re.compile('ザ'), 'za'],
		[re.compile('ジ'), 'zee'],
		[re.compile('ズ'), 'zu'],
		[re.compile('ゼ'), 'zay'],
		[re.compile('ゾ'), 'zo'],

		[re.compile('タ'), 'ta'],
		[re.compile('チ'), 'chee'],
		[re.compile('ツ'), 'tsu'],
		[re.compile('テ'), 'tay'],
		[re.compile('ト'), 'tau'],

		[re.compile('ダ'), 'da'],
		[re.compile('ヂ'), 'gee'],
		[re.compile('ヅ'), 'zu'],
		[re.compile('デ'), 'day'],
		[re.compile('ド'), 'dau'],

		[re.compile('ナ'), 'na'],
		[re.compile('ニ'), 'nee'],
		[re.compile('ヌ'), 'nu'],
		[re.compile('ネ'), 'nay'],
		[re.compile('ノ'), 'no'],

		[re.compile('ハ'), 'ha'],
		[re.compile('ヒ'), 'hee'],
		[re.compile('フ'), 'fu'],
		[re.compile('ヘ'), 'hay'],
		[re.compile('ホ'), 'ho'],

		[re.compile('バ'), 'ba'],
		[re.compile('ビ'), 'bee'],
		[re.compile('ブ'), 'boo'],
		[re.compile('ベ'), 'bay'],
		[re.compile('ボ'), 'bo'],

		[re.compile('パ'), 'pa'],
		[re.compile('ピ'), 'pee'],
		[re.compile('プ'), 'pu'],
		[re.compile('ペ'), 'pay'],
		[re.compile('ポ'), 'po'],

		[re.compile('マ'), 'ma'],
		[re.compile('ミ'), 'mee'],
		[re.compile('ム'), 'mu'],
		[re.compile('メ'), 'may'],
		[re.compile('モ'), 'mo'],

		[re.compile('ヤ'), 'ya'],
		[re.compile('ユ'), 'yu'],
		[re.compile('ヨ'), 'yo'],

		[re.compile('ラ'), 'la'],
		[re.compile('リ'), ' lee'],
		[re.compile('ル'), 'lu'],
		[re.compile('レ'), ' lay'],
		[re.compile('ロ'), ' low'],

		[re.compile('ワ'), 'wa'],
		[re.compile('ヲ'), 'wo'],

		[re.compile('ン'), 'n '],

		[re.compile('ア'), ' ah '],
		[re.compile('イ'), ' ee '],
		[re.compile('ウ'), ' u '],
		[re.compile('エ'), ' a '],
		[re.compile('オ'), ' o '],

		[re.compile('ァ'), 'ah'],
		[re.compile('ィ'), 'ee'],
		[re.compile('ゥ'), 'u'],
		[re.compile('ェ'), 'a'],
		[re.compile('ォ'), 'o'],

		[re.compile('ャ'), 'ya'],
		[re.compile('ュ'), 'yu'],
		[re.compile('ョ'), 'yo'],

		[re.compile('ッ'), ' '],
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
	# we don't want to use CharacterMode for replaced Japanese text
	a = []
	charmode = False
	for item in speechSequence:
		disableCharMode = False
		if isinstance(item, basestring):
			item = unicode_normalize(item)
			if isJapaneseLang(item):
				item = replaceJapanese(item)
				if charmode:
					disableCharMode = True
		elif isinstance(item, CharacterModeCommand):
			cmstate = item.state
		if disableCharMode:
			a.append(CharacterModeCommand(False))
			a.append(item)
			if charmode:
				a.append(CharacterModeCommand(True))
			disableCharMode = False
		else:
			a.append(item)
	return a
