# -*- coding: UTF-8 -*-

import unittest

import jpBrailleRunner
import jtalk_pipeline_probe
import jtalkPredicTest
import jtalkRunner
import mecabRunner


class JpBrailleTests(unittest.TestCase):
	def test_pass1(self):
		count, outfile = jpBrailleRunner.pass1()
		self.assertEqual(count, 0)

	def test_pass2(self):
		count, outfile = jpBrailleRunner.pass2()
		self.assertEqual(count, 0)


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
