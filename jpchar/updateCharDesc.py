# coding: UTF-8
# updateCharDesc.py
# A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2016 Takuya Nishimoto (NVDA Japanese Team)
# usage:
# > python updateCharDesc.py

from _checkCharDesc import *  # noqa: F403
from getord import getOrd

ch = read_characters_file(CS_FILE)  # noqa: F405


def isZenkakuKatakana(c):
	return re.search(r"[ァ-ヾ]", c) is not None  # noqa: F405


def isHankakuKatakana(c):
	return re.search(r"[ｦ-ﾝ]", c) is not None  # noqa: F405


def isHalfShape(c):
	return (32 < getOrd(c)) and (getOrd(c) < 128)


d = {}
keys = []
for k, a in ch.items():
	d[getOrd(k)] = a[1]
	keys.append(getOrd(k))
	# print k.encode('utf-8')
	# print ord(k) # character code
	# print a[0] # line number
	# print a[1].encode('utf-8')
	# print k + ',' + ','.join(a).encode('utf-8') + "\n"

hex3_curr = None
print("# Discriminant Reading Dictionary for NVDA Japanese")
print("# Copyright (C) 2016 NVDA Japanese Team")
for k in sorted(keys):
	hex5 = "%05x" % k
	hex3 = hex5[0:3]
	if hex3_curr != hex3:
		print()
		print("# %sxx" % hex3)
	c = chr(k)
	if c == "#":
		c = r"\#"

	desc = d[k].replace(":", " ")
	if isZenkakuKatakana(c):
		desc = "カタカナ " + desc
	elif isHankakuKatakana(c) or isHalfShape(c):
		desc = "ハンカク " + desc

	o = "%s\t(%s)" % (c, desc)
	print(o)
	hex3_curr = hex3

print("# end of file")
