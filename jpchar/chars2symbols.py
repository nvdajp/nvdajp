# coding: utf-8
# characters.dic 形式から Unicode 番号順に並べて symbols.dic 書式にする
# 必ずこの文字で音声エンジンに読ませる場合のための定義
#
# input (tab separated):
# 䪼	4abc	[セツ]	デグチノ デルニ ミギガ オーガイノ セツ
#
# output (tab separated):
# 䪼	セツ		# 䪼 U+4abc


FILENAME = '../source/locale/ja/characters.dic'
with open(FILENAME, encoding='utf-8') as file:
	items = {}
	for src in file:
		src = src.rstrip()
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
			items[int(a[1], 16)] = "%s\t%s" % (a[0], a[2].replace('[', '').replace(']', ''))

with open('_new_symbols.dic', mode='w', encoding='utf-8') as f:
    for k in sorted(items.keys()):
        f.write(items[k] + '\n')