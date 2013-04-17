# _jtalk_core.py 
# -*- coding: utf-8 -*-
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2010-2012 Takuya Nishimoto (NVDA Japanese Team)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

# Japanese speech engine wrapper for Open JTalk
# http://ja.nishimotz.com/project:libopenjtalk

import codecs
import re
import string
import os
import struct
import sys
from mecab import *

############################################

# htsengineapi/include/HTS_engine.h

# size of structure:
# HTS_Global     56
# HTS_ModelSet   76
# HTS_Label      24
# HTS_SStreamSet 24
# HTS_PStreamSet 12
# HTS_GStreamSet 20

class HTS_ModelSet(Structure):
	_fields_ = [
		("_dummy", c_byte * 56),
	]

class HTS_Label(Structure):
	_fields_ = [
		("_dummy", c_byte * 76),
	]
HTS_Label_ptr = POINTER(HTS_Label)

class HTS_SStreamSet(Structure):
	_fields_ = [
		("_dummy", c_byte * 24),
	]

class HTS_PStreamSet(Structure):
	_fields_ = [
		("_dummy", c_byte * 12),
	]

class HTS_GStream(Structure):
	_fields_ = [
		("static_length", c_int), # int static_length;  /* static features length */
		("par", c_double_p_p), # double **par; /* generated parameter */
	]

HTS_GStream_ptr = POINTER(HTS_GStream)

# FIXME: engine.gss.total_nsample is always 0
class HTS_GStreamSet(Structure):
	_fields_ = [
		("total_nsample", c_int), # int total_nsample; /* total sample */
		("total_frame", c_int), # int total_frame; /* total frame */
		("nstream", c_int), # int nstream; /* # of streams */
		("gstream", HTS_GStream_ptr), # HTS_GStream *gstream; /* generated parameter streams */
		("gspeech", c_short_p), # short *gspeech; /* generated speech */
	]
HTS_GStreamSet_ptr = POINTER(HTS_GStreamSet)

class HTS_Global(Structure):
	_fields_ = [
		("state", c_int), 		# /* Gamma=-1/stage : if stage=0 then Gamma=0 */
		("use_log_gain", c_int), 	# HTS_Boolean (TRUE=1) /* log gain flag (for LSP) */
		("sampling_rate", c_int), 	# /* sampling rate */
		("fperiod", c_int),		# /* frame period */
		("alpha", c_double),		# /* all-pass constant */
		("beta", c_double),		# /* postfiltering coefficient */
		("audio_buff_size", c_int),	# /* audio buffer size (for audio device) */
		("msd_threshold", c_double_p),	# /* MSD thresholds */
		("duration_iw", c_double_p),	# /* weights for duration interpolation */
		("parameter_iw", c_double_p_p),	# /* weights for parameter interpolation */
		("gv_iw", c_double_p_p),	# /* weights for GV interpolation */
		("gv_weight", c_double_p),	# /* GV weights */
	]
HTS_Global_ptr = POINTER(HTS_Global)

class HTS_Engine(Structure):
	_fields_ = [
		("global", HTS_Global),
		("audio", c_void_p), # HTS_Audio (requires nvdajp miscdep 86 or later)
		("ms", HTS_ModelSet),
		("label", HTS_Label),
		("sss", HTS_SStreamSet),
		("pss", HTS_PStreamSet),
		("gss", HTS_GStreamSet),
		("lf0_offset", c_double),
		("lf0_amp", c_double),
	]
HTS_Engine_ptr = POINTER(HTS_Engine)

############################################

class NJD(Structure):
	_fields_ = [
		("_dummy", c_byte * 8),
	]
NJD_ptr = POINTER(NJD)

class JPCommonNode(Structure):
	pass
JPCommonNode_ptr = POINTER(JPCommonNode)
JPCommonNode._fields_ = [
		('pron', c_char_p),
		('pos', c_char_p),
		('ctype', c_char_p),
		('cform', c_char_p),
		('acc', c_int),
		('chain_flag', c_int),
		('prev', JPCommonNode_ptr),
		('next', JPCommonNode_ptr),
	]

