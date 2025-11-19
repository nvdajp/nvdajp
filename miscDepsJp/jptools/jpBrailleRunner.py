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

jtalk_dir = os.path.normpath(
    os.path.join(getcwd(), "..", "source", "synthDrivers", "jtalk")
)
sys.path.append(jtalk_dir)
# Also add source/synthDrivers/jtalk where mecab.py is copied by scons miscdepsjp
source_jtalk_dir = os.path.normpath(
    os.path.join(getcwd(), "..", "..", "source", "synthDrivers", "jtalk")
)
if os.path.isdir(source_jtalk_dir):
    sys.path.insert(0, source_jtalk_dir)  # Insert at beginning to prioritize
import jtalkDir  # type: ignore
import translator1  # type: ignore
import translator2  # type: ignore
import mecab as mecab_module  # type: ignore

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
        output = io.StringIO()
        translator2.initialize(__print, jtalk_dir, dic_dir, user_dics)
        log = output.getvalue()
        output.close()
        f.write(log)
        f.write("\n")
        # Verify MeCab initialization
        if mecab_module.libmc is None or mecab_module.mecab is None:
            f.write("ERROR: MeCab initialization failed: libmc=%s, mecab=%s\n" % (mecab_module.libmc, mecab_module.mecab))
            f.write("This will cause access violations. Aborting.\n")
            return (1, outfile)
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
                            comment = t["comment"]
                            if isinstance(comment, (list, tuple)):
                                comment = " ".join(str(c) for c in comment)
                            else:
                                comment = str(comment)
                            f.write("comment: " + comment + "\n")
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
