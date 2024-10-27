# coding: UTF-8
# checkSymbols.py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2012-2016,2023 Takuya Nishimoto, NVDA Japanese Team, Shuaruta Inc.
# usage:
# > cd jpchar
# > py -3 checkSymbols.py

import _checkCharDesc as cc

print("symbols.dic - characterDescriptions.dic")
sy = cc.read_symbol_file(cc.SY_FILE, raiseDuplicated=False)
cd = cc.read_chardesc_file(cc.CH_FILE)
cc.print_different(sy, cd, skip_included=True)

print("symbols.dic - characters.dic")
ch = cc.read_characters_file(cc.CS_FILE, use_both=True)
cc.print_different(sy, ch, skip_included=True)
