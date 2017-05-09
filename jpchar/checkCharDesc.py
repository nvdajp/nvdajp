# coding: UTF-8
#checkCharDesc.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2012-2017 Takuya Nishimoto (NVDA Japanese Team)
# usage:
# > python checkCharDesc.py

#import sys
#sys.path.append(r'..\source\synthDrivers\jtalk')
from _checkCharDesc import *
#ch = read_chardesc_file(CH_FILE)
ch = read_characters_file(CS_FILE)
ch = add_katakana_prefix_to_characters(ch)
find_desc_duplicate(ch, skipKeisen=True, skipEmoji=True)
