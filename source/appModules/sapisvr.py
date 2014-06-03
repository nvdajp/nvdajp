#appModules/sapisvr.py
#A part of NonVisual Desktop Access (NVDA)
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.
#Copyright (C) 2011 Takuya Nishimoto (nishimotz.com)
#Windows 7 Speech Recognition

import appModuleHandler
import controlTypes
import api
import speech
from NVDAObjects.window import Window
from NVDAObjects.IAccessible import IAccessible

class AppModule(appModuleHandler.AppModule):

	def event_valueChange(self,obj,nextHandler):
		speech.speakMessage(obj.value)
		return nextHandler()
