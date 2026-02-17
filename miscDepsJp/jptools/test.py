# -*- coding: UTF-8 -*-

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
		self.assertEqual(count, 0, "translator_louis: %d error(s). see %s (scons source required)" % (count, outfile))

	def test_eng2_ueb_g2(self):
		"""eng2Harness の UEB 2級点字を検証（原文→translator2(louis)→translator1 と ueb_g2 比較）。louis 未ビルド時はスキップ。"""
		count, outfile = jpBrailleRunner.run_eng2_ueb_g2()
		self.assertEqual(count, 0, "eng2_ueb_g2: %d error(s). see %s" % (count, outfile))

	def test_eng2_us_g2(self):
		"""eng2Harness の US 2級点字を検証（原文→translator2(louis en-us-g2)→translator1 と us_g2 比較）。louis 未ビルド時はスキップ。"""
		count, outfile = jpBrailleRunner.run_eng2_us_g2()
		self.assertEqual(count, 0, "eng2_us_g2: %d error(s). see %s" % (count, outfile))


class MecabTests(unittest.TestCase):
	def test_all(self):
		count = mecabRunner.runTasks(enableUserDic=False)
		self.assertEqual(count, 0)
		count = mecabRunner.runTasks(enableUserDic=True)
		self.assertEqual(count, 0)


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


if __name__ == "__main__":
	unittest.main()
