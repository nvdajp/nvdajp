# -*- coding: UTF-8 -*-
"""
MeCab アクセス違反の再現スクリプト

ログから、以下の文字列でアクセス違反が発生：
- "NVDAのインストール(I)..."
- "nvda_jpalpha_251121x.exe"

バックグラウンドスレッドで MeCab を呼び出すことで再現を試みます。
"""

import os
import sys
import time
import threading

# Setup path
repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
jtalk_dir = os.path.join(repo_root, "miscDepsJp", "source", "synthDrivers", "jtalk")
if jtalk_dir in sys.path:
    sys.path.remove(jtalk_dir)
sys.path.insert(0, jtalk_dir)

# Import MeCab module
import mecab as mecab_module  # type: ignore
from mecab import Mecab_initialize, Mecab_analysis, MecabFeatures  # type: ignore

# Test strings that caused access violation
TEST_STRINGS = [
    "NVDAのインストール(I)...",
    "nvda_jpalpha_251121x.exe",
    "Pythonコンソール(P)",
    "ポータブル版の作成(C)...",
    "C:\\Users\\nishimotz\\Dropbox\\takuya\\Public - エクスプローラー",
]

dic_dir = os.path.join(jtalk_dir, "dic")
user_dics = []


def logwrite(s=""):
    print(f"[{threading.current_thread().name}] {s}")


