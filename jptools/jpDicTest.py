# coding: UTF-8
# -*- coding: utf-8 -*-
# A part of NonVisual Desktop Access (NVDA)
# by Takuya Nishimoto (NVDA Japanese Team)
# jpDicTest.py for testing source/jpUtils.py
# Usage:
# > miscDeps\tools\msgfmt.exe source\locale\ja\LC_MESSAGES\nvda.po -o source\locale\ja\LC_MESSAGES\nvda.mo
# > cd jptools
# > python jpDicTest.py

import unittest
import sys
from pathlib import Path

script_dir = Path(__file__).parent
sys.path.append(str(script_dir.parent / "source"))
sys.path.append(str(script_dir.parent / "miscdeps" / "python"))

import languageHandler  # noqa: E402

# Initialize globalVars before importing modules that depend on it.
import globalVars  # noqa: E402

appDir = str(Path(__file__).parent.parent.resolve())
globalVars.appDir = appDir

import gettext  # noqa: E402


# Mock config before importing jpDicUtils
class MockConfig:
	def __init__(self):
		self.conf = {
			"language": {
				"jpPhoneticReadingLatin": False,
				"jpPhoneticReadingKana": False,
				"jpKatakanaPitchChange": 0,
				"halfShapePitchChange": 0,
			},
			"speech": {
				"autoDialectSwitching": True,
				"autoLanguageSwitching": True,
			},
		}


# Create a mock config module with config attribute
class MockConfigModule:
	def __init__(self):
		self.config = MockConfig()
		self.conf = self.config.conf


sys.modules["config"] = MockConfigModule()

from jpDicUtils import (  # noqa: E402
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
	getAttrDesc,
	getJpAttr,
	getPitchChangeForCharAttr,
	code2hex,
	useAttrDesc,
	getOrd,
	splitChars,
	processKangxiRadicals,
	CharAttr,
	JpAttr,
)

languageHandler.setLanguage("ja")

gettext.translation(
	"nvda",
	localedir=str(script_dir.parent / "source" / "locale"),
	languages=["ja"],
).install()


class JpUtilsTestCase(unittest.TestCase):
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

	def test_getAttrDesc(self):
		a = CharAttr(True, False, False, False, False, False)
		self.assertEqual(getAttrDesc(a), "オオモジ ")

	def test_getJpAttr(self):
		a = getJpAttr("ja", "a", False)
		self.assertEqual(type(a), JpAttr)
		self.assertTrue(a.jpLatinCharacter)

	def test_getPitchChangeForCharAttr(self):
		a = getJpAttr("ja", "A", False)
		pitchChange = getPitchChangeForCharAttr(True, a, 50)
		self.assertEqual(pitchChange, 50)

	def test_code2hex(self):
		self.assertEqual(code2hex(0x123A), "u+123a")

	def test_useAttrDesc(self):
		a = CharAttr(True, False, False, False, False, False)
		self.assertEqual(useAttrDesc(["ー", a]), False)
		self.assertEqual(useAttrDesc(["あ", a]), True)

	def test_getOrd(self):
		self.assertEqual(getOrd("a"), 97)
		self.assertEqual(getOrd("𞀄"), 0x1E004)

	def test_splitChars(self):
		self.assertEqual(splitChars("a𞀄"), ["a", "𞀄"])

	def test_processKangxiRadicals(self):
		self.assertEqual(processKangxiRadicals("簡単に⾔えば"), "簡単に言えば")
		self.assertEqual(processKangxiRadicals("⾃由な発想"), "自由な発想")
		self.assertEqual(processKangxiRadicals("公益財団法⼈"), "公益財団法人")
		self.assertEqual(processKangxiRadicals("富⼭⽂化"), "富山文化")


if __name__ == "__main__":
	unittest.main()
