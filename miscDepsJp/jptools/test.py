# -*- coding: UTF-8 -*-
"""JP smoke tests (MeCab, braille, JTalk).

unittest runs test *classes* in alphabetical order:

1. JpBrailleTests (test_translator2 initializes MeCab with user_dics)
2. JtalkPrepareTests / JtalkTests (jtalk_pipeline_probe expects base dictionary)
3. MecabTests (runTasks without then with user_dics)

See projectDocs/jp/tab-character-analysis.md (2026-06-11, PR #663).

The user dictionary (jtusr.dic) is rebuilt from jtusr.csv by
build_userdic.py with the x64 mecab-dict-index.exe prepared by
"scons jtalkSync". See projectDocs/jp/userdic.md.
"""

import unittest

import jpBrailleRunner
import jtalk_pipeline_probe
import jtalkPredicTest
import jtalkRunner
import mecabRunner


class JpBrailleTests(unittest.TestCase):
	def test_translator2(self):
		"""translator2（MeCab・マスあけ・引用符範囲）。パイプライン1番目。"""
		count, outfile = jpBrailleRunner.run_translator2()
		self.assertEqual(count, 0)

	def test_translator1(self):
		"""translator1（カナ→点字）。パイプライン3番目。"""
		count, outfile = jpBrailleRunner.run_translator1()
		self.assertEqual(count, 0)

	def test_eng2_grade1(self):
		"""eng2Harness の1級点字を検証（原文→translator2→translator1 と output 比較）。"""
		count, outfile = jpBrailleRunner.run_eng2_grade1()
		self.assertEqual(count, 0, "eng2 grade1: %d error(s). see %s" % (count, outfile))

	def test_translator_louis(self):
		"""translator_louis 単体: liblouis en-ueb-g2.ctb で英文を UEB G2 に変換。louis 未ビルド時はスキップ。"""
		count, outfile = jpBrailleRunner.run_translator_louis()
		self.assertEqual(
			count, 0, "translator_louis: %d error(s). see %s (scons source required)" % (count, outfile),
		)

	def test_eng2_ueb_g2(self):
		"""eng2Harness の UEB 2級点字を検証（原文→translator2(louis)→translator1 と ueb_g2 比較）。louis 未ビルド時はスキップ。"""
		count, outfile = jpBrailleRunner.run_eng2_ueb_g2()
		self.assertEqual(count, 0, "eng2_ueb_g2: %d error(s). see %s" % (count, outfile))

	def test_eng2_us_g2(self):
		"""eng2Harness の US 2級点字を検証（原文→translator2(louis en-us-g2)→translator1 と us_g2 比較）。louis 未ビルド時はスキップ。"""
		count, outfile = jpBrailleRunner.run_eng2_us_g2()
		self.assertEqual(count, 0, "eng2_us_g2: %d error(s). see %s" % (count, outfile))

	def test_eng2_nabcc_regression(self):
		"""nabcc+2級併用の回帰テスト。nabcc=True で louis 2級パイプラインを実行し、クラッシュせず正常終了することを検証。louis 未ビルド時はスキップ。"""
		count, outfile = jpBrailleRunner.run_eng2_nabcc_regression()
		self.assertEqual(count, 0, "eng2_nabcc_regression: %d error(s). see %s" % (count, outfile))


class MecabTests(unittest.TestCase):
	def test_all(self):
		count = mecabRunner.runTasks(enableUserDic=False)
		self.assertEqual(count, 0)
		count = mecabRunner.runTasks(enableUserDic=True)
		self.assertEqual(count, 0)

	def test_user_dic_applied(self):
		"""User dictionary entry must actually win over the base analysis.

		The jtusr.csv sample word is split into several morphemes by the
		base dictionary and becomes a single morpheme (with the braille
		segmentation from the CSV) once jtusr.dic is loaded. This catches
		both load failures (incompatible dictionary) and entries that are
		never selected (context ID / cost mistakes).
		"""
		result = mecabRunner.probeUserDic()
		baseSize = result["base"][0]
		userSize, userReading, userBraille = result["user"]
		self.assertGreater(
			baseSize, 1, "base dictionary should split the sample word: %r" % (result["base"],),
		)
		self.assertEqual(userSize, 1, "user dic entry not selected: %r" % (result["user"],))
		# The braille segmentation must match the harness.json entry for the
		# same word so that translator2 results do not depend on whether the
		# user dictionary is loaded.
		self.assertEqual(userReading, "ジセダイガタテンジピンディスプレイ")
		self.assertEqual(userBraille, "ジセダイガタテンジピン ディスプレイ")


class JtalkPrepareTests(unittest.TestCase):
	def test_all(self):
		count = jtalkPredicTest.runTasks()
		self.assertEqual(count, 0)


class JtalkTests(unittest.TestCase):
	def test_jtalk(self):
		ret = jtalkRunner.main(do_play=False, do_write=False, do_log=False)
		self.assertEqual(ret, 0)

	def test_jtalk_regression_menu_sentence(self):
		text = (
			"NVDAを操作する多くのコマンドでは、NVDA制御キーを押しながら他のキーを押します。\n"
			"初期状態ではInsertキーおよびテンキーのInsertキーの両方がNVDA制御キーとして使えます。\n"
			"NVDA+NまたはシステムトレイのアイコンでNVDAメニューが開きます。\n"
			"NVDAメニューには、NVDAの終了、設定、ヘルプ、その他の機能があります。\n"
			"タッチモードでは2本指2回タップでNVDAメニューが開きます。"
		)
		result = jtalk_pipeline_probe.probe_text(text, feature_limit=256)
		self.assertTrue(result["hasWave"])
		self.assertGreater(result["waveBytes"], 0)
		self.assertGreater(result["tokenCount"], 20)
		self.assertIn("nvda", result["prepared"].lower())

	def test_jtalk_digit_compound_twelve(self):
		"""12 must be synthesized as juu-ni, not digit-by-digit ichi-ni."""
		result = jtalk_pipeline_probe.probe_digit_compound("12")
		self.assertTrue(result["hasWave"])
		self.assertEqual(result["mecabTokenCount"], 2)
		self.assertTrue(
			result["digitMerged"],
			"njd_set_digit failed to merge 12; labels=%r" % result["labelsSnippet"],
		)


if __name__ == "__main__":
	unittest.main()
