# coding: UTF-8
#nvdajptext/mecab.py 
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2010-2012 Masataka.Shinke, Takuya Nishimoto

CODE = 'utf-8'

from ctypes import *
import codecs
import re
import string
import os
import struct
import unicodedata
import threading
import sys

DEFAULT_JTALK_DIR = unicode(os.path.dirname(__file__), 'mbcs')
if hasattr(sys,'frozen'):
	d = os.path.join(os.getcwdu(), 'synthDrivers', 'jtalk')
	if os.path.isdir(d):
		DEFAULT_JTALK_DIR = d

c_double_p = POINTER(c_double)
c_double_p_p = POINTER(c_double_p) 
c_short_p = POINTER(c_short)
c_char_p_p = POINTER(c_char_p) 

##############################################

# http://mecab.sourceforge.net/libmecab.html
# c:/mecab/sdk/mecab.h
MECAB_NOR_NODE = 0
MECAB_UNK_NODE = 1
MECAB_BOS_NODE = 2
MECAB_EOS_NODE = 3
class mecab_token_t(Structure):
	pass
mecab_token_t_ptr = POINTER(mecab_token_t)

class mecab_path_t(Structure):
	pass
mecab_path_t_ptr = POINTER(mecab_path_t)

class mecab_node_t(Structure):
	pass
mecab_node_t_ptr = POINTER(mecab_node_t)
mecab_node_t_ptr_ptr = POINTER(mecab_node_t_ptr)
mecab_node_t._fields_ = [
		("prev", mecab_node_t_ptr),
		("next", mecab_node_t_ptr),
		("enext", mecab_node_t_ptr),
		("bnext", mecab_node_t_ptr),
		("rpath", mecab_path_t_ptr),
		("lpath", mecab_path_t_ptr),
		# ("begin_node_list", mecab_node_t_ptr_ptr),
		# ("end_node_list", mecab_node_t_ptr_ptr),
		("surface", c_char_p),
		("feature", c_char_p),
		("id", c_uint),
		("length", c_ushort),
		("rlength", c_ushort),
		("rcAttr", c_ushort),
		("lcAttr", c_ushort),
		("posid", c_ushort),
		("char_type", c_ubyte),
		("stat", c_ubyte),
		("isbest", c_ubyte),
		# ("sentence_length", c_uint),
		("alpha", c_float),
		("beta", c_float),
		("prob", c_float),
		("wcost", c_short),
		("cost", c_long),
		# ("token", mecab_token_t_ptr),
	]

############################################

# typedef struct _Mecab{
#    char **feature;
#    int size;
#    mecab_t *mecab;
# } Mecab;

FELEN   = 1000 # string len
FECOUNT = 1000
FEATURE = c_char * FELEN
FEATURE_ptr = POINTER(FEATURE)
FEATURE_ptr_array = FEATURE_ptr * FECOUNT
FEATURE_ptr_array_ptr = POINTER(FEATURE_ptr_array)

mecab = None
libmc = None
lock = threading.Lock()

mc_malloc = cdll.msvcrt.malloc
mc_malloc.restype = POINTER(c_ubyte)
mc_calloc = cdll.msvcrt.calloc
mc_calloc.restype = POINTER(c_ubyte)
mc_free = cdll.msvcrt.free

class NonblockingMecabFeatures(object):
	def __init__(self):
		self.size = 0
		self.feature = FEATURE_ptr_array()
		for i in xrange(0, FECOUNT):
			buf = mc_malloc(FELEN) 
			self.feature[i] = cast(buf, FEATURE_ptr)

	def __del__(self):
		for i in xrange(0, FECOUNT):
			try:
				mc_free(self.feature[i]) 
			except:
				pass

class MecabFeatures(NonblockingMecabFeatures):
	def __init__(self):
		global lock
		lock.acquire()
		super(MecabFeatures, self).__init__()

	def __del__(self):
		global lock
		super(MecabFeatures, self).__del__()
		lock.release()

predic = None

