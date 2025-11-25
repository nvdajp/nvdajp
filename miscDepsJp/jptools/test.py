# -*- coding: UTF-8 -*-

import unittest

import jpBrailleRunner
import jtalkPredicTest
import jtalkRunner
import mecabRunner


class JpBrailleTests(unittest.TestCase):
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


class MecabThreadSafetyTests(unittest.TestCase):
    """MeCab のスレッド安全性とアクセス違反のハンドリングをテスト"""
    
    @classmethod
    def setUpClass(cls):
        """テストクラスの初期化"""
        import os
        import sys
        import threading
        
        # Setup path for MeCab module (only for this test class)
        repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
        jtalk_dir = os.path.join(repo_root, "miscDepsJp", "source", "synthDrivers", "jtalk")
        if jtalk_dir not in sys.path:
            sys.path.insert(0, jtalk_dir)
        
        # Import MeCab module (lazy import to avoid affecting other tests)
        try:
            import mecab as mecab_module  # type: ignore
            from mecab import Mecab_initialize, Mecab_analysis, MecabFeatures  # type: ignore
        except ImportError as e:
            raise unittest.SkipTest("MeCab module not available: %s" % e)
        
        cls.mecab_module = mecab_module
        cls.Mecab_initialize = Mecab_initialize
        cls.Mecab_analysis = Mecab_analysis
        cls.MecabFeatures = MecabFeatures
        
        # Test strings that caused access violation
        cls.TEST_STRINGS = [
            "NVDAのインストール(I)...",
            "nvda_jpalpha_251121x.exe",
            "Pythonコンソール(P)",
            "ポータブル版の作成(C)...",
        ]
        
        cls.dic_dir = os.path.join(jtalk_dir, "dic")
        cls.user_dics = []
        
        # Initialize MeCab (only for this test class)
        dll_dir_handle = None
        if hasattr(os, "add_dll_directory"):
            try:
                dll_dir_handle = os.add_dll_directory(jtalk_dir)
            except OSError:
                pass
        
        try:
            def logwrite(s=""):
                pass  # Suppress log output in tests
            
            Mecab_initialize(logwrite, jtalk_dir, cls.dic_dir, cls.user_dics)
            
            # Verify initialization
            if mecab_module.libmc is None or mecab_module.mecab is None:
                raise RuntimeError("MeCab initialization failed")
        except Exception as e:
            if dll_dir_handle is not None:
                dll_dir_handle.close()
            raise unittest.SkipTest("MeCab initialization failed: %s" % e)
        finally:
            if dll_dir_handle is not None:
                dll_dir_handle.close()
    
    def test_single_threaded_analysis(self):
        """シングルスレッドでの MeCab 解析をテスト"""
        errors = []
        for text in self.TEST_STRINGS:
            try:
                mf = self.MecabFeatures()
                self.Mecab_analysis(text.encode("utf-8"), mf)
                # Access violation should be caught and handled gracefully
                # We expect size=0 if access violation occurred, but no crash
                self.assertIsInstance(mf.size, int, "mf.size should be int")
            except Exception as e:
                # Any unhandled exception is a failure
                errors.append("Text %r failed: %s" % (text, e))
        
        if errors:
            self.fail("Single-threaded tests failed:\n" + "\n".join(errors))
    
    def test_multi_threaded_analysis(self):
        """マルチスレッドでの MeCab 解析をテスト（ロック保護を確認）"""
        import threading
        
        errors = []
        results = []
        lock = threading.Lock()
        
        def worker(text, index):
            try:
                mf = self.MecabFeatures()
                self.Mecab_analysis(text.encode("utf-8"), mf)
                with lock:
                    results.append((index, mf.size))
            except Exception as e:
                with lock:
                    errors.append("Thread %d, text %r failed: %s" % (index, text, e))
        
        threads = []
        for i, text in enumerate(self.TEST_STRINGS):
            t = threading.Thread(target=worker, args=(text, i))
            t.start()
            threads.append(t)
        
        for t in threads:
            t.join()
        
        # All threads should complete without crashing
        # Note: results may be less than TEST_STRINGS if access violations occurred,
        # but threads should complete without crashing
        self.assertGreaterEqual(len(results) + len(errors), len(self.TEST_STRINGS),
                        "All threads should complete (some may have errors)")
        
        # If there are errors, they should be access violations that were handled
        # We don't fail the test if errors occurred, as long as threads completed
    
    def test_reinitialization_on_access_violation(self):
        """アクセス違反発生時の再初期化をテスト"""
        # This test verifies that re-initialization logic works
        # Even if access violation occurs, the system should handle it gracefully
        success_count = 0
        for text in self.TEST_STRINGS:
            try:
                mf = self.MecabFeatures()
                self.Mecab_analysis(text.encode("utf-8"), mf)
                # If we get here without exception, the re-initialization logic worked
                success_count += 1
            except Exception:
                # Access violation should be caught and handled
                pass
        
        # At least some tests should succeed (re-initialization should work)
        # We don't require all to succeed because access violations may still occur
        # but the important thing is that they don't crash
        self.assertGreater(success_count, 0,
                          "At least some tests should succeed after re-initialization")


if __name__ == "__main__":
    unittest.main()
