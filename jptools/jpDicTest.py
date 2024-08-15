# coding: UTF-8
# A part of NonVisual Desktop Access (NVDA)
# by Takuya Nishimoto (NVDA Japanese Team)
# jpDicTest.py for testing source/nvdajp_dic.py
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
import languageHandler

languageHandler.setLanguage("ja")
import jpUtils  # noqa: E402

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
    ("鬼", "キ オニノ キ", "キ オニノ キ"), # 9b3c
    ("⿁", "キ オニノ キ コーキブシュ", "キ オニノ キ 康熙部首"), # 2fc1 Kangxi Radicals
    ("⻤", "キ オニノ キ ブシュホジョ", "キ オニノ キ 部首補助"), # 2ee4 CJK Radicals Supplement
]


class JpUtilsTestCase(unittest.TestCase):
    def test_getLongDesc(self):
        self.assertEqual(jpUtils.getLongDesc("a"), "エー アルファー")

    def test_getShortDesc(self):
        self.assertEqual(jpUtils.getShortDesc("a"), "エー アルファー")

    def test_isJa(self):
        self.assertTrue(jpUtils.isJa("ja"))

    def test_isZenkakuHiragana(self):
        self.assertTrue(jpUtils.isZenkakuHiragana("あ"))

    def test_isZenkakuKatakana(self):
        self.assertTrue(jpUtils.isZenkakuKatakana("ア"))

    def test_isHankakuKatakana(self):
        self.assertTrue(jpUtils.isHankakuKatakana("ｱ"))

    def test_isHalfShape(self):
        self.assertTrue(jpUtils.isHalfShape("1"))

    def test_isFullShapeAlphabet(self):
        self.assertTrue(jpUtils.isFullShapeAlphabet("Ａ"))

    def test_isHalfShapeAlphabet(self):
        self.assertTrue(jpUtils.isHalfShapeAlphabet("A"))

    def test_isFullShapeNumber(self):
        self.assertTrue(jpUtils.isFullShapeNumber("１"))

    def test_isHalfShapeNumber(self):
        self.assertTrue(jpUtils.isHalfShapeNumber("1"))

    def test_isKanaCharacter(self):
        self.assertTrue(jpUtils.isKanaCharacter("ア"))

    def test_isLatinCharacter(self):
        self.assertTrue(jpUtils.isLatinCharacter("a"))

    def test_isFullShapeSymbol(self):
        self.assertTrue(jpUtils.isFullShapeSymbol("＠"))

    def test_isUpper(self):
        self.assertTrue(jpUtils.isUpper("A"))

    def test_replaceSpecialKanaCharacter(self):
        self.assertEqual(jpUtils.replaceSpecialKanaCharacter("ー"), "チョーオン")

    def test_getAttrDesc(self):
        a = jpUtils.CharAttr(True, False, False, False, False, False)
        self.assertEqual(jpUtils.getAttrDesc(a), "オオモジ ")

    def test_getJpAttr(self):
        a = jpUtils.getJpAttr("ja", "a", False)
        self.assertEqual(type(a), jpUtils.JpAttr)
        self.assertTrue(a.jpLatinCharacter)

    def test_getCharDesc(self):
        a = jpUtils.getJpAttr("ja", "a", False)
        desc = jpUtils.getCharDesc("ja", "a", a)
        self.assertEqual(desc, ("エー アルファー",))

    def test_getPitchChangeForCharAttr(self):
        a = jpUtils.getJpAttr("ja", "A", False)
        pitchChange = jpUtils.getPitchChangeForCharAttr("ja", a, True)
        self.assertEqual(pitchChange, True)

    def test_getJaCharAttrDetails(self):
        self.assertEqual(jpUtils.getJaCharAttrDetails("A", False, True), "半角 英字")

    def test_code2kana(self):
        self.assertEqual(jpUtils.code2kana(0x0123), "ゼロイチニーサン")

    def test_code2hex(self):
        self.assertEqual(jpUtils.code2hex(0x123a), "u+123a")

    def test_getCandidateCharDesc(self):
        a = jpUtils.CharAttr(True, False, False, False, False, False)
        self.assertEqual(jpUtils.getCandidateCharDesc("a", a, False), ' エー アルファー ')

    def test_useAttrDesc(self):
        a = jpUtils.CharAttr(True, False, False, False, False, False)
        self.assertEqual(jpUtils.useAttrDesc(["ー", a]), False)
        self.assertEqual(jpUtils.useAttrDesc(["あ", a]), True)

    def test_getOrd(self):
        self.assertEqual(jpUtils.getOrd("a"), 97)
        self.assertEqual(jpUtils.getOrd("𞀄"), 0x1e004)

    def test_splitChars(self):
        self.assertEqual(jpUtils.splitChars("a𞀄"), ['a', '𞀄'])

    def test_getDiscriminantReading(self):
        for source, saycap_expected, braille_expected in items:
            saycap = jpUtils.getDiscriminantReading(source, sayCapForCapitals=True)
            self.assertEqual(saycap_expected, saycap)
            braille = jpUtils.getDiscriminantReading(source, forBraille=True)
            self.assertEqual(braille_expected, braille)

    def test_getDiscrptionForBraille(self):
        self.assertEqual(jpUtils.getDiscrptionForBraille("a"), "半角 a")

    def test_processHexCode(self):
        self.assertEqual(jpUtils.processHexCode("ja", "u+0000"), "u+ゼロゼロゼロゼロ")

    def test_fixNewText(self):
        self.assertEqual(jpUtils.fixNewText("あ"), "ア")
        self.assertEqual(jpUtils.fixNewText("ー"), " チョーオン ")

    def test_processKangxiRadicals(self):
        self.assertEqual(jpUtils.processKangxiRadicals("簡単に⾔えば"), "簡単に言えば")
        self.assertEqual(jpUtils.processKangxiRadicals("⾃由な発想"), "自由な発想")
        self.assertEqual(jpUtils.processKangxiRadicals("公益財団法⼈"), "公益財団法人")
        self.assertEqual(jpUtils.processKangxiRadicals("富⼭⽂化"), "富山文化")

if __name__ == "__main__":
    unittest.main()