class JPCommonLabelBreathGroup(Structure):
	pass
JPCommonLabelBreathGroup_ptr = POINTER(JPCommonLabelBreathGroup)

class JPCommonLabelAccentPhrase(Structure):
	pass
JPCommonLabelAccentPhrase_ptr = POINTER(JPCommonLabelAccentPhrase)

class JPCommonLabelWord(Structure):
	pass
JPCommonLabelWord_ptr = POINTER(JPCommonLabelWord)

class JPCommonLabelMora(Structure):
	pass
JPCommonLabelMora_ptr = POINTER(JPCommonLabelMora)

class JPCommonLabelPhoneme(Structure):
	pass
JPCommonLabelPhoneme_ptr = POINTER(JPCommonLabelPhoneme)

# jpcommon/jpcommon.h
class JPCommonLabel(Structure):
	_fields_ = [
		('size', c_int),
		('feature', c_char_p_p),
		('breath_head', JPCommonLabelBreathGroup_ptr),
		('breath_tail', JPCommonLabelBreathGroup_ptr),
		('accent_head', JPCommonLabelAccentPhrase_ptr),
		('accent_tail', JPCommonLabelAccentPhrase_ptr),
		('word_head', JPCommonLabelWord_ptr),
		('word_tail', JPCommonLabelWord_ptr),
		('mora_head', JPCommonLabelMora_ptr),
		('mora_tail', JPCommonLabelMora_ptr),
		('phoneme_head', JPCommonLabelPhoneme_ptr),
		('phoneme_tail', JPCommonLabelPhoneme_ptr),
		('short_pause_flag', c_int),
	]
JPCommonLabel_ptr = POINTER(JPCommonLabel)

class JPCommon(Structure):
	_fields_ = [
		("head", JPCommonNode_ptr),
		("tail", JPCommonNode_ptr),
		("label", JPCommonLabel_ptr),
	]
JPCommon_ptr = POINTER(JPCommon)

# for debug
def JPC_label_print(feature, size, logwrite_):
	if logwrite_ is None: return
	if feature is None or size is None: 
		logwrite_( "JPC_label_print size: 0" )
		return
	s2 = "JPC_label_print size: %d\n" % size
	for i in xrange(0, size):
		s = string_at(feature[i])
		if s:
			s2 += "%s\n" % s
		else:
			s2 += "[None]"
	logwrite_(s2)

#############################################

FNLEN = 1000
FILENAME = c_char * FNLEN
FILENAME_ptr = POINTER(FILENAME)
FILENAME_ptr_ptr = POINTER(FILENAME_ptr)
FILENAME_ptr_x3 = FILENAME_ptr * 3
FILENAME_ptr_x3_ptr = POINTER(FILENAME_ptr_x3)

libjt = None
njd = NJD()
jpcommon = JPCommon()
engine = HTS_Engine()
use_lpf = 0

def libjt_version():
	if libjt is None: return "libjt version none"
	return libjt.jt_version()

