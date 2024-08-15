# coding: UTF-8
# _checkCharDesc.py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012,2023 Takuya Nishimoto, NVDA Japanese Team, Shuaruta Inc.

import re
import codecs

from getord import getOrd

LOCALE_JA = r"..\source\locale\ja"
SY_FILE = LOCALE_JA + r"\symbols.dic"
CH_FILE = LOCALE_JA + r"\characterDescriptions.dic"
CS_FILE = LOCALE_JA + r"\characters.dic"


def read_symbol_file(sy_file, returnSource=False, raiseDuplicated=True):
    src = []
    with codecs.open(sy_file, encoding="utf-8") as sy:
        mode = None
        ar = {}
        c = 0
        for line in sy:
            c += 1
            line = line.rstrip()
            if line == "complexSymbols:":
                mode = 1
                src.append(line)
                continue
            if line == "symbols:":
                mode = 2
                src.append(line)
                continue
            if len(line) == 0:
                src.append(line)
                continue
            if line[0] == "#":
                src.append(line)
                continue
            if mode == 2:
                a = line.split("\t")
                if len(a) >= 2 and (len(a[0]) == 1 or a[0][0] == "\\"):
                    if a[0] in ar:
                        print(
                            "duplicated %04x %s (line %d and %d)"
                            % (ord(a[0]), a[0], ar[a[0]][0], c)
                        )
                        if raiseDuplicated:
                            raise Exception
                    key = a[0]
                    if key[0] == "\\":
                        key = key.encode('unicode_escape').decode('utf-8')[0]
                    s = "U+%04x" % ord(key)
                    ar[key] = [c, a[1].strip()]
                    # add comment field
                    if a[-1][0] == "#":
                        # delete existing 'U+xxxx' string
                        a[-1] = re.sub(r" U\+[0-9a-f]{4}", "", a[-1])
                        a[-1] += " " + s
                    else:
                        a.append("# %s %s" % (key, s))
                    line = "\t".join(a)
            src.append(line)
    if returnSource:
        return ar, src
    return ar


def read_chardesc_file(ch_file):
    with codecs.open(ch_file, encoding="utf-8") as ch:
        ar = {}
        c = 0
        for line in ch:
            c += 1
            line = line.rstrip()
            if len(line) == 0:
                continue
            if line[0] == "#":
                continue
            if line[0:2] == "\\#":
                line = "#" + line[2:]
            a = line.split("\t")
            if len(a) >= 2:
                ar[a[0]] = [c, a[1]]
    return ar


def read_characters_file(cs_file, use_both=False):
    count = 0
    with codecs.open(cs_file, encoding="utf-8") as ch:
        ar = {}
        c = 0
        for line in ch:
            c += 1
            line = line.rstrip()
            if len(line) == 0:
                continue
            if line[0] == "#":
                continue
            if line[0:2] == "\\#":
                line = "#" + line[2:]
            a = line.split("\t")
            if len(a) >= 4:
                if use_both:
                    ar[a[0]] = [
                        c,
                        a[2].replace("[", "").replace("]", "") + " * " + a[3],
                    ]
                else:
                    ar[a[0]] = [c, a[3]]
                count += 1
    return ar


def print_diff(sy, ch):
    for k, v in ch.items():
        if k in sy:
            if v[1] == sy[k][1]:
                continue
            print("ch %d %s %s / sy %d %s" % (v[0], k, v[1], sy[k][0], sy[k][1]))


C = re.compile("\\s+")


def equals_ignore_spaces(s1, s2):
    s1 = C.sub("", s1)
    s2 = C.sub("", s2)
    if s1 == s2:
        return True
    return False


def print_different(sy, ch, skip_included=False, report_included=False):
    ar = {}
    for k, v in ch.items():
        if k in sy:
            s1 = v[1]
            s2 = sy[k][1]
            if equals_ignore_spaces(s1, s2):
                continue
            if skip_included:
                # 片方がもう一方に含まれる場合はスキップ
                if (s1 in s2) or (s2 in s1):
                    if report_included:
                        print("included %04x ch %s / sy %s" % (ord(k), s1, s2))
                    continue
                # 'セン' を取り除いて、片方がもう一方に含まれる場合はスキップ
                s1_ = s1.replace("セン", "")
                s2_ = s2.replace("セン", "")
                if (s1_ in s2_) or (s2_ in s1_):
                    if report_included:
                        print("included %04x ch %s / sy %s" % (ord(k), s1, s2))
                    continue
                # 'ノ ナカニ' を取り除いて、片方がもう一方に含まれる場合はスキップ
                s1_ = s1.replace("ノ ナカニ", "")
                s2_ = s2.replace("ノ ナカニ", "")
                if (s1_ in s2_) or (s2_ in s1_):
                    if report_included:
                        print("included %04x ch %s / sy %s" % (ord(k), s1, s2))
                    continue
                # 'スーガク' を取り除いて、片方がもう一方に含まれる場合はスキップ
                s1_ = s1.replace(" ", "")
                s2_ = s2.replace(" ", "")
                if (s1_ in s2_) or (s2_ in s1_):
                    if report_included:
                        print("included %04x ch %s / sy %s" % (ord(k), s1, s2))
                    continue
            output = "%04x sy %d %s / ch %d %s %s" % (
                ord(k),
                sy[k][0],
                sy[k][1],
                v[0],
                k,
                v[1],
            )
            ar[sy[k][0]] = output
    for s in sorted(ar.items(), key=lambda x: int(x[0])):
        print(s[1])


def find_desc_duplicate(ch, skipKeisen=True, skipEmoji=True):
    for k, v in ch.items():
        for k2, v2 in ch.items():
            if skipKeisen and ("ケイセン" in v[1] or "ケイセン" in v2[1]):
                continue
            if skipEmoji and ("エモジ" in v[1] or "エモジ" in v2[1]):
                continue
            assert isinstance(v[0], int) or isinstance(v[0], str)
            assert isinstance(v2[0], int) or isinstance(v2[0], str)
            if (
                isinstance(v[0], int)
                and isinstance(v2[0], int)
                and v[0] < v2[0]
                and k != k2
                and equals_ignore_spaces(v[1], v2[1])
            ):
                print(
                    "ch %d:%s %04x / %d:%s %04x / %s"
                    % (v[0], k, getOrd(k), v2[0], k2, getOrd(k2), v2[1])
                )


def isZenkakuKatakana(c):
    return re.search(r"[ァ-ヾ]", c) is not None


def isHankakuKatakana(c):
    return re.search(r"[ｦ-ﾝ]", c) is not None


def isHalfShape(c):
    c = c[0:1]
    return (32 < ord(c)) and (ord(c) < 128)


def add_katakana_prefix_to_characters(ch):
    ar = {}
    for k, v in ch.items():
        if isZenkakuKatakana(k):
            v = "カタカナ " + str(v)
        elif isHankakuKatakana(k):
            v = "ハンカクカタカナ " + str(v)
        elif k.isupper():
            v = "オオモジ " + str(v)
        elif isHalfShape(k):
            v = "ハンカク " + str(v)
        ar[k] = v
    return ar
