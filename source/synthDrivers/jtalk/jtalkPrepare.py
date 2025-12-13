# nvdajp_predic.py
# -*- coding: utf-8 -*-
# for python-jtalk

import re
import sys


re_ascii = re.ASCII


predic = None


def setup():
    global predic
    if predic is None:
        predic = load()


def convert(msg):
    setup()
    for p in predic:
        try:
            msg = re.sub(p[0], p[1], msg)
        except:
            pass
    msg = msg.lower()
    return msg


def load():
    return [
        [re.compile("^ー$"), "チョーオン"],
        [re.compile("^ン$"), "ウン"],
        [re.compile("\\sー$"), " チョーオン"],
        [re.compile("\\sン$"), " ウン"],
        ## 人々 昔々 家々 山々
        [re.compile("(.)々"), "\\1\\1"],
        ## isolated hiragana HA (mecab replaces to WA)
        ## は
        [re.compile("^は$"), "ハ"],
        [re.compile("\\sは$"), " ハ"],
        ## 59 名
        [re.compile("(\\d) 名"), "\\1名"],
        ## 4行 ヨンコー -> ヨンギョー
        [re.compile("(\\d)行"), "\\1ギョー"],
        ## 2 分前更新
        [re.compile("(\\d)+ 分前更新"), "\\1分マエコーシン"],
        ## 1MB 10MB 1.2MB 0.5MB 321.0MB 123.45MB 2.7GB
        ## 1 MB 10 MB 1.2 MB 0.5 MB 321.0 MB 123.45 MB 2.7 GB
        [re.compile("(\\d+)\\s*KB"), "\\1キロバイト"],
        [re.compile("(\\d+)\\s*MB"), "\\1メガバイト"],
        [re.compile("(\\d+)\\s*GB"), "\\1ギガバイト"],
        [re.compile("(\\d+)\\s*MHz"), "\\1メガヘルツ"],
        [re.compile("(\\d+)\\s*GHz"), "\\1ギガヘルツ"],
        ## 2013 年 1 月 2 日
        [re.compile("(\\d+)\\s+年\\s+(\\d+)\\s+月\\s+(\\d+)\\s+日"), "\\1年\\2月\\3日"],
        ### zenkaku symbols convert
        ## ２０１１．０３．１１
        ## １，２３４円
        [re.compile("．"), "."],
        [re.compile("，"), ","],
        ## 1,234
        ## 1,234,567
        ## 1,234,567,890
        ## 1,23 = ichi comma niju san
        ## 1,0 = ichi comma zero
        [re.compile("(\\d)\\,(\\d{3})"), "\\1\\2"],
        [re.compile("(\\d{2})\\,(\\d{3})"), "\\1\\2"],
        [re.compile("(\\d{3})\\,(\\d{3})"), "\\1\\2"],
        [re.compile("(\\d)\\,(\\d{1,2})"), "\\1カンマ\\2"],
        [
            re.compile("(\\d{1,4})\\.(\\d{1,4})\\.(\\d{1,4})\\.(\\d{1,4})"),
            "\\1テン\\2テン\\3テン\\4",
        ],
        [re.compile("(\\d{1,4})\\.(\\d{1,4})\\.(\\d{1,4})"), "\\1テン\\2テン\\3"],
        # do not replace '0' after '.' to phonetic symbols (prepare)
        [re.compile("\\.0"), ".0\u00a0"],
        [
            re.compile("\\b0(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)", re_ascii),
            "  \u00a00  \u00a0\\1  \u00a0\\2  \u00a0\\3  \u00a0\\4  \u00a0\\5  \u00a0\\6  \u00a0\\7  \u00a0\\8  \u00a0\\9 ",
        ],
        [
            re.compile("\\b0(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)", re_ascii),
            "  \u00a00  \u00a0\\1  \u00a0\\2  \u00a0\\3  \u00a0\\4  \u00a0\\5  \u00a0\\6  \u00a0\\7  \u00a0\\8 ",
        ],
        [
            re.compile("\\b0(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)", re_ascii),
            "  \u00a00  \u00a0\\1  \u00a0\\2  \u00a0\\3  \u00a0\\4  \u00a0\\5  \u00a0\\6  \u00a0\\7 ",
        ],
        [
            re.compile("\\b0(\\d)(\\d)(\\d)(\\d)(\\d)(\\d)", re_ascii),
            "  \u00a00  \u00a0\\1  \u00a0\\2  \u00a0\\3  \u00a0\\4  \u00a0\\5  \u00a0\\6 ",
        ],
        [
            re.compile("\\b0(\\d)(\\d)(\\d)(\\d)(\\d)", re_ascii),
            "  \u00a00  \u00a0\\1  \u00a0\\2  \u00a0\\3  \u00a0\\4  \u00a0\\5 ",
        ],
        [
            re.compile("\\b0(\\d)(\\d)(\\d)(\\d)", re_ascii),
            "  \u00a00  \u00a0\\1  \u00a0\\2  \u00a0\\3  \u00a0\\4 ",
        ],
        [
            re.compile("\\b0(\\d)(\\d)(\\d)", re_ascii),
            "  \u00a00  \u00a0\\1  \u00a0\\2  \u00a0\\3 ",
        ],
        [re.compile("\\b0(\\d)(\\d)", re_ascii), "  \u00a00  \u00a0\\1  \u00a0\\2 "],
        [re.compile("\\b0(\\d)", re_ascii), "  \u00a00  \u00a0\\1 "],
        [re.compile(" \u00a00"), "ゼロ"],
        [re.compile(" \u00a01"), "イチ"],
        [re.compile(" \u00a02"), "ニー"],
        [re.compile(" \u00a03"), "サン"],
        [re.compile(" \u00a04"), "ヨン"],
        [re.compile(" \u00a05"), "ゴー"],
        [re.compile(" \u00a06"), "ロク"],
        [re.compile(" \u00a07"), "ナナ"],
        [re.compile(" \u00a08"), "ハチ"],
        [re.compile(" \u00a09"), "キュー"],
        # do not replace '0' after '.' to phonetic symbols (finalize)
        [re.compile("\\.0\u00a0"), ".0"],
    ]
