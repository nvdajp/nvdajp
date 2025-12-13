# -*- coding: utf-8 -*-
# jptools/jpBrailleRunner.py
# A part of NonVisual Desktop Access (NVDA)
# This file is covered by the GNU General Public License.
# See the file COPYING for more details.
# Copyright (C) 2013 Masataka.Shinke, Takuya Nishimoto
# h1: カナと記号のテスト
# h2: テキスト解析とマスあけのテスト

import datetime
import io
import optparse
import os
import sys
import timeit

from harness import tests
from nabccHarness import tests as nabcc_tests

tests.extend(nabcc_tests)

from os import getcwd

open_file = lambda name, mode: open(name, mode, encoding="utf-8")

# Use __file__ to get the script's directory, which is more reliable than getcwd()
# jpBrailleRunner.py is in miscDepsJp/jptools
script_dir = os.path.dirname(os.path.abspath(__file__))
# script_dir -> miscDepsJp/jptools
# ../.. -> repo root
repo_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
# Verify repo_root contains miscDepsJp
if not os.path.exists(os.path.join(repo_root, "miscDepsJp")):
    # Fallback: try going up one more level if current calculation is wrong
    repo_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
jtalk_dir = os.path.join(repo_root, "source", "synthDrivers", "jtalk")
# Use source/synthDrivers/jtalk directly (files moved from miscDepsJp in Phase 1)
# Remove any existing occurrence to ensure correct import path
if jtalk_dir in sys.path:
    sys.path.remove(jtalk_dir)
sys.path.insert(0, jtalk_dir)
import jtalkDir  # type: ignore
import translator1  # type: ignore
import translator2  # type: ignore
import mecab as mecab_module  # type: ignore
import subprocess
import tempfile
import shutil
import csv

dic_dir = os.path.join(jtalk_dir, "dic")
user_dics = jtalkDir.user_dics


def __write(file, s=""):
    file.write(s)


def __writeln(file, s=""):
    file.write(s + "\n")


output = None


def __print(s=""):
    global output
    output.write(s + "\n")


def _find_mecab_dict_index(debug_file=None):
    """Find mecab-dict-index.exe from build output or jtusrdic directory.

    Args:
        debug_file: Optional file object to write debug information to.

    Returns:
        Path to mecab-dict-index.exe if found, None otherwise.
    """
    def debug_write(msg):
        # instrumentation cleanup: avoid noisy output in normal runs
        if debug_file:
            debug_file.write(msg + "\n")

    # Find it in the build output (from jtalkSync)
    # miscDepsJp/include/python-jtalk/libopenjtalk/mecab/src/mecab-dict-index.exe
    mecab_src_dir = os.path.join(repo_root, "miscDepsJp", "include", "python-jtalk", "libopenjtalk", "mecab", "src")
    mecab_dict_index_bin = os.path.join(mecab_src_dir, "mecab-dict-index.exe")
    # instrumentation cleanup: do not log search paths by default
    if os.path.exists(mecab_dict_index_bin):
        return mecab_dict_index_bin

    # If not found, return None (caller should handle the error)
    return None


