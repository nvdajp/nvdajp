# coding: UTF-8
#updateCharDesc.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2016 Takuya Nishimoto (NVDA Japanese Team)
# usage:
# > python updateCharDesc.py

from _checkCharDesc import *
from getord import getOrd

ch = read_characters_file(CS_FILE)

def isZenkakuKatakana(c):
	return re.search(ur'[ァ-ヾ]', c) is not None

def isHankakuKatakana(c):
	return re.search(ur'[ｦ-ﾝ]', c) is not None

def isHalfShape(c):
	return (32 < getOrd(c)) and (getOrd(c) < 128)

d = {}
keys = []
for k,a in ch.items():
	d[getOrd(k)] = a[1]
	keys.append(getOrd(k))
	#print k.encode('utf-8')
	#print ord(k) # character code
	#print a[0] # line number
	#print a[1].encode('utf-8')
	#print k + ',' + ','.join(a).encode('utf-8') + "\n"

hex3_curr = None
print "# Discriminant Reading Dictionary for NVDA Japanese"
print "# Copyright (C) 2016 NVDA Japanese Team"
for k in sorted(keys):
	hex5 = u"%05x" % k
	hex3 = hex5[0:3]
	if hex3_curr != hex3:
		print
		print "# %sxx" % hex3
	# http://d.hatena.ne.jp/nishiohirokazu/20120127/1327646600
	c = ("\U" + "%08x" % k).decode("unicode-escape") #unichr(k)
	if c == '#':
		c = r'\#'

	desc = d[k].replace(':', ' ')
	if isZenkakuKatakana(c):
		desc = u'カタカナ ' + desc
	elif isHankakuKatakana(c) or isHalfShape(c):
		desc = u'ハンカク ' + desc

	o = u"%s\t(%s)" % (c, desc)
	print o.encode('utf-8')
	hex3_curr = hex3

print "# end of file"
