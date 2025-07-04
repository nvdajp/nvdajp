# coding: UTF-8
# A part of NonVisual Desktop Access (NVDA)
# by Takuya Nishimoto (NVDA Japanese Team)
# jpDicTest.py for testing source/jpUtils.py
# Usage:
# > miscDeps\tools\msgfmt.exe source\locale\ja\LC_MESSAGES\nvda.po -o source\locale\ja\LC_MESSAGES\nvda.mo
# > cd jptools
# > python jpDicTest.py

import unittest
import sys
import os

sys.path.append(os.path.normpath(os.path.join(os.getcwd(), "mocks")))
sys.path.append(r"..\source")
sys.path.append(r"..\miscdeps\python")

# Initialize globalVars.appDir before importing modules that depend on it
import globalVars

if not hasattr(globalVars, "appDir") or not globalVars.appDir:
	globalVars.appDir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

import languageHandler

languageHandler.setLanguage("ja")
from jpUtils import (  # noqa: E402
	getLongDesc,
	getShortDesc,
	isJa,
	isZenkakuHiragana,
	isZenkakuKatakana,
	isHankakuKatakana,
	isHalfShape,
	isFullShapeAlphabet,
	isHalfShapeAlphabet,
	isFullShapeNumber,
	isHalfShapeNumber,
	isKanaCharacter,
	isLatinCharacter,
	isFullShapeSymbol,
	isUpper,
	replaceSpecialKanaCharacter,
	getAttrDesc,
	getJpAttr,
	getCharDesc,
	getPitchChangeForCharAttr,
	getJaCharAttrDetails,
	code2kana,
	code2hex,
	getCandidateCharDesc,
	useAttrDesc,
	getOrd,
	splitChars,
	getDiscriminantReading,
	getDescriptionForBraille,
	processHexCode,
	fixNewText,
	processKangxiRadicals,
	CharAttr,
	JpAttr,
)

# import locale
import gettext  # noqa: E402

gettext.translation("nvda", localedir=r"..\source\locale", languages=["ja"]).install()

items = [
	("a", "半角 英字 エー アルファー", "半角 a"),
	("A", "半角 英字 オオモジ  エー アルファー", "半角 A"),
	("あ", "ヒラガナ あ", "ヒラガナ あ"),
	("ア", "カタカナ ア", "カタカナ ア"),
	("あア", "ヒラガナ あ カタカナ ア", "ヒラガナ あ カタカナ ア"),
	("を", "ヒラガナ オワリノ オ", "ヒラガナ を"),
	("ヲ", "カタカナ オワリノ オ", "カタカナ ヲ"),
	("123", "半角 イチ ニ サン", "半角 123"),
	("１２３", "全角 イチ ニ サン", "全角 １２３"),
	("1.23", "半角 イチ ピリオド ニ サン", "半角 1 ピリオド 23"),
	("１．２３", "全角 イチ ピリオド ニ サン", "全角 １．２３"),
	# ('1(23)', '半角 イチ カッコ ニ サン カッコトジ', '半角 1(23)'),
	# ('１（２３）', '全角 イチ カッコ ニ サン カッコトジ', '全角 １（２３）'),
	("川", "サンボンガワノ カワ", "サンボンガワノ カワ"),
	("^", "半角 ベキジョー", "半角 ベキジョー"),
	("⭕", "マル", "マル"),  # uses source/locale/ja/characters.dic
	("言", "ゲンゴガクノ ゲン", "ゲンゴガクノ ゲン"),  # 8a00
	("⾔", "ゲンゴガクノ ゲン コーキブシュ", "ゲンゴガクノ ゲン 康熙部首"),  # 2f94 Kangxi Radicals
	("鬼", "キ オニノ キ", "キ オニノ キ"),  # 9b3c
	("⿁", "キ オニノ キ コーキブシュ", "キ オニノ キ 康熙部首"),  # 2fc1 Kangxi Radicals
	("⻤", "キ オニノ キ ブシュホジョ", "キ オニノ キ 部首補助"),  # 2ee4 CJK Radicals Supplement
]


