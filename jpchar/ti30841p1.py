# coding: UTF-8
# ti30841p1
#
# input emoji.txt
# 🐀,u'\U0001f400',鼠,ネズミ
#
# output (stdout)
# 🐀	1f400	[ネズミ]	ネズミノ エモジ

import codecs

with codecs.open("emoji.txt", "r", "utf-8") as file:
	lines = file.readlines()

dic = {}

for line in lines:
	line = line.rstrip()
	fields = line.split(",")
	if len(fields) == 4:
		if fields[0] in dic:
			continue
		s = "%s\t%s\t[%s]\t%s" % (
			fields[0],
			fields[1].replace(r"u'\U000", "").replace("'", ""),
			fields[3],
			fields[3] + "ノ エモジ",
		)
		print(s.encode("utf-8"))
		dic[fields[0]] = True
