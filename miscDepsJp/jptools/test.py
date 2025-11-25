# -*- coding: UTF-8 -*-

import io
import os
import sys
import unittest

import jpBrailleRunner
import jtalkPredicTest
import jtalkRunner
import mecabRunner

# Setup path for translator2 import (same as jpBrailleRunner)
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
jtalk_dir = os.path.join(repo_root, "miscDepsJp", "source", "synthDrivers", "jtalk")
if jtalk_dir in sys.path:
    sys.path.remove(jtalk_dir)
sys.path.insert(0, jtalk_dir)
import translator2  # type: ignore


class JpBrailleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Initialize translator2 for tests that need it"""
        dic_dir = os.path.join(jtalk_dir, "dic")
        user_dics = []
        output = io.StringIO()

        def logwrite(s=""):
            output.write(s + "\n")

        dll_dir_handle = None
        if hasattr(os, "add_dll_directory"):
            try:
                dll_dir_handle = os.add_dll_directory(jtalk_dir)
            except OSError:
                pass

        try:
            translator2.initialize(logwrite, jtalk_dir, dic_dir, user_dics)
        finally:
            if dll_dir_handle is not None:
                dll_dir_handle.close()

    def test_pass1(self):
        try:
            count, outfile = jpBrailleRunner.pass1()
            self.assertEqual(count, 0, f"pass1 failed with {count} errors. See {outfile}")
        except Exception as e:
            self.fail(f"pass1 raised exception: {e}")

    def test_pass2(self):
        try:
            count, outfile = jpBrailleRunner.pass2()
            self.assertEqual(count, 0, f"pass2 failed with {count} errors. See {outfile}")
        except RuntimeError as e:
            self.fail(f"pass2 initialization failed: {e}")
        except Exception as e:
            self.fail(f"pass2 raised unexpected exception: {e}")

    def test_translateWithInPos2_return_order(self):
        """Verify that translateWithInPos2() returns values in the correct order.

        This test explicitly checks the return value order to catch issues like
        incorrect unpacking in jpBrailleRunner.pass2().

        Expected return order: (outbuf, result, inpos1, inpos2)
        - outbuf: kana representation (カナ表記)
        - result: braille output (点字)
        - inpos1: position mapping for translator1
        - inpos2: position mapping for translator2
        """
        # Test with a simple case that should produce different outbuf and result
        test_text = "あいうえお"

        # Call translateWithInPos2 directly
        outbuf, result, inpos1, inpos2 = translator2.translateWithInPos2(test_text)

        # Verify return types
        self.assertIsInstance(outbuf, str, "outbuf should be str")
        self.assertIsInstance(result, str, "result should be str")
        self.assertIsInstance(inpos1, list, "inpos1 should be list")
        self.assertIsInstance(inpos2, list, "inpos2 should be list")

        # Verify non-empty results
        self.assertGreater(len(outbuf), 0, "outbuf should not be empty")
        self.assertGreater(len(result), 0, "result should not be empty")
        self.assertGreater(len(inpos1), 0, "inpos1 should not be empty")
        self.assertGreater(len(inpos2), 0, "inpos2 should not be empty")

        # Verify that outbuf (kana) and result (braille) are different
        # outbuf should contain kana characters, result should contain braille
        # This helps catch if the order is swapped
        self.assertNotEqual(outbuf, result,
                          "outbuf (kana) and result (braille) should be different. "
                          "If they're the same, the return order might be wrong.")

        # Verify position mappings have correct lengths
        self.assertEqual(len(inpos1), len(outbuf),
                        "inpos1 length should match outbuf length")
        self.assertEqual(len(inpos2), len(test_text),
                        "inpos2 length should match input text length")


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
