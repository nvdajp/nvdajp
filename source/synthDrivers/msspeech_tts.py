#synthDrivers/msspeech_tts.py
# -*- coding: utf-8 -*-
#A part of NonVisual Desktop Access (NVDA)
#Copyright (C) 2006-2011 NVDA Contributors <http://www.nvda-project.org/>
#Copyright (C) 2010-2012 Masataka Shinke, Takuya Nishimoto
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.

import jpUtils
import speech
from logHandler import log

from .jtalk import _nvdajp_spellchar
from .mssp import SynthDriver
from .sapi5 import SpeechVoiceSpeakFlags


class SynthDriver(SynthDriver):
	COM_CLASS = "speech.SPVoice"

	name="msspeech_tts"
	description="Haruka (nvdajp)"

	def __init__(self):
		super(SynthDriver,self).__init__()
		_nvdajp_spellchar.init()

	def speak(self,speechSequence):
		textList=[]
		spellState = False
		for item in speechSequence:
			if isinstance(item, str):
				item=item.replace(u"NVDA", u'エヌブイディーエー')
				item=item.replace(u"\u2022", '') # bullet
				item=item.replace(u"\uf0b7", '') # bullet
				item=item.replace("<","&lt;")
				if spellState:
					item = _nvdajp_spellchar.convert(item)
					#log.info("item replaced to '%s'" % item)
				item = jpUtils.getShortDesc(item)
				textList.append(item.replace("<","&lt;"))
			elif isinstance(item,speech.IndexCommand):
				textList.append("<Bookmark Mark=\"%d\" />"%item.index)
			elif isinstance(item,speech.CharacterModeCommand):
				#textList.append("<spell>" if item.state else "</spell>")
				if item.state: 
					#log.info("spellState = True")
					spellState = True 
				else: 
					#log.info("spellState = False")
					spellState = False
			elif isinstance(item,speech.SpeechCommand):
				log.debugWarning("Unsupported speech command: %s"%item)
			else:
				log.error("Unknown speech: %s"%item)
		text="".join(textList)
		#Pitch must always be hardcoded
		pitch=(self._pitch/2)-25
		text="<pitch absmiddle=\"%s\">%s</pitch>"%(pitch,text)
		flags=SpeechVoiceSpeakFlags.IsXML|SpeechVoiceSpeakFlags.Async
		self.tts.Speak(text,flags)
