# from source/jpUtils.jp
def getOrd(s):
	# handle surrogate pairs
	if len(s) == 1:
		return ord(s)
	if len(s) != 2:
		raise Exception
	o0 = ord(s[0])
	o1 = ord(s[1])
	uc = (o0 - 0xd800) * 0x800 + (o1 - 0xdc00)
	return uc
