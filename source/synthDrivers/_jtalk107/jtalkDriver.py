# _nvdajp_jtalk.py 
# -*- coding: utf-8 -*-
#A part of NonVisual Desktop Access (NVDA)
# speech engine nvdajp_jtalk
# Copyright (C) 2010-2014 Takuya Nishimoto (nishimotz.com)

from logHandler import log
import time
import Queue
import os
import codecs
import re
import string
import ctypes
import baseObject
import copy
import nvwave
from .. import _espeak
from jtalkCore import *
import jtalkPrepare 
from ..jtalk._nvdajp_unicode import unicode_normalize
from ..jtalk import _bgthread
import sys
import time
import watchdog
import config

jtalk_dir = unicode(os.path.dirname(__file__), 'mbcs')
if hasattr(sys,'frozen'):
	d = os.path.join(os.getcwdu(), 'synthDrivers', '_jtalk107')
	if os.path.isdir(d):
		jtalk_dir = d

mecab_dir = os.path.join(jtalk_dir, '..', 'jtalk')

DEBUG = False

RATE_BOOST_MULTIPLIER = 1.5

# math.log(150) = 5.0, math.log(350) = 5.86
_jtalk_voices = [
	{"id": "V1",
	 "name": "m001",
	 "lang":"ja",
	 "samp_rate": 48000,
	 "fperiod": 240,
	 "lf0_base": 5.0,
	 "pitch_bias": 0,
	 "speaker_attenuation": 1.0,
	 "htsvoice": os.path.join(jtalk_dir, 'm001', 'm001.htsvoice'),
	 "espeak_variant": "max"},
	{"id": "V2",
	 "name": "mei",
	 "lang":"ja",
	 "samp_rate": 48000,
	 "fperiod": 240,
	 "lf0_base": 5.86,
	 "pitch_bias": -10,
	 "speaker_attenuation": 0.5,
	 "htsvoice": os.path.join(jtalk_dir, 'mei', 'mei_normal.htsvoice'),
	 "espeak_variant": "f1"},
	{"id": "V3",
	 "name": "lite",
	 "lang":"ja",
	 "samp_rate": 16000,
	 "fperiod": 80,
	 "lf0_base": 5.0,
	 "pitch_bias": 0,
	 "speaker_attenuation": 1.0,
	 "htsvoice": os.path.join(jtalk_dir, 'lite', 'voice.htsvoice'),
	 "espeak_variant": "max"},
]
default_jtalk_voice = _jtalk_voices[1] # V2
voice_args = None

class VoiceProperty(baseObject.AutoPropertyObject):
	def __init__(self):
		super(VoiceProperty,self).__init__()

# if samp_rate==16000: normal speed = 80samples period
fperiod = 240

# gain control
max_level = 32000
thres_level = 128
thres2_level = 128
speaker_attenuation = 1.0

logwrite = log.debug
lastIndex = None
currIndex = None
lastIndex = None
player = None
currentEngine = 0 # 1:espeak 2:jtalk

def isSpeaking():
	return _bgthread.isSpeaking

def setSpeaking(b):
	_bgthread.isSpeaking = b

def _jtalk_speak(msg, index=None, prop=None):
	global currIndex, buff
	global currentEngine
	global lastIndex
	if prop is None: return
	currIndex = index
	if prop.characterMode:
		fperiod_current = voice_args['fperiod']
	else:
		fperiod_current = fperiod
	msg = unicode_normalize(msg)
	msg = jtalkPrepare.convert(msg)
	lw = None
	if DEBUG: lw = logwrite
	setSpeaking(True)
	currentEngine = 2
	if DEBUG: logwrite("p:%d i:%d msg:%s" % (prop.pitch, prop.inflection, msg))
	level =	int(max_level * speaker_attenuation)
	la = 0.020 * prop.inflection # 50 = original range
	ls = 0.015 * (prop.pitch - 50.0 + voice_args['pitch_bias']) # 50 = no shift
	lo = ls + voice_args['lf0_base'] * (1 - la)
	if DEBUG: logwrite("lo:%f la:%f" % (lo, la))
	for t in string.split(msg):
		if DEBUG: logwrite("unicode (%s)" % t)
		s = text2mecab(t)
		if DEBUG: logwrite("utf-8 (%s)" % s.decode('utf-8', 'ignore'))
		if not isSpeaking(): libjt_refresh(); return
		mf = MecabFeatures()
		Mecab_analysis(s, mf, logwrite_=logwrite)
		if DEBUG: Mecab_print(mf, logwrite)
		Mecab_correctFeatures(mf)
		if DEBUG: Mecab_print(mf, logwrite)
		ar = Mecab_splitFeatures(mf, CODE_='utf-8')
		for a in ar:
			if isSpeaking():
				if DEBUG: Mecab_print(a, logwrite, CODE_='utf-8')
				Mecab_utf8_to_cp932(a)
				if DEBUG: logwrite("Mecab_analysis done")
				libjt_synthesis(
					a.feature,
					a.size,
					fperiod_ = fperiod_current,
					feed_func_ = player.feed, # player.feed() is called inside
					is_speaking_func_ = isSpeaking,
					begin_thres_ = thres_level,
					end_thres_ = thres2_level,
					level_ = level,
					logwrite_ = lw,
					lf0_offset_ = lo,
					lf0_amp_ = la)
				libjt_refresh()
				if DEBUG: logwrite("libjt_synthesis done")
			del a
		del mf
	player.sync()
	lastIndex = currIndex
	currIndex = None
	setSpeaking(False)
	currentEngine = 0