def libjt_initialize(JT_DLL, **args):
	global libjt, njd, jpcommon, engine, use_lpf
	use_lpf = args['use_lpf']
	
	if libjt is None: libjt = cdll.LoadLibrary(JT_DLL.encode('mbcs'))
	libjt.jt_version.restype = c_char_p
	
	libjt.NJD_initialize.argtypes = [NJD_ptr]
	libjt.NJD_initialize(njd)

	libjt.JPCommon_initialize.argtypes = [JPCommon_ptr]
	libjt.JPCommon_initialize(jpcommon)

	libjt.HTS_Engine_initialize.argtypes = [HTS_Engine_ptr, c_int]
	if use_lpf:
		libjt.HTS_Engine_initialize(engine, 3)
	else:
		libjt.HTS_Engine_initialize(engine, 2)
	
	libjt.HTS_Engine_set_sampling_rate.argtypes = [HTS_Engine_ptr, c_int]
	libjt.HTS_Engine_set_sampling_rate(engine, args['samp_rate']) # 16000
	
	libjt.HTS_Engine_set_fperiod.argtypes = [HTS_Engine_ptr, c_int]
	libjt.HTS_Engine_set_fperiod(engine, args['fperiod']) # if samping-rate is 16000: 80(point=5ms) frame period

	libjt.HTS_Engine_set_alpha.argtypes = [HTS_Engine_ptr, c_double]
	libjt.HTS_Engine_set_alpha(engine, args['alpha']) # 0.42

	libjt.HTS_Engine_set_gamma.argtypes = [HTS_Engine_ptr, c_int]
	libjt.HTS_Engine_set_gamma(engine, 0)
	
	libjt.HTS_Engine_set_log_gain.argtypes = [HTS_Engine_ptr, c_int]
	libjt.HTS_Engine_set_log_gain(engine, 0)
	
	libjt.HTS_Engine_set_beta.argtypes = [HTS_Engine_ptr, c_double]
	libjt.HTS_Engine_set_beta(engine, 0.0)
	
	libjt.HTS_Engine_set_audio_buff_size.argtypes = [HTS_Engine_ptr, c_int]
	libjt.HTS_Engine_set_audio_buff_size(engine, 1600)
	
	libjt.HTS_Engine_set_msd_threshold.argtypes = [HTS_Engine_ptr, c_int, c_double]
	libjt.HTS_Engine_set_msd_threshold(engine, 1, 0.5)
	
	libjt.HTS_Engine_set_gv_weight.argtypes = [HTS_Engine_ptr, c_int, c_double]
	libjt.HTS_Engine_set_gv_weight(engine, 0, 1.0)
	libjt.HTS_Engine_set_gv_weight(engine, 1, 0.7)
	if use_lpf:
		libjt.HTS_Engine_set_gv_weight(engine, 2, 1.0)
	
	# for libjt_synthesis()
	libjt.mecab2njd.argtypes = [NJD_ptr, FEATURE_ptr_array_ptr, c_int]
	libjt.njd_set_pronunciation.argtypes = [NJD_ptr]
	libjt.njd_set_digit.argtypes = [NJD_ptr]
	libjt.njd_set_accent_phrase.argtypes = [NJD_ptr]
	libjt.njd_set_accent_type.argtypes = [NJD_ptr]
	libjt.njd_set_unvoiced_vowel.argtypes = [NJD_ptr]
	libjt.njd_set_long_vowel.argtypes = [NJD_ptr]
	libjt.njd2jpcommon.argtypes = [JPCommon_ptr, NJD_ptr]
	libjt.JPCommon_make_label.argtypes = [JPCommon_ptr]
	libjt.JPCommon_get_label_size.argtypes = [JPCommon_ptr]
	libjt.JPCommon_get_label_size.argtypes = [JPCommon_ptr]
	libjt.JPCommon_get_label_feature.argtypes = [JPCommon_ptr]
	libjt.JPCommon_get_label_feature.restype = c_char_p_p
	libjt.JPCommon_get_label_size.argtypes = [JPCommon_ptr]
	libjt.HTS_Engine_load_label_from_string_list.argtypes = [
		HTS_Engine_ptr, c_char_p_p, c_int]

	libjt.HTS_Engine_create_sstream.argtypes = [HTS_Engine_ptr]
	libjt.HTS_Engine_create_pstream.argtypes = [HTS_Engine_ptr]
	libjt.HTS_Engine_create_gstream.argtypes = [HTS_Engine_ptr]
	libjt.HTS_Engine_refresh.argtypes = [HTS_Engine_ptr]
	libjt.JPCommon_refresh.argtypes = [JPCommon_ptr]
	libjt.NJD_refresh.argtypes = [NJD_ptr]
	libjt.HTS_GStreamSet_get_total_nsample.argtypes = [HTS_GStreamSet_ptr]
	libjt.HTS_GStreamSet_get_speech.argtypes = [HTS_GStreamSet_ptr, c_int]
	libjt.NJD_print.argtypes = [NJD_ptr]
	libjt.JPCommon_print.argtypes = [JPCommon_ptr]
	libjt.JPCommonLabel_print.argtypes = [JPCommonLabel_ptr]

	libjt.jt_total_nsample.argtypes = [HTS_Engine_ptr]
	libjt.jt_speech_ptr.argtypes = [HTS_Engine_ptr]
	libjt.jt_speech_ptr.restype = c_short_p
	libjt.jt_save_logs.argtypes = [c_char_p, HTS_Engine_ptr, NJD_ptr]
	libjt.jt_save_riff.argtypes = [c_char_p, HTS_Engine_ptr]
	libjt.jt_speech_normalize.argtypes = [HTS_Engine_ptr, c_short, c_int]
	libjt.jt_trim_silence.argtypes = [HTS_Engine_ptr, c_short, c_short]
	libjt.jt_trim_silence.restype = c_int

	libjt.NJD_clear.argtypes = [NJD_ptr]
	libjt.JPCommon_clear.argtypes = [JPCommon_ptr]
	libjt.HTS_Engine_clear.argtypes = [HTS_Engine_ptr]
	
	libjt.HTS_Engine_set_lf0_offset_amp.argtypes = [HTS_Engine_ptr, c_double, c_double]

	# for libjt_jpcommon_make_label()
	libjt.JPCommonLabel_clear.argtypes = [JPCommonLabel_ptr]
	libjt.JPCommonLabel_initialize.argtypes = [JPCommonLabel_ptr]
	libjt.JPCommonNode_get_pron.restype = c_char_p
	libjt.JPCommonNode_get_pos.restype = c_char_p
	libjt.JPCommonNode_get_ctype.restype = c_char_p
	libjt.JPCommonNode_get_cform.restype = c_char_p
	libjt.JPCommonNode_get_acc.restype = c_int
	libjt.JPCommonNode_get_chain_flag.restype = c_int
	libjt.JPCommonLabel_push_word.argtype = [JPCommonLabel_ptr, c_char_p, c_char_p, c_char_p, c_char_p, c_int, c_int]

