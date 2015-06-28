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

class JpDicTestCase(unittest.TestCase):
	
	def test_getJapaneseDiscriminantReading(self):
		items = [
			('a', '半角 英字 エー アルファー'),
			('A', '半角 英字 大文字 エー アルファー'),
			('あ', 'ヒラガナ あ'),
			('ア', 'カタカナ ア'),
			('あア', 'ヒラガナ あ カタカナ ア'),
			('を', 'ヒラガナ オワリノ オ'),
			('ヲ', 'カタカナ オワリノ オ'),
			('123', '半角 イチ ニ サン'),
			('１２３', '全角 イチ ニ サン'),
			]
		for i in items:
			a, b = i[0], i[1]
			s = dic.getJapaneseDiscriminantReading(a)
			print("(%s),(%s),(%s)" % (a, b, s))
			self.assertEqual(s, b)

if __name__ == '__main__':
	unittest.main()