espeakMark = 10000

def _espeak_speak(msg, lang, index=None, prop=None):
	global currentEngine, lastIndex, espeakMark
	currentEngine = 1
	msg = unicode(msg)
	msg.translate({ord(u'\01'):None,ord(u'<'):u'&lt;',ord(u'>'):u'&gt;'})
	msg = u"<voice xml:lang=\"%s\">%s</voice>" % (lang, msg)
	msg += u"<mark name=\"%d\" />" % espeakMark
	_espeak.speak(msg)
	while currentEngine == 1 and _espeak.lastIndex != espeakMark:
		time.sleep(0.1)
		watchdog.alive()
	time.sleep(0.4)
	watchdog.alive()
	lastIndex = index
	currentEngine = 0
	espeakMark += 1

# call from BgThread
def _speak(arg):
	msg, lang, index, prop = arg
	if DEBUG: logwrite('[' + lang + ']' + msg)
	if DEBUG: logwrite("_speak(%s)" % msg)
	if lang == 'ja':
		_jtalk_speak(msg, index, prop)
	else:
		_espeak_speak(msg, lang, index, prop)

def speak(msg, lang, index=None, voiceProperty_=None):
	msg = msg.strip()
	if len(msg) == 0: return
	if voiceProperty_ is None: return
	arg = [msg, lang, index, copy.deepcopy(voiceProperty_)]
	_bgthread.execWhenDone(_speak, arg, mustBeAsync=True)

def stop():
	global currentEngine
	if currentEngine == 1:
		_espeak.stop()
		currentEngine = 0
		return
	# Kill all speech from now.
	# We still want parameter changes to occur, so requeue them.
	params = []
	stop_task_count = 0 # for log.info()
	try:
		while True:
			item = _bgthread.bgQueue.get_nowait() # [func, args, kwargs]
			if item[0] != _speak:
				params.append(item)
			else:
				stop_task_count = stop_task_count + 1
			_bgthread.bgQueue.task_done()
	except Queue.Empty:
		# Let the exception break us out of this loop, as queue.empty() is not reliable anyway.
		pass
	for item in params:
		_bgthread.bgQueue.put(item)
	setSpeaking(False)
	if DEBUG: logwrite("stop: %d task(s) stopping" % stop_task_count)
	player.stop()
	lastIndex = None

def pause(switch):
	if currentEngine == 1:
		_espeak.pause(switch)
	elif currentEngine == 2:
		player.pause(switch)

def initialize(voice = default_jtalk_voice):
	global player, voice_args
	global speaker_attenuation
	voice_args = voice
	speaker_attenuation = voice_args['speaker_attenuation']
	if not _espeak.espeakDLL:
		_espeak.initialize()
		log.debug("jtalk using eSpeak version %s" % _espeak.info())
	_espeak.setVoiceByLanguage("en")
	_espeak.setVoiceAndVariant(variant=voice["espeak_variant"])
	if not player:
		player = nvwave.WavePlayer(channels=1, samplesPerSec=voice_args['samp_rate'], bitsPerSample=16, outputDevice=config.conf["speech"]["outputDevice"])
	if not _bgthread.bgThread:
		_bgthread.initialize()
	if not mecab:
		Mecab_initialize(logwrite_=log.info, mecab_dir = mecab_dir)
	jtalkPrepare.setup()

	jt_dll = os.path.join(jtalk_dir, 'libopenjtalk.dll')
	log.debug('jt_dll %s' % jt_dll)
	libjt_initialize(jt_dll)
	log.debug(libjt_version())

	if os.path.isfile(voice_args['htsvoice']):
		libjt_load(voice_args['htsvoice'])
		log.info("loaded " + voice_args['htsvoice'])
	else:
		log.error("load error " + voice_args['htsvoice'])

def terminate():
	global player
	stop()
	_bgthread.terminate()
	player.close()
	player = None
	_espeak.terminate()

rate_percent = 50

def get_rate(rateBoost):
	return rate_percent

def set_rate(rate, rateBoost):
	global fperiod, rate_percent
	rate_percent = rate
	if voice_args['samp_rate'] == 16000:
		fperiod = int(80 - int(rate) / 2) # 80..30
	if voice_args['samp_rate'] == 48000:
		fperiod = int(240 - 1.5 * int(rate)) # 240..90
	if not rateBoost:
		fperiod = int(fperiod * RATE_BOOST_MULTIPLIER)

def set_volume(vol):
	global max_level, thres_level, thres2_level
	max_level = int(326.67 * int(vol) + 100) # 100..32767
	thres_level = 128
	thres2_level = 128

