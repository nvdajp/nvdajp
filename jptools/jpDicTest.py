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
			('a', 'ハンカク エイジ エー アルファー'),
			('A', 'ハンカク エイジ オーモジ エー アルファー'),
			('あ', 'ヒラガナ あ'),
			('ア', 'カタカナ ア'),
			('あア', 'ヒラガナ あ カタカナ ア'),
			('123', 'ハンカク イチ ニ サン'),
			('１２３', 'ゼンカク イチ ニ サン'),
			]
		for i in items:
			a, b = i[0], i[1]
			s = dic.getJapaneseDiscriminantReading(a)
			print("(%s),(%s),(%s)" % (a, b, s))
			self.assertEqual(s, b)

if __name__ == '__main__':
	unittest.main()





