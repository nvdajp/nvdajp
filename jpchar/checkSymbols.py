# coding: UTF-8
#checkSymbols.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2012-2016,2023 Takuya Nishimoto, NVDA Japanese Team, Shuaruta Inc.
# usage:
# > cd jpchar
# > py -3 checkSymbols.py

#import sys
#sys.path.append(r'..\source\synthDrivers\jtalk')
from _checkCharDesc import *
sy = read_symbol_file(SY_FILE, raiseDuplicated=False)
#ch = read_chardesc_file(CH_FILE)
ch = read_characters_file(CS_FILE, use_both=True)
print_different(sy, ch, skip_included=True)
