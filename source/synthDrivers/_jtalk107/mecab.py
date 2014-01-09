# coding: UTF-8
# mecab.py for python-jtalk

CODE = 'utf-8'

from ctypes import *
import codecs
import string
import os
import struct
import threading
import sys
from text2mecab import text2mecab

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
		("alpha", c_float),
		("beta", c_float),
		("prob", c_float),
		("wcost", c_short),
		("cost", c_long),
	]

############################################

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

def Mecab_initialize(logwrite_ = None, mecab_dir = None):
	mecab_dll = os.path.join(mecab_dir, 'libmecab.dll')
	global libmc
	if libmc is None:
		libmc = cdll.LoadLibrary(mecab_dll.encode('mbcs'))
		libmc.mecab_version.restype = c_char_p
		libmc.mecab_strerror.restype = c_char_p
		libmc.mecab_sparse_tonode.restype = mecab_node_t_ptr
		libmc.mecab_new.argtypes = [c_int, c_char_p_p]
	global mecab
	if mecab is None:
		dic = os.path.join(mecab_dir, 'dic')
		if logwrite_: logwrite_('dic: %s' % dic)
		try:
			f = open(os.path.join(dic, "DIC_VERSION"))
			s = f.read().strip()
			f.close()
			logwrite_('mecab:' + libmc.mecab_version() + ' ' + s)
			# check utf-8 dictionary
			if not CODE in s:
				raise RuntimeError('utf-8 dictionary for mecab required.')
		except:
			pass
		mecabrc = os.path.join(mecab_dir, 'mecabrc')
		args = (c_char_p * 5)('mecab', '-d', dic.encode('utf-8'), '-r', mecabrc.encode('utf-8'))
		mecab = libmc.mecab_new(5, args)
		if logwrite_:
			if not mecab: logwrite_('mecab_new failed.')
			s = libmc.mecab_strerror(mecab).strip()
			if s: logwrite_(s)

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
		if i >= FECOUNT:
			if logwrite_: logwrite_('too many nodes')
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
				Mecab_analysis(text2mecab(c, CODE_=CODE_), nbmf)
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

def Mecab_duplicateFeatures(mf, startPos = 0, stopPos = None, CODE_ = 'utf-8'):
	if not stopPos:
		stopPos = mf.size
	nbmf = NonblockingMecabFeatures()
	newPos = 0
	for pos in xrange(startPos, stopPos):
		s = Mecab_getFeature(mf, pos, CODE_)
		Mecab_setFeature(nbmf, newPos, s, CODE_)
		newPos += 1
	nbmf.size = newPos
	return nbmf

def Mecab_splitFeatures(mf, CODE_ = 'utf-8'):
	ar = []
	startPos = 0
	for pos in xrange(mf.size):
		a = Mecab_getFeature(mf, pos, CODE_).split(',')
		if a[0].isspace() or a[1] == u'記号' and a[2] in (u'空白', u'句点', u'読点'):
			f = Mecab_duplicateFeatures(mf, startPos, pos + 1, CODE_)
			ar.append(f)
			startPos = pos + 1
	if startPos < mf.size:
		f = Mecab_duplicateFeatures(mf, startPos, mf.size, CODE_)
		ar.append(f)
	return ar
