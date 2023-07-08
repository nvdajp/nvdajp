# coding: UTF-8
# A part of NonVisual Desktop Access (NVDA)
# by Takuya Nishimoto (NVDA Japanese Team)
# jpDicTest.py for testing source/nvdajp_dic.py
# Usage:
# > miscDeps\tools\msgfmt.exe source\locale\ja\LC_MESSAGES\nvda.po -o source\locale\ja\LC_MESSAGES\nvda.mo
# > cd jptools
# > python jpDicTest.py

import unittest
import sys, os

sys.path.append(os.path.normpath(os.path.join(os.getcwd(), "mocks")))
sys.path.append(r"..\source")
sys.path.append(r"..\miscdeps\python")
import languageHandler

languageHandler.setLanguage("ja")
import jpUtils

# import locale
import gettext

gettext.translation("nvda", localedir=r"..\source\locale", languages=["ja"]).install(
    True
)

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
    ("1.23", "半角 イチ .ニ サン", "半角 1.23"),
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
    def test_getDiscriminantReading(self):
        for source, saycap_expected, braille_expected in items:
            saycap = jpUtils.getDiscriminantReading(source, sayCapForCapitals=True)
            self.assertEqual(saycap_expected, saycap)
            braille = jpUtils.getDiscriminantReading(source, forBraille=True)
            self.assertEqual(braille_expected, braille)

    def test_code2kana(self):
        self.assertEqual(jpUtils.code2kana(0x0123), "ゼロイチニーサン")

    def test_code2hex(self):
        self.assertEqual(jpUtils.code2hex(0x123a), "u+123a")

    def test_processKangxiRadicals(self):
        self.assertEqual(jpUtils.processKangxiRadicals("簡単に⾔えば"), "簡単に言えば")
        self.assertEqual(jpUtils.processKangxiRadicals("⾃由な発想"), "自由な発想")
        self.assertEqual(jpUtils.processKangxiRadicals("公益財団法⼈"), "公益財団法人")
        self.assertEqual(jpUtils.processKangxiRadicals("富⼭⽂化"), "富山文化")

if __name__ == "__main__":
    unittest.main()
