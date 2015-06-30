# coding: UTF-8
# annotateSymbolsDic.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2015 Takuya Nishimoto (NVDA Japanese Team)
#
# annotate Unicode numbers as comments to symbols
from __future__ import print_function
import pprint

import _checkCharDesc as cd

def convert(sy_file, outfile):
	sy, src = cd.read_symbol_file(sy_file, returnSource=True)
	with open(outfile, 'w') as of:
		for line in src:
			of.write(line.encode('utf-8') + "\n")

convert(
	r"..\..\srt\ja\symbols-newRevisions\11146\symbols.dic",
	'_en.dic'
)

convert(
	#r"..\source\locale\ja\symbols.dic",
	r"..\..\srt\ja\symbols.dic",
	'_ja.dic'
)

