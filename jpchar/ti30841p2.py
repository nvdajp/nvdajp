# coding: UTF-8
# ti30841p2
#
# input ../source/locale/ja/characters.dic
# 🌀	1f300	[グルグル]	タイフウ グルグルノ エモジ
#
# output (stdout)
# 🌀	グルグル	none

import codecs

with codecs.open("../source/locale/ja/characters.dic", "r", "utf-8") as file:
	lines = file.readlines()

for line in lines:
	line = line.rstrip()
	if len(line) == 0 or line[0] == "#":
		print()
		continue
	fields = line.split("\t")
	if len(fields[1]) == 5:
		s = "%s\t%s\tnone" % (fields[0], fields[2].replace("[", "").replace("]", ""))
		print(s.encode("utf-8"))
