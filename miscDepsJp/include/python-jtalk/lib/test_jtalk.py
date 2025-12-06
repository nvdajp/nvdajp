# test_jtalk.py 
# -*- coding: utf-8 -*-

from ctypes import *
from jtalk import *
import re

libjt = None
mecab_feature = None

def test_init():
	global libjt, mecab_feature
	CODE = 'shift_jis'
	FELEN   = 1000 # string len
	FECOUNT = 100
	FEATURE = c_char * FELEN
	FEATURE_ptr = POINTER(FEATURE)
	FEATURE_ptr_array = FEATURE_ptr * FECOUNT
	libjt = cdll.LoadLibrary(JT_DLL)
	mecab_feature = FEATURE_ptr_array()
	for i in xrange(0, FECOUNT):
		buf = libjt.jt_malloc(FELEN)
		mecab_feature[i] = cast(buf, FEATURE_ptr)

def load_features(filename):
	f = open(filename) # utf-8
	_feature = f.readlines()
	f.close()
	size = 0
	for f in _feature:
		us = f.rstrip('\r\n').decode('utf-8')
		if re.compile(u'^、,記号,読点,').match(us):
			continue
		s = us.encode(CODE)
		dst_ptr = mecab_feature[size]
		buf = create_string_buffer(s)
		src_ptr = byref(buf)
		memmove(dst_ptr, src_ptr, len(s)+1)
		size += 1
	return [mecab_feature, size]

def main():
	initialize()
	test_init()
	files = [
		'd35','b13','i35','f34','c33','f48','d41','e40',
		'b21','a47','i18','f33','h34','b42','d29','b49',
		'g24','g23','h19','f32','e42','c19','e03','g42',
	]
	names = [
		'11','12','13','14','15','16','17','18',
		'21','22','23','24','25','26','27','28',
		'31','32','33','34','35','36','37','38',
	]
	for index in xrange(len(files)):
		file = files[index]
		print "speaking %s" % file
		[feature, size] = load_features(file + '.txt')
		for i in xrange(0,5):
			r = 100 - i * 15
			print 'rate:%d' % r
			setRate(r)
			#speak(f, isFeatures=True);
			#time.sleep(5)
			sf = "out\\" + names[index] + ('%d'%i) + '-' + file + ('s%d' % (5-i))
			OpenJTalk_synthesis(feature, size, doPlay=False, saveFile=sf)
		#time.sleep(10)
	terminate()
	print "end"

if __name__ == "__main__":
	main()