def libjt_load(VOICE):
	global libjt, engine, use_lpf
	VOICE = VOICE.encode('mbcs')
	libjt.HTS_Engine_load_duration_from_fn.argtypes = [
		HTS_Engine_ptr, FILENAME_ptr_ptr, FILENAME_ptr_ptr, c_int]
	
	fn_ms_dur_buf = create_string_buffer(os.path.join(VOICE, "dur.pdf"))
	fn_ms_dur_buf_ptr = cast(byref(fn_ms_dur_buf), FILENAME_ptr)
	fn_ms_dur = cast(byref(fn_ms_dur_buf_ptr), FILENAME_ptr_ptr)
	fn_ts_dur_buf = create_string_buffer(os.path.join(VOICE, "tree-dur.inf"))
	fn_ts_dur_buf_ptr = cast(byref(fn_ts_dur_buf), FILENAME_ptr)
	fn_ts_dur = cast(byref(fn_ts_dur_buf_ptr), FILENAME_ptr_ptr)
	libjt.HTS_Engine_load_duration_from_fn(engine, fn_ms_dur, fn_ts_dur, 1)
	
	libjt.HTS_Engine_load_parameter_from_fn.argtypes = [
		HTS_Engine_ptr, FILENAME_ptr_ptr, FILENAME_ptr_ptr,
		FILENAME_ptr_x3_ptr, c_int, c_int, c_int, c_int]
	
	fn_ms_mcp_buf = create_string_buffer(os.path.join(VOICE, "mgc.pdf"))
	fn_ms_mcp_buf_ptr = cast(byref(fn_ms_mcp_buf), FILENAME_ptr)
	fn_ms_mcp = cast(byref(fn_ms_mcp_buf_ptr), FILENAME_ptr_ptr)
	fn_ts_mcp_buf = create_string_buffer(os.path.join(VOICE, "tree-mgc.inf"))
	fn_ts_mcp_buf_ptr = cast(byref(fn_ts_mcp_buf), FILENAME_ptr)
	fn_ts_mcp = cast(byref(fn_ts_mcp_buf_ptr), FILENAME_ptr_ptr)
	fn_ws_mcp_buf_1 = create_string_buffer(os.path.join(VOICE, "mgc.win1"))
	fn_ws_mcp_buf_2 = create_string_buffer(os.path.join(VOICE, "mgc.win2"))
	fn_ws_mcp_buf_3 = create_string_buffer(os.path.join(VOICE, "mgc.win3"))
	fn_ws_mcp_buf_ptr_x3 = FILENAME_ptr_x3(
		cast(byref(fn_ws_mcp_buf_1), FILENAME_ptr),
		cast(byref(fn_ws_mcp_buf_2), FILENAME_ptr),
		cast(byref(fn_ws_mcp_buf_3), FILENAME_ptr))
	fn_ws_mcp = cast(byref(fn_ws_mcp_buf_ptr_x3), FILENAME_ptr_x3_ptr)
	libjt.HTS_Engine_load_parameter_from_fn(
		engine, fn_ms_mcp, fn_ts_mcp, fn_ws_mcp, 
		0, 0, 3, 1)
	
	fn_ms_lf0_buf = create_string_buffer(os.path.join(VOICE, "lf0.pdf"))
	fn_ms_lf0_buf_ptr = cast(byref(fn_ms_lf0_buf), FILENAME_ptr)
	fn_ms_lf0 = cast(byref(fn_ms_lf0_buf_ptr), FILENAME_ptr_ptr)
	fn_ts_lf0_buf = create_string_buffer(os.path.join(VOICE, "tree-lf0.inf"))
	fn_ts_lf0_buf_ptr = cast(byref(fn_ts_lf0_buf), FILENAME_ptr)
	fn_ts_lf0 = cast(byref(fn_ts_lf0_buf_ptr), FILENAME_ptr_ptr)
	fn_ws_lf0_buf_1 = create_string_buffer(os.path.join(VOICE, "lf0.win1"))
	fn_ws_lf0_buf_2 = create_string_buffer(os.path.join(VOICE, "lf0.win2"))
	fn_ws_lf0_buf_3 = create_string_buffer(os.path.join(VOICE, "lf0.win3"))
	fn_ws_lf0_buf_ptr_x3 = FILENAME_ptr_x3(
		cast(byref(fn_ws_lf0_buf_1), FILENAME_ptr),
		cast(byref(fn_ws_lf0_buf_2), FILENAME_ptr),
		cast(byref(fn_ws_lf0_buf_3), FILENAME_ptr))
	fn_ws_lf0 = cast(byref(fn_ws_lf0_buf_ptr_x3), FILENAME_ptr_x3_ptr)
	libjt.HTS_Engine_load_parameter_from_fn(
		engine, fn_ms_lf0, fn_ts_lf0, fn_ws_lf0, 
		1, 1, 3, 1)
	
	if use_lpf:
		fn_ms_lpf_buf = create_string_buffer(os.path.join(VOICE, "lpf.pdf"))
		fn_ms_lpf_buf_ptr = cast(byref(fn_ms_lpf_buf), FILENAME_ptr)
		fn_ms_lpf = cast(byref(fn_ms_lpf_buf_ptr), FILENAME_ptr_ptr)
		fn_ts_lpf_buf = create_string_buffer(os.path.join(VOICE, "tree-lpf.inf"))
		fn_ts_lpf_buf_ptr = cast(byref(fn_ts_lpf_buf), FILENAME_ptr)
		fn_ts_lpf = cast(byref(fn_ts_lpf_buf_ptr), FILENAME_ptr_ptr)
		fn_ws_lpf_buf_1 = create_string_buffer(os.path.join(VOICE, "lpf.win1"))
		fn_ws_lpf_buf_ptr_x3 = FILENAME_ptr_x3(
			cast(byref(fn_ws_lpf_buf_1), FILENAME_ptr), 
			cast(0, FILENAME_ptr), 
			cast(0, FILENAME_ptr))
		fn_ws_lpf = cast(byref(fn_ws_lpf_buf_ptr_x3), FILENAME_ptr_x3_ptr)
		libjt.HTS_Engine_load_parameter_from_fn(engine, fn_ms_lpf, fn_ts_lpf, fn_ws_lpf, 2, 0, 1, 1)
	
	libjt.HTS_Engine_load_gv_from_fn.argtypes = [
		HTS_Engine_ptr, FILENAME_ptr_ptr, FILENAME_ptr_ptr, 
		c_int, c_int]

	fn_ms_gvm_buf = create_string_buffer(os.path.join(VOICE, "gv-mgc.pdf"))
	fn_ms_gvm_buf_ptr = cast(byref(fn_ms_gvm_buf), FILENAME_ptr)
	fn_ms_gvm = cast(byref(fn_ms_gvm_buf_ptr), FILENAME_ptr_ptr)
	fn_ts_gvm_buf = create_string_buffer(os.path.join(VOICE, "tree-gv-mgc.inf"))
	fn_ts_gvm_buf_ptr = cast(byref(fn_ts_gvm_buf), FILENAME_ptr)
	fn_ts_gvm = cast(byref(fn_ts_gvm_buf_ptr), FILENAME_ptr_ptr)
	libjt.HTS_Engine_load_gv_from_fn(
		engine, fn_ms_gvm, fn_ts_gvm, 0, 1)

	fn_ms_gvl_buf = create_string_buffer(os.path.join(VOICE, "gv-lf0.pdf"))
	fn_ms_gvl_buf_ptr = cast(byref(fn_ms_gvl_buf), FILENAME_ptr)
	fn_ms_gvl = cast(byref(fn_ms_gvl_buf_ptr), FILENAME_ptr_ptr)
	fn_ts_gvl_buf = create_string_buffer(os.path.join(VOICE, "tree-gv-lf0.inf"))
	fn_ts_gvl_buf_ptr = cast(byref(fn_ts_gvl_buf), FILENAME_ptr)
	fn_ts_gvl = cast(byref(fn_ts_gvl_buf_ptr), FILENAME_ptr_ptr)
	libjt.HTS_Engine_load_gv_from_fn(
		engine, fn_ms_gvl, fn_ts_gvl, 1, 1)

	libjt.HTS_Engine_load_gv_switch_from_fn.argtypes = [
		HTS_Engine_ptr, FILENAME_ptr]

	fn_gv_switch_buf = create_string_buffer(os.path.join(VOICE, "gv-switch.inf"))
	fn_gv_switch = cast(byref(fn_gv_switch_buf), FILENAME_ptr)
	libjt.HTS_Engine_load_gv_switch_from_fn(
		engine, fn_gv_switch)

