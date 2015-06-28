# coding: UTF-8
# A part of NonVisual Desktop Access (NVDA)
# by Takuya Nishimoto (NVDA Japanese Team)
# jpDicTest.py for testing source/nvdajp_dic.py
# Usage:
# > cd jptools
# > python jpDicTest.py

from __future__ import unicode_literals, print_function
import unittest
import sys, os
sys.path.append(os.path.normpath(os.path.join(os.getcwdu(), 'mocks')))
sys.path.append(r'..\source')
import languageHandler
languageHandler.setLanguage('ja')
import nvdajp_dic as dic

items = [
	('a', '半角 英字 エー アルファー', '半角 a'),
	('A', '半角 英字 大文字 エー アルファー', '半角 A'),
	('あ', 'ヒラガナ あ', 'ヒラガナ あ'),
	('ア', 'カタカナ ア', 'カタカナ ア'),
	('あア', 'ヒラガナ あ カタカナ ア', 'ヒラガナ あ カタカナ ア'),
	('を', 'ヒラガナ オワリノ オ', 'ヒラガナ を'),
	('ヲ', 'カタカナ オワリノ オ', 'カタカナ ヲ'),
	('123', '半角 イチ ニ サン', '半角 123'),
	('１２３', '全角 イチ ニ サン', '全角 １２３'),
	('1.23', '半角 イチ .ニ サン', '半角 1.23'),
	('１．２３', '全角 イチ ピリオド ニ サン', '全角 １．２３'),
	#('1(23)', '半角 イチ カッコ ニ サン カッコトジ', '半角 1(23)'),
	#('１（２３）', '全角 イチ カッコ ニ サン カッコトジ', '全角 １（２３）'),
	('川', 'サンボンガワノ カワ', 'サンボンガワノ カワ'),
]

class JpDicTestCase(unittest.TestCase):
	
	def test_getJapaneseDiscriminantReading(self):
		for i in items:
			a, b, c = i[0], i[1], i[2]
			s = dic.getJapaneseDiscriminantReading(a)
			print("name(%s) correctS(%s) actualS(%s)" % (a, b, s))
			self.assertEqual(b, s)
			t = dic.getJapaneseDiscriminantReading(a, forBraille=True)
			print("name(%s) correctB(%s) actualB(%s)" % (a, c, t))
			self.assertEqual(c, t)

if __name__ == '__main__':
	unittest.main()





