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

# Use UTF-8 dictionary files from include/libopenjtalk/mecab-naist-jdic (instead of EUC-JP from jptools/jtalk/libopenjtalk/mecab-naist-jdic)
# THISDIR = path.normpath(path.join(JTDIR, "libopenjtalk", "mecab-naist-jdic"))  # Old: EUC-JP files
THISDIR = path.normpath(path.join(JTDIR, "..", "..", "include", "libopenjtalk", "mecab-naist-jdic"))  # New: UTF-8 files (source)
OLD_THISDIR = path.normpath(path.join(JTDIR, "libopenjtalk", "mecab-naist-jdic"))  # For custom dict output and OUTDIR/TEMPDIR paths
OUTDIR = path.normpath(path.join(OLD_THISDIR, "dic"))
TEMPDIR = path.normpath(path.join(OLD_THISDIR, "_temp"))
MECAB_DICT_INDEX = path.normpath(
    path.join(OLD_THISDIR, "..", "mecab", "src", "mecab-dict-index.exe")
)

CODE = "utf-8"  # cp932


def mkdir_p(path):
    os.makedirs(path, exist_ok=True)


mkdir_p(OUTDIR)
mkdir_p(TEMPDIR)

# Use OLD_THISDIR for custom dictionary makers (they write files to THISDIR)
# Custom dictionaries are written to OLD_THISDIR, but tankan_dic_maker reads naist-jdic.csv from THISDIR (UTF-8)
eng_dic_maker.make_dic(ENGDIC, CODE, OLD_THISDIR)
tankan_dic_maker.make_dic(CODE, CS_FILE, OLD_THISDIR, naist_jdic_dir=THISDIR)  # Read from THISDIR (UTF-8), write to OLD_THISDIR
custom_dic_maker.make_dic(CODE, OLD_THISDIR)


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

# Copy files from OLD_THISDIR (custom dictionaries are generated there)
# Note: tankan_dic_maker writes to THISDIR, but we use OLD_THISDIR for eng_dic_maker and custom_dic_maker
for f in files:
    # Check both OLD_THISDIR and THISDIR (tankan_dic_maker writes to THISDIR)
    src = path.join(OLD_THISDIR, f)
    if not path.exists(src):
        src = path.join(THISDIR, f)
    if path.exists(src):
        print("copy %s to %s" % (src, TEMPDIR))
        shutil.copy(src, TEMPDIR)

# Copy UTF-8 files directly (no conversion needed)
for f in euc_files:
    src = path.join(THISDIR, f)
    dst = path.join(TEMPDIR, f)
    print("copy %s to %s (UTF-8, no conversion)" % (src, dst))
    shutil.copy2(src, dst)

# Convert naist-jdic.csv with filter (still needs filter processing)
convert_file(
    path.join(THISDIR, jdic_file), "utf-8", path.join(TEMPDIR, jdic_file), CODE, apply_filter=True
)

print(TEMPDIR, [MECAB_DICT_INDEX, "-d", ".", "-o", OUTDIR, "-f", CODE, "-c", CODE])
subprocess.check_call(
    [MECAB_DICT_INDEX, "-d", ".", "-o", OUTDIR, "-f", CODE, "-c", CODE], cwd=TEMPDIR
)

# Copy euc_files (UTF-8) from TEMPDIR to OUTDIR
for f in euc_files:
    src = path.join(TEMPDIR, f)
    dst = path.join(OUTDIR, f)
    if path.exists(src):
        print("copy %s to %s" % (src, dst))
        shutil.copy2(src, dst)

# Copy dicrc to OUTDIR, updating config-charset to UTF-8
dicrc_src = path.join(TEMPDIR, "dicrc")
dicrc_dst = path.join(OUTDIR, "dicrc")
if path.exists(dicrc_src):
    # Read dicrc from TEMPDIR and update config-charset to UTF-8
    with open_file(dicrc_src, "r", "utf-8") as f:
        content = f.read()
    # Replace config-charset = EUC-JP with config-charset = UTF-8
    content = content.replace("config-charset = EUC-JP", "config-charset = UTF-8")
    with open_file(dicrc_dst, "w", "utf-8") as f:
        f.write(content)
    print("copy %s to %s (config-charset updated to UTF-8)" % (dicrc_src, dicrc_dst))
else:
    # Fallback: copy from THISDIR and update config-charset
    dicrc_orig = path.join(THISDIR, "dicrc")
    if path.exists(dicrc_orig):
        with open_file(dicrc_orig, "r", "utf-8") as f:
            content = f.read()
        content = content.replace("config-charset = EUC-JP", "config-charset = UTF-8")
        with open_file(dicrc_dst, "w", "utf-8") as f:
            f.write(content)
        print("copy %s to %s (config-charset updated to UTF-8)" % (dicrc_orig, dicrc_dst))

dic_version_file = path.join(OUTDIR, "DIC_VERSION")
print("dic version file: " + dic_version_file)
version = f"nvdajp-jtalk-dic ({CODE}) {datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
print(version)
with open_file(dic_version_file, "w", "utf-8") as f:
    f.write(version + os.linesep)

# end of file
