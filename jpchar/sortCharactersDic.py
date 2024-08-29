# coding: utf-8
# source/local/ja/characters.dic を Unicode 番号順に並べる

FILENAME = r"..\source\locale\ja\characters.dic"
with open(FILENAME) as file:
	items = {}
	for src in file:
		src = src.rstrip().decode("utf-8")
		if not src:
			continue
		elif src[0] == "#":
			continue
		elif src[0:2] == "\\#":
			line = "#" + src[2:]
		else:
			line = src
		a = line.split("\t")
		if len(a) >= 4:
			items[int(a[1], 16)] = src

for k in sorted(items.keys()):
	print(items[k].encode("utf-8", "ignore"))