def text2mecab_setup():
	global predic
	if predic is None:
		predic = [
			[re.compile(u" "), u"　"],
			[re.compile(u"!"), u"！"],
			[re.compile(u"\""), u"”"],
			[re.compile(u"#"), u"＃"],
			[re.compile(u"\\$"), u"＄"],
			[re.compile(u"%"), u"％"],
			[re.compile(u"&"), u"＆"],
			[re.compile(u"'"), u"’"],
			[re.compile(u"\\("), u"（"],
			[re.compile(u"\\)"), u"）"],
			[re.compile(u"\\*"), u"＊"],
			[re.compile(u"\\+"), u"＋"],
			[re.compile(u","), u"，"],
			[re.compile(u"\\-"), u"−"],
			[re.compile(u"\\."), u"．"],
			[re.compile(u"\\/"), u"／"],
			[re.compile(u"0"), u"０"],
			[re.compile(u"1"), u"１"],
			[re.compile(u"2"), u"２"],
			[re.compile(u"3"), u"３"],
			[re.compile(u"4"), u"４"],
			[re.compile(u"5"), u"５"],
			[re.compile(u"6"), u"６"],
			[re.compile(u"7"), u"７"],
			[re.compile(u"8"), u"８"],
			[re.compile(u"9"), u"９"],
			[re.compile(u":"), u"："],
			[re.compile(u";"), u"；"],
			[re.compile(u"<"), u"＜"],
			[re.compile(u"="), u"＝"],
			[re.compile(u">"), u"＞"],
			[re.compile(u"\?"), u"？"],
			[re.compile(u"@"), u"＠"],
			[re.compile(u"A"), u"Ａ"],
			[re.compile(u"B"), u"Ｂ"],
			[re.compile(u"C"), u"Ｃ"],
			[re.compile(u"D"), u"Ｄ"],
			[re.compile(u"E"), u"Ｅ"],
			[re.compile(u"F"), u"Ｆ"],
			[re.compile(u"G"), u"Ｇ"],
			[re.compile(u"H"), u"Ｈ"],
			[re.compile(u"I"), u"Ｉ"],
			[re.compile(u"J"), u"Ｊ"],
			[re.compile(u"K"), u"Ｋ"],
			[re.compile(u"L"), u"Ｌ"],
			[re.compile(u"M"), u"Ｍ"],
			[re.compile(u"N"), u"Ｎ"],
			[re.compile(u"O"), u"Ｏ"],
			[re.compile(u"P"), u"Ｐ"],
			[re.compile(u"Q"), u"Ｑ"],
			[re.compile(u"R"), u"Ｒ"],
			[re.compile(u"S"), u"Ｓ"],
			[re.compile(u"T"), u"Ｔ"],
			[re.compile(u"U"), u"Ｕ"],
			[re.compile(u"V"), u"Ｖ"],
			[re.compile(u"W"), u"Ｗ"],
			[re.compile(u"X"), u"Ｘ"],
			[re.compile(u"Y"), u"Ｙ"],
			[re.compile(u"Z"), u"Ｚ"],
			[re.compile(u"\\["), u"［"],
			[re.compile(u"\\\\"), u"￥"],
			[re.compile(u"\\]"), u"］"],
			[re.compile(u"\\^"), u"＾"],
			[re.compile(u"_"), u"＿"],
			[re.compile(u"`"), u"‘"],
			[re.compile(u"a"), u"ａ"],
			[re.compile(u"b"), u"ｂ"],
			[re.compile(u"c"), u"ｃ"],
			[re.compile(u"d"), u"ｄ"],
			[re.compile(u"e"), u"ｅ"],
			[re.compile(u"f"), u"ｆ"],
			[re.compile(u"g"), u"ｇ"],
			[re.compile(u"h"), u"ｈ"],
			[re.compile(u"i"), u"ｉ"],
			[re.compile(u"j"), u"ｊ"],
			[re.compile(u"k"), u"ｋ"],
			[re.compile(u"l"), u"ｌ"],
			[re.compile(u"m"), u"ｍ"],
			[re.compile(u"n"), u"ｎ"],
			[re.compile(u"o"), u"ｏ"],
			[re.compile(u"p"), u"ｐ"],
			[re.compile(u"q"), u"ｑ"],
			[re.compile(u"r"), u"ｒ"],
			[re.compile(u"s"), u"ｓ"],
			[re.compile(u"t"), u"ｔ"],
			[re.compile(u"u"), u"ｕ"],
			[re.compile(u"v"), u"ｖ"],
			[re.compile(u"w"), u"ｗ"],
			[re.compile(u"x"), u"ｘ"],
			[re.compile(u"y"), u"ｙ"],
			[re.compile(u"z"), u"ｚ"],
			[re.compile(u"{"), u"｛"],
			[re.compile(u"\\|"), u"｜"],
			[re.compile(u"}"), u"｝"],
			[re.compile(u"~"), u"〜"],
		]

