# coding: UTF-8
# A part of NonVisual Desktop Access (NVDA)
# by Takuya Nishimoto (NVDA Japanese Team)
# jpDicTest.py for testing source/nvdajp_dic.py
# Usage:
# > cd jptools
# > python jpDicTest.py

from __future__ import unicode_literals, print_function
import unittest
import sys
sys.path.append(r'..\source')
import languageHandler
languageHandler.setLanguage('ja')
import nvdajp_dic as dic

class JpDicTestCase(unittest.TestCase):
	
	def test_getJapaneseDiscriminantReading(self):
		items = [
			('a', 'ハンカク エイジ a'), 
			('A', 'ハンカク エイジ オーモジ a'), 
			('あ', 'ヒラガナ あ'),
			('ア', 'カタカナ ア'),
			('あア', 'ヒラガナ あ カタカナ ア'),
			]
		for i in items:
			s = dic.getJapaneseDiscriminantReading(i[0])
			print("%s,%s,%s" % (i[0], i[1], s))
			self.assertEqual(s, i[1])

if __name__ == '__main__':
	unittest.main()





