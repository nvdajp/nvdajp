# coding: UTF-8
# ti36402p1
#
# input emoji2.txt
# ‼,u'\u203c',二重感嘆符,ニジュウカンタンフ
#
# output (stdout)
# ‼		203c	[ニジュウカンタンフ]	ニジュウカンタンフノ エモジ

import codecs

with codecs.open("emoji2.txt", "r", "utf-8") as file:
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
			fields[1].replace(r"u'\u", "").replace("'", ""),
			fields[3],
			fields[3] + "ノ エモジ",
		)
		print(s.encode("utf-8"))
		dic[fields[0]] = True