def _build_user_dic_from_csv(csv_path, dic_path, debug_file=None):
    """Build user dictionary from CSV file using mecab-dict-index.exe.

    Args:
        csv_path: Path to CSV file.
        dic_path: Path to output dictionary file.
        debug_file: Optional file object to write debug information to.
    """
    mecab_dict_index = _find_mecab_dict_index(debug_file=debug_file)
    if not mecab_dict_index:
        raise RuntimeError(
            "mecab-dict-index.exe not found. "
            "Please run 'scons jtalkSync' to build it, or ensure it exists in "
            "miscDepsJp/include/python-jtalk/libopenjtalk/mecab/src/"
        )

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"User dictionary CSV file not found: {csv_path}")

    # Ensure output directory exists
    dic_dir_path = os.path.dirname(dic_path)
    if dic_dir_path and not os.path.exists(dic_dir_path):
        os.makedirs(dic_dir_path, exist_ok=True)

    # Build user dictionary in a temporary dicdir (stable on Windows/CRLF + dicrc parsing differences).
    #
    # Rationale:
    # - This repo's dic assets are UTF-8 and often CRLF on Windows.
    # - Some mecab-dict-index builds treat trailing '\r' as part of tokens (pos-id.def parsing),
    #   causing "not a number" and "format error".
    # - In this branch, MeCab's Param::load is OpenJTalk-patched and does not parse dicrc, so
    #   required params like "model" may be missing unless we pass them via CLI.
    #
    # Strategy:
    # - Create temp dicdir
    # - Copy required dictionary assets from the real dic_dir, normalizing line endings to LF for *.def/*.csv
    # - Convert jtusr.csv (OpenJTalk style) to MeCab 5-column userdic CSV
    # - Call mecab-dict-index with -d <temp_dicdir> and -m <temp_dicdir>/model.bin
    temp_dic_dir = tempfile.mkdtemp()
    converted_csv = os.path.join(temp_dic_dir, "jtusr_userdic.csv")
    model_bin = os.path.join(temp_dic_dir, "model.bin")

    def _copy_text_lf(src: str, dst: str) -> None:
        with open(src, "rb") as rf:
            data = rf.read()
        # Normalize CRLF/CR -> LF
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "wb") as f:
            f.write(data)

    # Copy dictionary assets into temp dicdir.
    # Keep list explicit to avoid huge copies, but include the usual MeCab/IPADIC assets.
    assets_text = [
        "dicrc",
        "pos-id.def",
        "rewrite.def",
        "feature.def",
        "char.def",
        "unk.def",
        "left-id.def",
        "right-id.def",
        "matrix.def",
        "model.def",
    ]
    assets_bin = [
        "matrix.bin",
        "char.bin",
        "sys.dic",
        "unk.dic",
        "model.bin",
    ]

    for name in assets_text:
        src = os.path.join(dic_dir, name)
        if os.path.exists(src):
            _copy_text_lf(src, os.path.join(temp_dic_dir, name))

    for name in assets_bin:
        src = os.path.join(dic_dir, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(temp_dic_dir, name))

    # Convert jtusr.csv (OpenJTalk-style) -> MeCab userdic CSV (5 columns):
    # surface,left_id,right_id,cost,feature
    with open(csv_path, "r", encoding="utf-8", newline="") as fin, open(
        converted_csv, "w", encoding="utf-8", newline=""
    ) as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout, lineterminator="\n")
        for row in reader:
            if not row:
                continue
            surface = row[0]
            # OpenJTalk-style: surface + 4 empty columns + feature columns...
            if len(row) >= 6 and all((c == "" for c in row[1:5])):
                feature = ",".join(row[5:])
            # Already 5-col format
            elif len(row) == 5:
                feature = row[4]
            else:
                # Best-effort fallback
                feature = ",".join(row[4:]) if len(row) > 4 else ""
            writer.writerow([surface, "0", "0", "0", feature])

    # instrumentation cleanup: no verbose logging here

    # Run mecab-dict-index.exe
    # mecab-dict-index.exe -d <dic_dir> -m <model> -u <user_dic> -f utf-8 -t utf-8 <csv_file>
    cmd = [
        mecab_dict_index,
        "-d", temp_dic_dir,
        "-m", model_bin,
        "-u", dic_path,
        "-f", "utf-8",
        "-t", "utf-8",
        converted_csv,
    ]

    try:
        # Use cp932 encoding for Windows console output (mecab-dict-index.exe may output in CP932)
        result = subprocess.run(cmd, capture_output=True, text=True, encoding='cp932', errors='replace', check=True)
        return dic_path
    except subprocess.CalledProcessError as e:
        error_msg = f"Failed to build user dictionary: {e}\n"
        if e.stdout:
            error_msg += f"stdout: {e.stdout}\n"
        if e.stderr:
            # Filter out known harmless error messages
            filtered_stderr = "\n".join([
                line for line in e.stderr.split('\n')
                if 'context_id.cpp' not in line or ('cannot find LEFT-ID' not in line and 'cannot find RIGHT-ID' not in line)
            ])
            if filtered_stderr:
                error_msg += f"stderr (filtered): {filtered_stderr}\n"
        raise RuntimeError(error_msg)
    finally:
        try:
            shutil.rmtree(temp_dic_dir, ignore_errors=True)
        except Exception:
            pass


