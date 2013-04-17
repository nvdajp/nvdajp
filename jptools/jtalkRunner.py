# _jtalk_runner.py 
# -*- coding: utf-8 -*-
# Japanese speech engine test module
# by Takuya Nishimoto
# http://ja.nishimotz.com/project:libopenjtalk
# Usage:
# > cd source
# > python synthDrivers/jtalk/_jtalk_runner.py

import os
import sys
sys.path.append(r'..\source\synthDrivers\jtalk')
from _jtalk_core import *

import _nvdajp_predic 
#JT_DIR = unicode(os.path.abspath(os.path.dirname(__file__)), 'mbcs')
JT_DIR = r'..\source\synthDrivers\jtalk'
JT_DLL = os.path.join(JT_DIR, 'libopenjtalk.dll')
VOICE_DIR = os.path.join(JT_DIR, 'm001')

# for miscdep/include/jtalk
#JT_DIR = os.path.join(os.getcwdu(), '..', '..', 'source', 'synthDrivers', 'jtalk')
#JT_DLL = os.path.join(JT_DIR, 'libopenjtalk.dll')
#VOICE_DIR = os.path.join(JT_DIR, 'm001')

def pa_play(data, samp_rate = 16000):
	# requires pyaudio (PortAudio wrapper)
	# http://people.csail.mit.edu/hubert/pyaudio/
	import time
	import pyaudio
	p = pyaudio.PyAudio()
	stream = p.open(format = p.get_format_from_width(2),
		channels = 1, rate = samp_rate, output = True)
	size = len(data)
	pos = 0 # byte count
	while pos < size:
		a = stream.get_write_available() * 2
		o = data[pos:pos+a]
		stream.write(o)
		pos += a
	time.sleep(float(size) / 2 / samp_rate)
	stream.close()
	p.terminate()

def __print(s):
	print s.encode('cp932', 'ignore')

def print_code(msg):
	s = ''
	for c in msg:
		s += '%04x ' % ord(c)
	print s

if __name__ == '__main__':
	njd = NJD()
	jpcommon = JPCommon()
	engine = HTS_Engine()
	voice_args = {"id": "V1", "name": "m001", "lang":"ja", "samp_rate": 48000, "fperiod": 240, "alpha": 0.55, "lf0_base":5.0,  "use_lpf":1, "speaker_attenuation":1.0, "dir": VOICE_DIR}
	libjt = libjt_initialize(JT_DLL, **voice_args)
	libjt_load(voice_args['dir'].encode('mbcs'))
	Mecab_initialize(__print, JT_DIR)
	#
	#msg = u'100.25ドル。ウェルカムトゥー nvda テンキーのinsertキーとメインのinsertキーの両方がnvdaキーとして動作します'
	#msg = u'YouTube iTunes Store sjis co jp'
	#msg = u'十五絡脈病証。' # nvdajp ticket 29828
	#msg = u'マーク。まーく。' # nvdajp ticket 29859
	msg = u'∫⣿♪ ウェルカムトゥー 鈹噯呃瘂蹻脘鑱涿癃 十五絡脈病証 マーク。まーく。ふぅー。ふぅぅぅぅぅー。ぅー。ぅぅー。'
	_nvdajp_predic.setup()
	msg = _nvdajp_predic.convert(msg)
	s = Mecab_text2mecab(msg, CODE_='utf-8')
	__print("utf-8: (%s)" % s.decode('utf-8', 'ignore'))
	mf = MecabFeatures()
	Mecab_analysis(s, mf)
	Mecab_print(mf, __print, CODE_='utf-8')
	Mecab_correctFeatures(mf, CODE_='utf-8')
	Mecab_utf8_to_cp932(mf)
	Mecab_print(mf, __print, CODE_='cp932')
	fperiod = voice_args['fperiod']
	data = libjt_synthesis(mf.feature, mf.size, fperiod_ = fperiod, logwrite_ = __print)
	mf = None
	if data: 
		pa_play(data, voice_args['samp_rate'])
		import wave
		w = wave.Wave_write("_test.wav")
		w.setparams( (1, 2, voice_args['samp_rate'], len(data)/2, 'NONE', 'not compressed') )
		w.writeframes(data)
		w.close()
	libjt_clear()
