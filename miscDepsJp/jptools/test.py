# -*- coding: UTF-8 -*-

import unittest

import jpBrailleRunner
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


if __name__ == "__main__":
    unittest.main()
