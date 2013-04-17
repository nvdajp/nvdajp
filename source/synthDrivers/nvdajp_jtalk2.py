#synthDrivers/nvdajp_jtalk2.py
# -*- coding: utf-8 -*-
#A part of NonVisual Desktop Access (NVDA)
# Copyright (C) 2010-2012 Takuya Nishimoto (nishimotz.com)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#

from nvdajp_jtalk import SynthDriver
from jtalk import _nvdajp_jtalk

class SynthDriver(SynthDriver):
	"""A Japanese/multi-lingual synth driver for NVDAjp.
	"""
	name = "nvdajp_jtalk2"
	description = "JTalk2"

	def __init__(self):
		self.voice_id = 'V2'
		self._volume = 100
		self._pitch = 50
		self._inflection = 50
		self._rateBoost = False
		_nvdajp_jtalk.initialize(_multilang = True)
