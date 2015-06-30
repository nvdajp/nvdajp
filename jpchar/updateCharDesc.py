# coding: UTF-8
#updateCharDesc.py
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2012 Takuya Nishimoto (NVDA Japanese Team)
# usage:
# > python updateCharDesc.py

from _checkCharDesc import *
ch = read_characters_file(CS_FILE)

def isZenkakuKatakana(c):
	return re.search(ur'[ァ-ヾ]', c) is not None

def isHankakuKatakana(c):
	return re.search(ur'[ｦ-ﾝ]', c) is not None

def isHalfShape(c):
	return (32 < ord(c)) and (ord(c) < 128)

d = {}
keys = []
for k,a in ch.items():
	d[ord(k)] = a[1]
	keys.append(ord(k))
	#print k.encode('utf-8')
	#print ord(k) # character code
	#print a[0] # line number
	#print a[1].encode('utf-8')
	#print k + ',' + ','.join(a).encode('utf-8') + "\n"

hex2_curr = None
print "# Discriminant Reading Dictionary for NVDA Japanese"
print "# Copyright (C) 2012 NVDA Japanese Team"
for k in sorted(keys):
	hex4 = u"%04x" % k
	hex2 = hex4[0:2]
	if hex2_curr != hex2:
		print
		print "# %sxx" % hex2
	c = unichr(k)
	if c == '#':
		c = r'\#'

	desc = d[k].replace(':', ' ')
	if isZenkakuKatakana(c):
		desc = u'カタカナ ' + desc
	elif isHankakuKatakana(c) or isHalfShape(c):
		desc = u'ハンカク ' + desc

	o = u"%s\t(%s)" % (c, desc)
	print o.encode('utf-8')
	hex2_curr = hex2

print "# end of file"