def _get_test_user_dics(debug_file=None):
    """Get user dictionaries for testing, building from jtusr.csv if available.

    Args:
        debug_file: Optional file object to write debug information to.

    Returns:
        List of user dictionary file paths.
    """
    # First, try to build from jtusr.csv
    jtusr_csv = os.path.join(script_dir, "jtusr.csv")
    test_user_dics = []

    def debug_write(msg):
        # instrumentation cleanup: only emit when debug_file is explicitly given
        if debug_file:
            debug_file.write(msg + "\n")

    if os.path.exists(jtusr_csv):
        # Use temporary directory for test user dictionary
        temp_dir = tempfile.mkdtemp()
        jtusr_dic = os.path.join(temp_dir, "jtusr.dic")
        try:
            _build_user_dic_from_csv(jtusr_csv, jtusr_dic, debug_file=debug_file)
            test_user_dics = [jtusr_dic]
        except Exception as e:
            import traceback
            error_details = traceback.format_exc()
            debug_write(f"jpBrailleRunner: Warning: Failed to build user dictionary from {jtusr_csv}: {e}")
            debug_write(f"jpBrailleRunner: Error details: {error_details}")
            # Fall back to existing user_dics if available
            if user_dics:
                test_user_dics = user_dics
    else:
        debug_write(f"jpBrailleRunner: jtusr.csv not found at {jtusr_csv}")
        # Fall back to existing user_dics if jtusr.csv doesn't exist
        if user_dics:
            test_user_dics = user_dics

    return test_user_dics


def dot_numbers(s):
    ret = []
    for c in s:
        code = ord(c)
        if code == 0x20 or code == 0x2800:
            ret.append("0")
        elif 0x2801 <= code and code <= 0x28FF:
            ar = []
            if code & 0x01:
                ar.append("1")
            if code & 0x02:
                ar.append("2")
            if code & 0x04:
                ar.append("3")
            if code & 0x08:
                ar.append("4")
            if code & 0x10:
                ar.append("5")
            if code & 0x20:
                ar.append("6")
            if code & 0x40:
                ar.append("7")
            if code & 0x80:
                ar.append("8")
            ret.append("".join(ar))
    return " ".join(ret)


def pass1():
    global output
    outfile = "__h1output.txt"
    with open_file(outfile, "w") as f:
        count = 0
        for t in tests:
            nabcc = False
            if t.get("mode") == "NABCC":
                nabcc = True
            if "output" in t:
                result, inpos1 = translator1.translateWithInPos(t["input"], nabcc=nabcc)
                if "inpos1" in t:
                    correct_inpos1 = ",".join(["%d" % n for n in t["inpos1"]])
                else:
                    correct_inpos1 = None
                result_inpos1 = ",".join(["%d" % n for n in inpos1])
                if (
                    result != t["output"]
                    or (correct_inpos1 and result_inpos1 != correct_inpos1)
                    or (len(result) != len(inpos1))
                ):
                    count += 1
                    f.write("input: " + t["input"].encode("utf-8") + "\n")
                    f.write("result: " + result.encode("utf-8") + "\n")
                    f.write("correct: " + t["output"].encode("utf-8") + "\n")
                    if correct_inpos1:
                        f.write("correct_inpos1: " + correct_inpos1 + "\n")
                    f.write("result_inpos1: " + result_inpos1 + "\n")
                    if "comment" in t:
                        f.write("comment: " + t["comment"].encode("utf-8") + "\n")
                    f.write("\n")
        print("h1: %d error(s). see %s" % (count, outfile))
    return (count, outfile)