def libjt_refresh():
	libjt.HTS_Engine_refresh(engine)
	libjt.JPCommon_refresh(jpcommon)
	libjt.NJD_refresh(njd)

def libjt_clear():
	libjt.NJD_clear(njd)
	libjt.JPCommon_clear(jpcommon)
	libjt.HTS_Engine_clear(engine)

#def libjt_jpcommon_make_label(jpcommon, logwrite_=None):
#	if jpcommon.label:
#		libjt.JPCommonLabel_clear(jpcommon.label)
#	else:
#		jpcommon.label = cast(mc_calloc(1, sizeof(JPCommonLabel)), JPCommonLabel_ptr)
#	libjt.JPCommonLabel_initialize(jpcommon.label)
#	node = jpcommon.head
#	while node:
#		label = jpcommon.label
#		pron = libjt.JPCommonNode_get_pron(node)
#		pos = libjt.JPCommonNode_get_pos(node)
#		ctype = libjt.JPCommonNode_get_ctype(node)
#		cform = libjt.JPCommonNode_get_cform(node)
#		acc = libjt.JPCommonNode_get_acc(node)
#		flag = libjt.JPCommonNode_get_chain_flag(node)
#		if logwrite_ : logwrite_('%s,%s,%d,%d' % (pron, pos, acc, flag))
#		libjt.JPCommonLabel_push_word(label, pron, pos, ctype, cform, acc, flag)
#		node = cast(node[0].next, JPCommonNode_ptr)
#	libjt.JPCommonLabel_make(jpcommon.label)