def test_mecab_analysis(text):
    """MeCab 解析を実行"""
    try:
        print(f"\nTesting: {text!r}")
        mf = MecabFeatures()
        Mecab_analysis(text.encode("utf-8"), mf, logwrite_=logwrite)
        print(f"  Success: size={mf.size}")
        return True
    except OSError as e:
        if "access violation" in str(e).lower():
            print(f"  [ACCESS VIOLATION] DETECTED: {e}")
            return False
        else:
            print(f"  [WARNING] Other OSError: {e}")
            return False
    except Exception as e:
        print(f"  [ERROR] Exception: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False


def background_thread_test():
    """バックグラウンドスレッドでテスト"""
    print("\n=== Background Thread Test ===")

    def worker():
        for text in TEST_STRINGS:
            test_mecab_analysis(text)
            time.sleep(0.1)  # Small delay between tests

    threads = []
    for i in range(3):  # Multiple threads to stress test
        t = threading.Thread(target=worker, name=f"Worker-{i}")
        t.start()
        threads.append(t)

    for t in threads:
        t.join()


def rapid_fire_test():
    """連続で素早く呼び出すテスト"""
    print("\n=== Rapid Fire Test ===")
    for text in TEST_STRINGS * 10:  # Repeat 10 times
        test_mecab_analysis(text)
        time.sleep(0.01)  # Very short delay


def investigate_mecab_new_failure():
    """mecab_new が失敗する原因を詳細に調査"""
    print("\n" + "=" * 60)
    print("Investigating mecab_new failure...")
    print("=" * 60)

    import ctypes
    from ctypes import c_char_p, c_int, POINTER

    # Check dictionary files
    print("\n[Dictionary Files]")
    required_files = ["sys.dic", "matrix.bin", "char.bin", "unk.dic"]
    for name in required_files:
        fp = os.path.join(dic_dir, name)
        if os.path.isfile(fp):
            size = os.path.getsize(fp)
            print(f"  {name}: OK ({size:,} bytes)")
        else:
            print(f"  {name}: MISSING")

    # Check mecabrc
    print("\n[mecabrc]")
    mecabrc = os.path.join(jtalk_dir, "mecabrc")
    if os.path.isfile(mecabrc):
        size = os.path.getsize(mecabrc)
        print(f"  mecabrc: OK ({size} bytes)")
        if size > 0:
            try:
                with open(mecabrc, encoding="utf-8") as f:
                    content = f.read()
                    print(f"  Content:\n{content}")
            except Exception as e:
                print(f"  Failed to read: {e}")
        else:
            print("  WARNING: mecabrc is empty")
    else:
        print(f"  mecabrc: MISSING (will use temp file)")

    # Check libmecab.dll
    print("\n[libmecab.dll]")
    libmecab_dll = os.path.join(jtalk_dir, "libmecab.dll")
    if os.path.isfile(libmecab_dll):
        size = os.path.getsize(libmecab_dll)
        print(f"  libmecab.dll: OK ({size:,} bytes)")
    else:
        print(f"  libmecab.dll: MISSING")
        return

    # Try to load DLL and call mecab_new directly
    print("\n[Direct mecab_new test]")
    try:
        libmc = ctypes.cdll.LoadLibrary(libmecab_dll)
        print(f"  DLL loaded: {libmc}")

        # Setup function signatures
        libmc.mecab_new.restype = ctypes.c_void_p
        libmc.mecab_new.argtypes = [c_int, POINTER(c_char_p)]
        libmc.mecab_strerror.restype = c_char_p
        libmc.mecab_strerror.argtypes = [ctypes.c_void_p]

        # Prepare arguments
        dic_for_mecab = dic_dir.replace("\\", "/")
        mecabrc_path = mecabrc if os.path.isfile(mecabrc) and os.path.getsize(mecabrc) > 0 else None

        if mecabrc_path:
            argc = 5
            args = (c_char_p * 5)(
                b"mecab",
                b"-d",
                dic_for_mecab.encode("utf-8"),
                b"-r",
                mecabrc_path.encode("utf-8"),
            )
        else:
            # Create temp mecabrc
            import tempfile
            tmp = tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", delete=False, suffix="mecabrc")
            tmp.write(f"dicdir = {dic_for_mecab}\n")
            tmp.write("input-buffer-size = 8192\n")
            tmp.close()
            mecabrc_path = tmp.name
            argc = 5
            args = (c_char_p * 5)(
                b"mecab",
                b"-d",
                dic_for_mecab.encode("utf-8"),
                b"-r",
                mecabrc_path.encode("utf-8"),
            )

        print(f"  Calling mecab_new with:")
        print(f"    argc={argc}")
        for i in range(argc):
            try:
                arg_str = args[i].decode("utf-8", "ignore")
                print(f"    args[{i}]={arg_str!r}")
            except:
                print(f"    args[{i}]={repr(args[i])}")

        # Call mecab_new
        mecab_ptr = libmc.mecab_new(argc, args)
        print(f"  mecab_new returned: {mecab_ptr}")
        print(f"    Type: {type(mecab_ptr)}")
        print(f"    Value as int: {mecab_ptr if mecab_ptr else 'None'}")

        if mecab_ptr:
            # Try to get error message
            print(f"  Testing mecab_strerror...")
            try:
                # Convert int to c_void_p for mecab_strerror
                mecab_void_p = ctypes.c_void_p(mecab_ptr)
                err_msg = libmc.mecab_strerror(mecab_void_p)
                if err_msg:
                    print(f"  mecab_strerror: {err_msg.decode('utf-8', 'ignore')}")
                else:
                    print(f"  mecab_strerror: (empty)")
            except Exception as e:
                print(f"  mecab_strerror failed: {e}")
                print(f"    This indicates mecab pointer is invalid!")
                import traceback
                traceback.print_exc()

            # Try to use mecab_sparse_tonode to test if pointer is valid
            print(f"  Testing mecab_sparse_tonode...")
            try:
                libmc.mecab_sparse_tonode.restype = ctypes.c_void_p
                libmc.mecab_sparse_tonode.argtypes = [ctypes.c_void_p, c_char_p]
                test_text = b"test"
                mecab_void_p = ctypes.c_void_p(mecab_ptr)
                result = libmc.mecab_sparse_tonode(mecab_void_p, test_text)
                print(f"  mecab_sparse_tonode: {result}")
            except Exception as e:
                print(f"  mecab_sparse_tonode failed: {e}")
                import traceback
                traceback.print_exc()
        else:
            print(f"  mecab_new returned NULL/None")
            # Try to get last error
            try:
                if hasattr(ctypes, "get_last_error"):
                    last_error = ctypes.get_last_error()
                    print(f"  GetLastError: {last_error}")
            except:
                pass

    except Exception as e:
        print(f"  [ERROR] Direct test failed: {e}")
        import traceback
        traceback.print_exc()


def main():
    print("MeCab Access Violation Reproduction Script")
    print("=" * 60)

    # Investigate mecab_new failure first
    investigate_mecab_new_failure()

    # Initialize MeCab
    print("\n" + "=" * 60)
    print("Initializing MeCab...")
    dll_dir_handle = None
    if hasattr(os, "add_dll_directory"):
        try:
            dll_dir_handle = os.add_dll_directory(jtalk_dir)
            print(f"  add_dll_directory: OK")
        except OSError as e:
            print(f"  WARNING: add_dll_directory failed: {e}")

    try:
        Mecab_initialize(logwrite, jtalk_dir, dic_dir, user_dics)
        print("  MeCab initialized successfully")

        # Verify initialization
        if mecab_module.libmc is None or mecab_module.mecab is None:
            print("  [ERROR] MeCab initialization failed!")
            print(f"    libmc={mecab_module.libmc}, mecab={mecab_module.mecab}")
            return 1
        else:
            print(f"  [OK] libmc={mecab_module.libmc}, mecab={mecab_module.mecab}")
    except Exception as e:
        print(f"  [ERROR] Failed to initialize MeCab: {e}")
        import traceback
        traceback.print_exc()
        return 1
    finally:
        if dll_dir_handle is not None:
            dll_dir_handle.close()

    # Run tests
    print("\n" + "=" * 60)
    print("Running single-threaded tests...")
    for text in TEST_STRINGS:
        test_mecab_analysis(text)
        time.sleep(0.1)

    # Run multi-threaded test
    print("\n" + "=" * 60)
    background_thread_test()

    # Run rapid fire test
    print("\n" + "=" * 60)
    rapid_fire_test()

    print("\n" + "=" * 60)
    print("Test completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