def pass2(verboseMode=False):
    global output
    outfile = "__h2output.txt"

    with open_file(outfile, "w") as f:
        libmecab_path = os.path.join(jtalk_dir, "libmecab.dll")

        # Get test user dictionaries (build from jtusr.csv if available)
        test_user_dics = _get_test_user_dics(debug_file=None)

        dll_dir_handle = None
        if hasattr(os, "add_dll_directory"):
            try:
                dll_dir_handle = os.add_dll_directory(jtalk_dir)
            except OSError as e:
                f.write(f"WARNING: add_dll_directory failed for {jtalk_dir}: {e}\n")

        output = io.StringIO()
        # jtalk_dir points to miscDepsJp/source/synthDrivers/jtalk/ where libmecab.dll is located
        try:
            translator2.initialize(__print, jtalk_dir, dic_dir, test_user_dics)
        except OSError as e:
            log = output.getvalue()
            output.close()
            f.write(log)
            f.write("\n")
            f.write(f"ERROR: Failed to load MeCab DLL: {e}\n")
            f.write(f"Expected libmecab.dll at: {libmecab_path}\n")
            raise RuntimeError(f"MeCab DLL load failed: {e}") from e
        finally:
            if dll_dir_handle is not None:
                dll_dir_handle.close()

        log = output.getvalue()
        output.close()
        f.write(log)
        f.write("\n")
        # Verify MeCab initialization
        if mecab_module.libmc is None or mecab_module.mecab is None:
            msg = "MeCab initialization failed: libmc=%s, mecab=%s" % (
                mecab_module.libmc,
                mecab_module.mecab,
            )
            f.write(msg + "\n")
            f.write("This will cause access violations. Aborting.\n")
            raise RuntimeError(msg)
        count = 0
        for t in tests:
            if "input" not in t:
                continue
            nabcc = False
            if t.get("mode") == "NABCC":
                nabcc = True
            if "text" in t:
                output = io.StringIO()
                result, pat, inpos1, inpos2 = translator2.translateWithInPos2(
                    t["text"], logwrite=__print, nabcc=nabcc
                )
                log = output.getvalue()
                output.close()
                # inpos2
                if "inpos2" in t:
                    correct_inpos2 = ",".join(["%d" % n for n in t["inpos2"]])
                else:
                    correct_inpos2 = None
                # inpos1
                if "inpos1" in t:
                    correct_inpos1 = ",".join(["%d" % n for n in t["inpos1"]])
                else:
                    correct_inpos1 = None
                # merged inpos
                inpos, outpos_ = translator2.mergePositionMap(
                    inpos1, inpos2, len(pat), len(t["text"])
                )
                # outpos
                outpos = translator2.makeOutPos(inpos, len(t["text"]), len(pat))

                if "inpos" in t:
                    correct_inpos = ",".join(["%d" % n for n in t["inpos"]])
                else:
                    correct_inpos = None
                if "outpos" in t:
                    correct_outpos = ",".join(["%d" % n for n in t["outpos"]])
                else:
                    correct_outpos = None
                # result
                result_inpos2 = ",".join(["%d" % n for n in inpos2])
                result_inpos1 = ",".join(["%d" % n for n in inpos1])
                result_inpos = ",".join(["%d" % n for n in inpos])
                result_outpos = ",".join(["%d" % n for n in outpos])
                # output
                isError = False
                if (
                    result != t["input"]
                    or (correct_inpos2 and result_inpos2 != correct_inpos2)
                    or (correct_inpos and result_inpos != correct_inpos)
                    or (correct_outpos and result_outpos != correct_outpos)
                ):
                    isError = True
                    count += 1
                if isError or verboseMode:
                    f.write("text   : " + t["text"] + "\n")
                    f.write("correct: " + t["input"] + "\n")
                    f.write("result : " + result + "\n")
                    f.write("pat    : " + pat + "\n")
                    if correct_inpos2:
                        f.write("cor_in2: " + correct_inpos2 + "\n")
                    if correct_inpos1:
                        f.write("cor_in1: " + correct_inpos1 + "\n")
                    if correct_inpos:
                        f.write("cor_in : " + correct_inpos + "\n")
                    if correct_outpos:
                        f.write("cor_out: " + correct_outpos + "\n")
                    f.write("res_in2: " + result_inpos2 + "\n")
                    f.write("res_in1: " + result_inpos1 + "\n")
                    f.write("res_in : " + result_inpos + "\n")
                    f.write("res_out: " + result_outpos + "\n")
                    if "comment" in t and t["comment"]:
                        f.write("comment: " + t["comment"] + "\n")
                    f.write("\n")
                    f.write(log)
                    f.write("\n")
        print("h2: %d error(s). see %s" % (count, outfile))
    return (count, outfile)