def libjt_synthesis(feature, size, fperiod_=80, feed_func_=None, is_speaking_func_=None, thres_=32, thres2_=32, level_=32767, logwrite_=None, lf0_offset_=0.0, lf0_amp_=1.0):
	if feature is None or size is None: return None
	if logwrite_ : logwrite_('libjt_synthesis start.')
	try:
		libjt.HTS_Engine_set_lf0_offset_amp(engine, lf0_offset_, lf0_amp_)
		libjt.HTS_Engine_set_fperiod(engine, fperiod_) # 80(point=5ms) frame period
		libjt.mecab2njd(njd, feature, size)
		libjt.njd_set_pronunciation(njd)
		libjt.njd_set_digit(njd)
		libjt.njd_set_accent_phrase(njd)
	except WindowsError:
		if logwrite_ : logwrite_('libjt_synthesis error #1 ')
	# exception: access violation reading 0x00000000
	# https://github.com/nishimotz/libopenjtalk/commit/10d3abda6835e0547846fb5e12a36c1425561aaa#diff-66
	try:
		libjt.njd_set_accent_type(njd)
	except WindowsError:
		if logwrite_ : logwrite_('libjt_synthesis njd_set_accent_type() error ')
	try:
		libjt.njd_set_unvoiced_vowel(njd)
		libjt.njd_set_long_vowel(njd)
		libjt.njd2jpcommon(jpcommon, njd)
		libjt.JPCommon_make_label(jpcommon)
	except WindowsError:
		if logwrite_ : logwrite_('libjt_synthesis error #2 ')
	if is_speaking_func_ and not is_speaking_func_() :
		libjt_refresh()
		return None
	try:
		s = libjt.JPCommon_get_label_size(jpcommon)
	except WindowsError:
		if logwrite_ : logwrite_('libjt_synthesis JPCommon_get_label_size() error ')
	buf = None
	if s > 2:
		try:
			f = libjt.JPCommon_get_label_feature(jpcommon)
			libjt.HTS_Engine_load_label_from_string_list(engine, f, s)
			libjt.HTS_Engine_create_sstream(engine)
			libjt.HTS_Engine_create_pstream(engine)
			libjt.HTS_Engine_create_gstream(engine)
		except WindowsError:
			if logwrite_ : logwrite_('libjt_synthesis error #3 ')
		if is_speaking_func_ and not is_speaking_func_() :
			libjt_refresh()
			return None
		try:
			total_nsample = libjt.jt_trim_silence(engine, thres_, thres2_)
			libjt.jt_speech_normalize(engine, level_, total_nsample)
			speech_ptr = libjt.jt_speech_ptr(engine)
			byte_count = total_nsample * sizeof(c_short)
			buf = string_at(speech_ptr, byte_count)
			if feed_func_: feed_func_(buf)
			#libjt.jt_save_logs("_logfile", engine, njd)
		except WindowsError:
			if logwrite_ : logwrite_('libjt_synthesis error #5 ')
	if logwrite_ : logwrite_('libjt_synthesis done.')
	return buf
