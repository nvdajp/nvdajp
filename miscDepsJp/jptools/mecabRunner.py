# mecabRunner.py
# -*- coding: utf-8 -*-
# Japanese text processor test module
# by Takuya Nishimoto

import os
import sys
import subprocess
import tempfile
import shutil
import csv
from os import getcwd

from mecabHarness import tasks

# Use source/synthDrivers/jtalk directly (files moved from miscDepsJp in Phase 1)
script_dir = os.path.dirname(os.path.abspath(__file__))
# script_dir -> miscDepsJp/jptools
# ../.. -> repo root
repo_root = os.path.abspath(os.path.join(script_dir, "..", ".."))
jt_dir = os.path.join(repo_root, "source", "synthDrivers", "jtalk")
sys.path.insert(0, jt_dir)
import jtalkDir  # type: ignore
from _nvdajp_unicode import unicode_normalize  # type: ignore
from mecab import *  # type: ignore

dic = os.path.join(jt_dir, "dic")
user_dics_org = jtalkDir.user_dics_org
user_dics = jtalkDir.user_dics


def __print(s):
    print(s)


_buffer = ""


def clear_morph_buffer():
    global _buffer
    _buffer = ""


def print_morph_buffer():
    __print(_buffer)


def __print_dummy(s):
    global _buffer
    _buffer += s + "\n"


def Mecab_get_reading(mf, CODE_=CODE):  # type: ignore
    reading = ""
    braille = ""
    for pos in range(0, mf.size):
        ar = Mecab_getFeature(mf, pos, CODE_=CODE_).split(",")
        rd = ""
        if len(ar) > 9:
            rd = ar[9].replace("\u3000", " ")
        elif ar[0] != "ー":
            rd = unicode_normalize(ar[0])
        reading += rd
        if len(ar) > 12:
            braille += ar[12] + r"/"
        else:
            braille += rd + r"/"
    return (reading, braille.rstrip(r" /"))


def get_reading(msg):
    s = text2mecab(msg)
    mf = MecabFeatures()
    Mecab_analysis(s, mf)
    Mecab_print(mf, logwrite_=__print_dummy)
    Mecab_correctFeatures(mf)
    Mecab_print(mf, logwrite_=__print_dummy)
    Mecab_print(mf)
    reading = Mecab_get_reading(mf)
    mf = None
    return reading


def _find_mecab_dict_index():
    """Find mecab-dict-index.exe from build output (from jtalkSync).

    The executable is built by scons jtalkSync and located at:
    miscDepsJp/include/python-jtalk/libopenjtalk/mecab/src/mecab-dict-index.exe
    """
    # Find it in the build output (from jtalkSync)
    # miscDepsJp/include/python-jtalk/libopenjtalk/mecab/src/mecab-dict-index.exe
    mecab_src_dir = os.path.join(repo_root, "miscDepsJp", "include", "python-jtalk", "libopenjtalk", "mecab", "src")
    mecab_dict_index_bin = os.path.join(mecab_src_dir, "mecab-dict-index.exe")
    if os.path.exists(mecab_dict_index_bin):
        return mecab_dict_index_bin

    # If not found, return None (caller should handle the error)
    return None


def _filter_mecab_stderr(stderr_text):
    """Filter out known harmless error messages from mecab-dict-index.exe.

    These errors are expected and do not indicate a failure:
    - context_id.cpp LEFT-ID/RIGHT-ID errors (known issue with some dictionary entries)
    - These are suppressed by Open JTalk's patched CHECK_DIE macro
    """
    if not stderr_text:
        return ""

    lines = stderr_text.split('\n')
    filtered_lines = []
    for line in lines:
        # Filter out context_id.cpp LEFT-ID/RIGHT-ID errors
        # These are expected warnings that don't prevent successful dictionary compilation
        if 'context_id.cpp' in line and ('cannot find LEFT-ID' in line or 'cannot find RIGHT-ID' in line):
            continue
        filtered_lines.append(line)

    return '\n'.join(filtered_lines)