def text2mecab_convert(s):
	for p in predic:
		try:
			s = re.sub(p[0], p[1], s)
		except:
			pass
	return s

def Mecab_text2mecab(txt, CODE_=CODE):
	text2mecab_setup()
	txt = unicodedata.normalize('NFKC', txt)
	txt = text2mecab_convert(txt)
	return txt.encode(CODE_, 'ignore')

def Mecab_initialize(logwrite_ = None, jtalk_dir = DEFAULT_JTALK_DIR):
	#if logwrite_: logwrite_('mecab init begin')
	mecab_dll = os.path.join(jtalk_dir, 'libmecab.dll')
	global libmc
	if libmc is None:
		libmc = cdll.LoadLibrary(mecab_dll.encode('mbcs'))
		libmc.mecab_version.restype = c_char_p
		libmc.mecab_strerror.restype = c_char_p
		libmc.mecab_sparse_tonode.restype = mecab_node_t_ptr
		libmc.mecab_new.argtypes = [c_int, c_char_p_p]
	global mecab
	if mecab is None:
		dic = os.path.join(jtalk_dir, 'dic')
		if logwrite_: logwrite_('dic: %s' % dic)
		f = open(os.path.join(dic, "DIC_VERSION"))
		s = f.read().strip()
		f.close()
		logwrite_('mecab:' + libmc.mecab_version() + ' ' + s)
		# check utf-8 dictionary
		if not CODE in s:
			raise RuntimeError('utf-8 dictionary for mecab required.')
		mecabrc = os.path.join(jtalk_dir, 'mecabrc')
		args = (c_char_p * 5)('mecab', '-d', dic.encode('utf-8'), '-r', mecabrc.encode('utf-8'))
		mecab = libmc.mecab_new(5, args)
		if logwrite_:
			if not mecab: logwrite_('mecab_new failed.')
			logwrite_(libmc.mecab_strerror(mecab))
	#if logwrite_: logwrite_('mecab init end')

def Mecab_analysis(src, features, logwrite_ = None):
	if not src:
		if logwrite_: logwrite('src empty')
		features.size = 0
		return
	head = libmc.mecab_sparse_tonode(mecab, src)
	if head is None:
		if logwrite_: logwrite('mecab_sparse_tonode result empty')
		features.size = 0
		return
	features.size = 0

	# make array of features
	node = head
	i = 0
	while node:
		s = node[0].stat
		if s != MECAB_BOS_NODE and s != MECAB_EOS_NODE:
			c = node[0].length
			s = string_at(node[0].surface, c) + "," + string_at(node[0].feature)
			if logwrite_: logwrite_(s.decode(CODE, 'ignore'))
			buf = create_string_buffer(s)
			dst_ptr = features.feature[i]
			src_ptr = byref(buf)
			memmove(dst_ptr, src_ptr, len(s)+1)
			i += 1
		node = node[0].next
		features.size = i
		if i > FECOUNT: 
			if logwrite_: logwrite('too many nodes')
			return
	return

# for debug
def Mecab_print(mf, logwrite_ = None, CODE_ = CODE, output_header = True):
	if logwrite_ is None: return
	feature = mf.feature
	size = mf.size
	if feature is None or size is None: 
		if output_header:
			logwrite_( "Mecab_print size: 0" )
		return
	s2 = ''
	if output_header:
		s2 += "Mecab_print size: %d\n" % size
	for i in xrange(0, size):
		s = string_at(feature[i])
		if s:
			if CODE_ is None:
				s2 += "%d %s\n" % (i, s)
			else:
				s2 += "%d %s\n" % (i, s.decode(CODE_, 'ignore'))
		else:
			s2 += "[None]\n"
	logwrite_(s2)

def Mecab_getFeature(mf, pos, CODE_ = CODE):
	s = string_at(mf.feature[pos])
	return s.decode(CODE_, 'ignore')

def Mecab_setFeature(mf, pos, s, CODE_ = CODE):
	s = s.encode(CODE_, 'ignore')
	buf = create_string_buffer(s)
	dst_ptr = mf.feature[pos]
	src_ptr = byref(buf)
	memmove(dst_ptr, src_ptr, len(s)+1)

def getMoraCount(s):
	# 1/3 => 3
	# */* => 0
	m = s.split('/')
	if len(m) == 2:
		m2 = m[1]
		if m2 != '*':
			return int(m2)
	return 0

