# NVDAObjects/IAccessible/atok.py

import time

import api
import config
import controlTypes
import mouseHandler
import speech
import tones
import winUser

from . import IAccessible


class ATOKxxUIComment(IAccessible):
	role = controlTypes.Role.STATICTEXT

	def _get_name(self):
		name = self.displayText
		return name

	def event_show(self):
		if not (
			config.conf["keyboard"]["nvdajpEnableKeyEvents"]
			and config.conf["inputComposition"]["announceSelectedCandidate"]
		):
			return
		tones.beep(880, 20)
		api.setNavigatorObject(self)
		speech.cancelSpeech()
		time.sleep(0.2)
		speech.speakMessage(self.name)
		(left, top, width, height) = self.location
		x = left + (width // 2)
		y = top + (height // 2)
		winUser.setCursorPos(x, y)
		mouseHandler.executeMouseMoveEvent(x, y)


def findExtraOverlayClasses(obj, clsList):
	windowClassName = obj.windowClassName
	if windowClassName.endswith("UIComment"):
		clsList.append(ATOKxxUIComment)