def _build_user_dic_from_csv(csv_path, dic_path):
    """Build user dictionary from CSV file using mecab-dict-index.exe."""
    mecab_dict_index = _find_mecab_dict_index()
    if not mecab_dict_index:
        raise RuntimeError(
            "mecab-dict-index.exe not found. "
            "Please run 'scons jtalkSync' to build it, or ensure it exists in "
            "miscDepsJp/include/python-jtalk/libopenjtalk/mecab/src/"
        )

    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"User dictionary CSV file not found: {csv_path}")

    # Ensure output directory exists
    dic_dir = os.path.dirname(dic_path)
    if dic_dir and not os.path.exists(dic_dir):
        os.makedirs(dic_dir, exist_ok=True)

    # Build user dictionary in a temporary dicdir (stable on Windows/CRLF + dicrc parsing differences).
    temp_dic_dir = tempfile.mkdtemp()
    converted_csv = os.path.join(temp_dic_dir, "jtusr_userdic.csv")
    model_bin = os.path.join(temp_dic_dir, "model.bin")

    def _copy_text_lf(src: str, dst: str) -> None:
        with open(src, "rb") as rf:
            data = rf.read()
        data = data.replace(b"\r\n", b"\n").replace(b"\r", b"\n")
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(dst, "wb") as f:
            f.write(data)

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
        src = os.path.join(dic, name)
        if os.path.exists(src):
            _copy_text_lf(src, os.path.join(temp_dic_dir, name))
    for name in assets_bin:
        src = os.path.join(dic, name)
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(temp_dic_dir, name))

    with open(csv_path, "r", encoding="utf-8", newline="") as fin, open(
        converted_csv, "w", encoding="utf-8", newline=""
    ) as fout:
        reader = csv.reader(fin)
        writer = csv.writer(fout, lineterminator="\n")
        for row in reader:
            if not row:
                continue
            surface = row[0]
            if len(row) >= 6 and all((c == "" for c in row[1:5])):
                feature = ",".join(row[5:])
            elif len(row) == 5:
                feature = row[4]
            else:
                feature = ",".join(row[4:]) if len(row) > 4 else ""
            writer.writerow([surface, "0", "0", "0", feature])

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
        # Filter out known harmless error messages
        filtered_stderr = _filter_mecab_stderr(result.stderr)
        if filtered_stderr:
            # Only print filtered stderr if there are other messages
            __print(f"mecab-dict-index stderr (filtered): {filtered_stderr}")
        __print(f"User dictionary built successfully: {dic_path}")
        return dic_path
    except subprocess.CalledProcessError as e:
        # Filter stderr before reporting errors
        filtered_stderr = _filter_mecab_stderr(e.stderr) if e.stderr else ""
        error_msg = f"Failed to build user dictionary: {e}\n"
        if e.stdout:
            error_msg += f"stdout: {e.stdout}\n"
        if filtered_stderr:
            error_msg += f"stderr (filtered): {filtered_stderr}\n"
        # Check if the error is only the known harmless warnings
        if not filtered_stderr and e.returncode != 0:
            # If stderr was completely filtered but return code is non-zero,
            # there might be a real error, so include original stderr
            if e.stderr:
                error_msg += f"stderr (original): {e.stderr}\n"
        raise RuntimeError(error_msg)
    finally:
        try:
            shutil.rmtree(temp_dic_dir, ignore_errors=True)
        except Exception:
            pass


def runTasks(enableUserDic=False):
    temp_dir = None
    if enableUserDic:
        # Build user dictionary from jtusr.csv if needed
        jtusr_csv = os.path.join(script_dir, "jtusr.csv")
        test_user_dics = []

        if os.path.exists(jtusr_csv):
            # Use temporary directory for test user dictionary
            temp_dir = tempfile.mkdtemp()
            jtusr_dic = os.path.join(temp_dir, "jtusr.dic")
            try:
                _build_user_dic_from_csv(jtusr_csv, jtusr_dic)
                test_user_dics = [jtusr_dic]
                __print(f"Using test user dictionary: {jtusr_dic}")
            except Exception as e:
                __print(f"Warning: Failed to build user dictionary from {jtusr_csv}: {e}")
                # Fall back to existing user_dics if available
                if user_dics:
                    test_user_dics = user_dics
        else:
            # Fall back to existing user_dics if jtusr.csv doesn't exist
            if user_dics:
                test_user_dics = user_dics

        if test_user_dics:
            print(jt_dir, dic, test_user_dics)
            Mecab_initialize(__print, jt_dir, dic, test_user_dics)
        else:
            print(jt_dir, dic, "(no user dictionary)")
            Mecab_initialize(__print, jt_dir, dic)
    else:
        print(jt_dir, dic)
        Mecab_initialize(__print, jt_dir, dic)
    count = 0
    for i in tasks:
        if isinstance(i, dict):
            if "braille" in i:
                if "speech" in i:
                    item = [i["text"], i["speech"], i["braille"]]
                else:
                    s = i["braille"].replace(" ", "").replace("/", "")
                    item = [i["text"], s, i["braille"]]
            elif "input" in i:
                if "speech" in i:
                    item = [i["text"], i["speech"], i["input"]]
                else:
                    s = i["input"].replace(" ", "").replace("/", "")
                    item = [i["text"], s, i["input"]]
            elif "text" in i and "speech" in i:
                item = [i["text"], i["speech"]]
            else:
                continue
        else:
            item = i
        clear_morph_buffer()
        result = get_reading(item[0])
        if item[1] is not None and item[1] and result[0] != item[1]:
            __print("input:    " + item[0])
            __print("reading expected: " + item[1])
            __print("reading result:   " + result[0])
            print_morph_buffer()
            count += 1
        if len(item) > 2 and item[2] and result[1] != item[2]:
            __print("input:            " + item[0])
            __print("braille expected: " + item[2])
            __print("braille result:   " + result[1])
            print_morph_buffer()
            count += 1

    # Clean up temporary directory if created
    if temp_dir and os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir)
        except Exception as e:
            __print(f"Warning: Failed to clean up temporary directory {temp_dir}: {e}")

    return count


if __name__ == "__main__":
    runTasks(enableUserDic=True)
