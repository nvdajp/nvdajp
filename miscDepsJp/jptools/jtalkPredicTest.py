# jtalkPredicTest.py
# -*- coding: utf-8 -*-

import os
import sys
from pathlib import Path

# Use source/synthDrivers/jtalk directly (files moved from miscDepsJp in Phase 1)
script_dir = Path(__file__).resolve().parent
# script_dir -> miscDepsJp/jptools
# ../.. -> repo root
repo_root = (script_dir / ".." / "..").resolve()
jtalk_dir = repo_root / "source" / "synthDrivers" / "jtalk"
sys.path.insert(0, str(jtalk_dir))
import jtalkPrepare  # type: ignore
from _nvdajp_unicode import unicode_normalize  # type: ignore

tests = [
    ["ー", "チョーオン"],
    ["ン", "ウン"],
    ["あ ー", "あ チョーオン"],
    ["あ ン", "あ ウン"],
    ["0123345", " ゼロ イチ ニー サン サン ヨン ゴー "],
    ["人々", "人人"],
    ["昔々", "昔昔"],
    ["家々", "家家"],
    ["山々", "山山"],
    ["は", "ハ"],
    ["あ は", "あ ハ"],
    ["Ａ", "a"],
    ["59 名", "59名"],
    ["4行", "4ギョー"],
    ["2 分前更新", "2分マエコーシン"],
    ["1MB", "1メガバイト"],
    ["10MB", "10メガバイト"],
    ["1.2MB", "1.2メガバイト"],
    ["0.5MB", "0.5メガバイト"],
    ["321.1MB", "321.1メガバイト"],
    ["123.45MB", "123.45メガバイト"],
    ["2.7GB", "2.7ギガバイト"],
    ["10KB", "10キロバイト"],
    ["1 MB", "1メガバイト"],
    ["10 MB", "10メガバイト"],
    ["1.2 MB", "1.2メガバイト"],
    ["0.5 MB", "0.5メガバイト"],
    ["321.0 MB", "321.0メガバイト"],
    ["123.45 MB", "123.45メガバイト"],
    ["2.7 GB", "2.7ギガバイト"],
    ["10 KB", "10キロバイト"],
    ["12.01 KB", "12.01キロバイト"],
    ["12.01", "12.01"],
    ["12.35", "12.35"],
    ["01234", " ゼロ イチ ニー サン ヨン "],
    ["1.01", "1.01"],
    ["1.10", "1.10"],
    ["２０１１．０３．１１", "2011テン ゼロ サン テン11"],
    ["２０１１．１１．１１", "2011テン11テン11"],
    ["7.0.1", "7テン0テン1"],
    ["7.0.10", "7テン0テン10"],
    ["1.2.3", "1テン2テン3"],
    ["7.01.45", "7テン ゼロ イチ テン45"],
    ["7.1.45", "7テン1テン45"],
    ["7.01.01", "7テン ゼロ イチ テン ゼロ イチ "],
    ["7.1.01", "7テン1テン ゼロ イチ "],
    ["0.0.0.1", "0テン0テン0テン1"],
    ["１，２３４円", "1234円"],
    ["0,1", "0カンマ1"],
    ["134,554", "134554"],
    ["2013年2月10日", "2013年2月10日"],
    ["2013‎年‎2‎月‎10‎日", "2013年2月10日"],  # remove U+200E LEFT-TO-RIGHT MARK
    ["2013‎年‎2‎月‎10‎日、‏‎23:45:19", "2013年2月10日、23:45:19"],  # remove U+200E U+200F
    ["築3年", "築3年"],
    ["SC3301", "sc3301"],
    ["SC4401", "sc4401"],
    ["SC330100", "sc330100"],
]


def _print(s):
    print(s)


def runTasks():
    jtalkPrepare.setup()
    count = 0
    for item in tests:
        msg = item[0]
        normalized = unicode_normalize(msg)
        s = jtalkPrepare.convert(normalized)
        if item[1] != s:
            _print(
                "input:%s normalized:%s result:%s expected:%s"
                % (msg, normalized, s, item[1])
            )
            count += 1
    return count


if __name__ == "__main__":
    runTasks()