# PATTERN 1
# before:
# 1 五絡脈病証,名詞,数,*,*,*,*,*
#
# after:
# 1 五絡脈病証,名詞,普通名詞,*,*,*,*,五絡脈病証,ゴミャクラクビョウショウ,
# ゴミャクラクビョーショー,1/9,C0
# 
# PATTERN 2
# before:
# 0 ∫⣿♪　,名詞,サ変接続,*,*,*,*,*
#
# after:
# 0 ∫⣿♪　,名詞,サ変接続,*,*,*,*,∫♪　,セキブンキゴーイチニーサンヨンゴーロクナナ
# ハチノテンオンプ,セキブンキゴーイチニーサンヨンゴーロクナナハチノテンオンプ,1/29,C0
# 
# PATTERN 3
# before:
# 0 ま,接頭詞,名詞接続,*,*,*,*,ま,マ,マ,1/1,P2
# 1 ー,名詞,一般,*,*,*,*,*
#
# after:
# 0 ま,接頭詞,名詞接続,*,*,*,*,まー,マー,マー,1/2,P2
# 1 ー,名詞,一般,*,*,*,*,*
def Mecab_correctFeatures(mf, CODE_ = CODE):
	for pos in xrange(0, mf.size):
		ar = Mecab_getFeature(mf, pos, CODE_=CODE_).split(',')
		need_fix = False
		if ar[2] == u'数' and ar[7] == u'*': 
			need_fix = True
		if ar[1] == u'名詞' and ar[2] == u'サ変接続' and ar[7] == u'*': 
			need_fix = True
		if need_fix:
			hyoki = ar[0]
			yomi = ''
			pron = ''
			mora = 0
			nbmf = NonblockingMecabFeatures()
			for c in hyoki:
				Mecab_analysis(Mecab_text2mecab(c, CODE_=CODE_), nbmf)
				for pos2 in xrange(0, nbmf.size):
					ar2 = Mecab_getFeature(nbmf, pos2, CODE_=CODE_).split(',')
					if len(ar2) > 10:
						yomi += ar2[8]
						pron += ar2[9]
						mora += getMoraCount(ar2[10])
			nbmf = None
			feature = u'{h},名詞,普通名詞,*,*,*,*,{h},{y},{p},1/{m},C0'.format(h=hyoki, y=yomi, p=pron, m=mora)
			Mecab_setFeature(mf, pos, feature, CODE_=CODE_)
		elif pos > 0 and ar[0] == u'ー' and ar[1] == u'名詞' and ar[2] == u'一般':
			ar2 = Mecab_getFeature(mf, pos-1, CODE_=CODE_).split(',')
			if len(ar2) > 10:
				hyoki = ar2[0] + u'ー'
				hin1 = ar2[1]
				hin2 = ar2[2]
				yomi = ar2[8] + u'ー'
				pron = ar2[9] + u'ー'
				mora = getMoraCount(ar2[10]) + 1
				feature = u'{h},{h1},{h2},*,*,*,*,{h},{y},{p},1/{m},C0'.format(h=hyoki, h1=hin1, h2=hin2, y=yomi, p=pron, m=mora)
				Mecab_setFeature(mf, pos-1, feature, CODE_=CODE_)
			elif pos >= 2:
				ar3 = Mecab_getFeature(mf, pos-2, CODE_=CODE_).split(',')
				if len(ar3) > 10 and ar3[1] != u'記号':
					hyoki = ar3[0] + ar2[0] + u'ー'
					hin1 = ar3[1]
					hin2 = ar3[2]
					yomi = ar3[8] + ar2[0] + u'ー'
					pron = ar3[9] + ar2[0] + u'ー'
					mora = getMoraCount(ar3[10]) + len(ar2[0]) + 1
					feature = u'{h},{h1},{h2},*,*,*,*,{h},{y},{p},1/{m},C0'.format(h=hyoki, h1=hin1, h2=hin2, y=yomi, p=pron, m=mora)
					Mecab_setFeature(mf, pos-2, feature, CODE_=CODE_)

def Mecab_utf8_to_cp932(mf):
	for pos in xrange(0, mf.size):
		s = Mecab_getFeature(mf, pos, CODE_ = 'utf-8')
		Mecab_setFeature(mf, pos, s, CODE_ = 'cp932')