def make_doc():
    outfile = "__jpBrailleHarness.md"
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    with open_file(outfile, "w") as f:
        __writeln(
            f,
            """
# NVDA 日本語版 点訳テストケース """
            + timestamp,
        )
        count = 0
        for t in tests:
            # 'note' はテストケースではなく説明の記述
            if "note" in t:
                note = t["note"]
                # "==== 見出し ====" => "##### 見出し"
                # "=== 見出し ===" => "#### 見出し"
                # "== 見出し ==" => "### 見出し"
                # "+ 見出し +" => "## 見出し"
                if note.startswith("====") and note.endswith("===="):
                    note = "##### " + note[4:-4]
                elif note.startswith("===") and note.endswith("==="):
                    note = "#### " + note[3:-3]
                elif note.startswith("==") and note.endswith("=="):
                    note = "### " + note[2:-2]
                elif note.startswith("+") and note.endswith("+"):
                    note = "## " + note[1:-1]
                __writeln(f)
                __writeln(f, note)
                __writeln(f)
                continue
            count += 1
            __writeln(f, "###### 番号: %d" % count)

            if "text" in t:
                __writeln(f, "- 日本語: " + t["text"].replace("　", "□").replace(" ", "□"))
            if "input" in t:
                __writeln(f, "- カナ表記: " + t["input"].replace(" ", "□"))
            if "output" in t:
                __writeln(f, "- 点字: " + t["output"].replace(" ", "□"))
            if "output" in t:
                __writeln(f, "- ドット番号: " + dot_numbers(t["output"]))
            if "mode" in t:
                __writeln(f, "- モード: " + t["mode"])
            if "comment" in t:
                if type(t["comment"]) == str:
                    __writeln(f, "- コメント: " + t["comment"])
                else:
                    __writeln(f, "- コメント: ")
                    for c in t["comment"]:
                        __writeln(f, "  - " + c)
                    __writeln(f, "  -")
            __writeln(f, "")


if __name__ == "__main__":
    parser = optparse.OptionParser()
    parser.add_option(
        "-1",
        "--pass1only",
        action="store_true",
        dest="pass1_only",
        default="False",
        help="pass1 only timeit",
    )
    parser.add_option(
        "-2",
        "--pass2only",
        action="store_true",
        dest="pass2_only",
        default="False",
        help="pass2 only timeit",
    )
    parser.add_option(
        "-v",
        "--verbose",
        action="store_true",
        dest="verbose",
        default="False",
        help="pass2 with verbose mode",
    )
    parser.add_option(
        "-m",
        "--makedoc",
        action="store_true",
        dest="make_doc",
        default="False",
        help="make t2t document of harness",
    )
    parser.add_option(
        "-n",
        "--number",
        action="store",
        dest="number",
        type="int",
        default=1,
        help="number for timeit",
    )
    (options, args) = parser.parse_args()

    if options.make_doc == True:
        make_doc()
    elif options.pass1_only == True:
        t = timeit.Timer(stmt=pass1)
        print(t.timeit(number=options.number))
    elif options.pass2_only == True:
        t = timeit.Timer(stmt=pass2)
        print(t.timeit(number=options.number))
    elif options.verbose == True:
        pass2(verboseMode=True)
    else:
        pass1()
        pass2()
