# coding: utf-8
# make_jdic.py
# Copyright (C) 2010-2013 Takuya Nishimoto (NVDA Japanese Team)


open_file = lambda name, mode, encoding: open(name, mode, encoding=encoding)


import errno
import os
import shutil
import subprocess
from datetime import datetime, timezone
from os import path

import custom_dic_maker
import eng_dic_maker
import tankan_dic_maker
from filter_jdic import filter_jdic

# MECAB_DICT_INDEX と OUTDIR は libopenjtalk/mecab-naist-jdic/_temp が基準
JTDIR = path.dirname(path.abspath(__file__))
ENGDIC = path.normpath(path.join(JTDIR, "bep-eng.dic"))
CS_FILE = path.normpath(path.join(JTDIR, "characters-ja.dic"))

# THISDIR = path.normpath(path.join(JTDIR, "..", "python-jtalk", "libopenjtalk", "mecab-naist-jdic"))
THISDIR = path.normpath(path.join(JTDIR, "libopenjtalk", "mecab-naist-jdic"))
OUTDIR = path.normpath(path.join(THISDIR, "dic"))
TEMPDIR = path.normpath(path.join(THISDIR, "_temp"))
MECAB_DICT_INDEX = path.normpath(
    path.join(THISDIR, "..", "mecab", "src", "mecab-dict-index.exe")
)

CODE = "utf-8"  # cp932


def mkdir_p(path):
    os.makedirs(path, exist_ok=True)


mkdir_p(OUTDIR)
mkdir_p(TEMPDIR)

eng_dic_maker.make_dic(ENGDIC, CODE, THISDIR)
tankan_dic_maker.make_dic(CODE, CS_FILE, THISDIR)
custom_dic_maker.make_dic(CODE, THISDIR)


def convert_file(src_file, src_enc, dest_file, dest_enc, apply_filter=False):
    print("converting %s to %s" % (src_file, dest_file))
    with open_file(src_file, "r", src_enc) as sf:
        with open_file(dest_file, "w", dest_enc) as df:
            while 1:
                s = sf.readline()
                if not s:
                    break
                if apply_filter:
                    s = s.rstrip()
                    s = filter_jdic(s)
                    if s:
                        s += "\n"  # do not use os.linesep here
                df.write(s)


files = [
    "dicrc",
    "nvdajp-eng-dic.csv",
    "nvdajp-tankan-dic.csv",
    "nvdajp-custom-dic.csv",
]

euc_files = [
    "char.def",
    "feature.def",
    "left-id.def",
    "matrix.def",
    "pos-id.def",
    "rewrite.def",
    "right-id.def",
    "unk.def",
]

jdic_file = "naist-jdic.csv"

for f in files:
    print("copy %s to %s" % (path.join(THISDIR, f), TEMPDIR))
    shutil.copy(path.join(THISDIR, f), TEMPDIR)

for f in euc_files:
    convert_file(path.join(THISDIR, f), "euc-jp", path.join(TEMPDIR, f), CODE)

convert_file(
    path.join(THISDIR, jdic_file), "euc-jp", path.join(TEMPDIR, jdic_file), CODE, apply_filter=True
)

cmd = [MECAB_DICT_INDEX, "-d", ".", "-o", OUTDIR, "-f", CODE, "-c", CODE]
print(TEMPDIR, cmd)
# Suppress normal mecab-dict-index chatter but surface output on failure
result = subprocess.run(
    cmd,
    cwd=TEMPDIR,
    capture_output=True,
    text=True,
)
if result.returncode != 0:
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr)
    result.check_returncode()

print("copy %s to %s" % (path.join(THISDIR, "dicrc"), OUTDIR))
shutil.copy(path.join(THISDIR, "dicrc"), OUTDIR)
dic_version_file = path.join(OUTDIR, "DIC_VERSION")
print("dic version file: " + dic_version_file)
version = f"nvdajp-jtalk-dic ({CODE}) {datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
print(version)
with open_file(dic_version_file, "w", "utf-8") as f:
    f.write(version + os.linesep)

# end of file
