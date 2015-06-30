# coding: utf-8
# characters.dic 形式から Unicode 番号順に並べて symbols.dic 書式にする
# 必ずこの文字で音声エンジンに読ませる場合のための定義
#
# input (tab separated):
# 䪼	4abc	[セツ]	デグチノ デルニ ミギガ オーガイノ セツ
#
# output (tab separated):
# 䪼	セツ	none	# 䪼 U+4abc


from __future__ import print_function, unicode_literals

import csv
import unicodedata

from _checkCharDesc import read_characters_file

FILENAME = r'medicalChars.dic'
with open(FILENAME) as file:
	items = {}
	for src in file:
		src = src.rstrip().decode('utf-8')
		if not src:
			continue
		elif src[0] == '#':
			continue
		elif src[0:2] == '\\#': 
			line = '#' + src[2:]
		else:
			line = src
		a = line.split('\t')
		if len(a) >= 4:
			items[int(a[1], 16)] = "%s\t%s\tnone\t# %s U+%s" % (a[0], a[2].replace('[', '').replace(']', ''), a[0], a[1])

for k in sorted(items.keys()):
	print(items[k].encode('utf-8', 'ignore'))