class JpUtilsTestCase(unittest.TestCase):
	def test_getLongDesc(self):
		self.assertEqual(getLongDesc("a"), "エー アルファー")

	def test_getShortDesc(self):
		self.assertEqual(getShortDesc("a"), "エー アルファー")

	def test_isJa(self):
		self.assertTrue(isJa("ja"))

	def test_isZenkakuHiragana(self):
		self.assertTrue(isZenkakuHiragana("あ"))

	def test_isZenkakuKatakana(self):
		self.assertTrue(isZenkakuKatakana("ア"))

	def test_isHankakuKatakana(self):
		self.assertTrue(isHankakuKatakana("ｱ"))

	def test_isHalfShape(self):
		self.assertTrue(isHalfShape("1"))

	def test_isFullShapeAlphabet(self):
		self.assertTrue(isFullShapeAlphabet("Ａ"))

	def test_isHalfShapeAlphabet(self):
		self.assertTrue(isHalfShapeAlphabet("A"))

	def test_isFullShapeNumber(self):
		self.assertTrue(isFullShapeNumber("１"))

	def test_isHalfShapeNumber(self):
		self.assertTrue(isHalfShapeNumber("1"))

	def test_isKanaCharacter(self):
		self.assertTrue(isKanaCharacter("ア"))

	def test_isLatinCharacter(self):
		self.assertTrue(isLatinCharacter("a"))

	def test_isFullShapeSymbol(self):
		self.assertTrue(isFullShapeSymbol("＠"))

	def test_isUpper(self):
		self.assertTrue(isUpper("A"))

	def test_replaceSpecialKanaCharacter(self):
		self.assertEqual(replaceSpecialKanaCharacter("ー"), "チョーオン")

	def test_getAttrDesc(self):
		a = CharAttr(True, False, False, False, False, False)
		self.assertEqual(getAttrDesc(a), "オオモジ ")

	def test_getJpAttr(self):
		a = getJpAttr("ja", "a", False)
		self.assertEqual(type(a), JpAttr)
		self.assertTrue(a.jpLatinCharacter)

	def test_getCharDesc(self):
		a = getJpAttr("ja", "a", False)
		desc = getCharDesc("ja", "a", a)
		self.assertEqual(desc, ("エー アルファー",))

	def test_getPitchChangeForCharAttr(self):
		a = getJpAttr("ja", "A", False)
		pitchChange = getPitchChangeForCharAttr("ja", a, True)
		self.assertEqual(pitchChange, True)

	def test_getJaCharAttrDetails(self):
		self.assertEqual(getJaCharAttrDetails("A", False, True), "半角 英字")

	def test_code2kana(self):
		self.assertEqual(code2kana(0x0123), "ゼロイチニーサン")

	def test_code2hex(self):
		self.assertEqual(code2hex(0x123A), "u+123a")

	def test_getCandidateCharDesc(self):
		a = CharAttr(True, False, False, False, False, False)
		self.assertEqual(getCandidateCharDesc("a", a, False), " エー アルファー ")

	def test_useAttrDesc(self):
		a = CharAttr(True, False, False, False, False, False)
		self.assertEqual(useAttrDesc(["ー", a]), False)
		self.assertEqual(useAttrDesc(["あ", a]), True)

	def test_getOrd(self):
		self.assertEqual(getOrd("a"), 97)
		self.assertEqual(getOrd("𞀄"), 0x1E004)

	def test_splitChars(self):
		self.assertEqual(splitChars("a𞀄"), ["a", "𞀄"])

	def test_getDiscriminantReading(self):
		for source, saycap_expected, braille_expected in items:
			saycap = getDiscriminantReading(source, sayCapForCapitals=True)
			self.assertEqual(saycap_expected, saycap)
			braille = getDiscriminantReading(source, forBraille=True)
			self.assertEqual(braille_expected, braille)

	def test_getDescriptionForBraille(self):
		self.assertEqual(getDescriptionForBraille("a"), "半角 a")

	def test_processHexCode(self):
		self.assertEqual(processHexCode("ja", "u+0000"), "u+ゼロゼロゼロゼロ")

	def test_fixNewText(self):
		self.assertEqual(fixNewText("あ"), "ア")
		self.assertEqual(fixNewText("ー"), " チョーオン ")

	def test_processKangxiRadicals(self):
		self.assertEqual(processKangxiRadicals("簡単に⾔えば"), "簡単に言えば")
		self.assertEqual(processKangxiRadicals("⾃由な発想"), "自由な発想")
		self.assertEqual(processKangxiRadicals("公益財団法⼈"), "公益財団法人")
		self.assertEqual(processKangxiRadicals("富⼭⽂化"), "富山文化")


if __name__ == "__main__":
	unittest.main()
