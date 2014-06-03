# NVDAObjects/IAccessible/atok.py

from logHandler import log
import tones
from . import IAccessible
import controlTypes
import speech
import api
import time
import winUser
import mouseHandler

class ATOK26Cand(IAccessible):
	name=_("Candidate")
	role=controlTypes.ROLE_LIST

	def event_show(self):
		#tones.beep(880,20)
		log.debug("candidate show")

class ATOK26UIComment(IAccessible):
	role=controlTypes.ROLE_STATICTEXT

	def _get_name(self):
		name = self.displayText
		return name

	def event_show(self):
		tones.beep(880,20)
		api.setNavigatorObject(self)
		speech.cancelSpeech()
		time.sleep(0.2)
		speech.speakMessage(self.name)
		(left,top,width,height)=self.location
		x=left+(width/2)
		y=top+(height/2)
		winUser.setCursorPos(x,y)
		mouseHandler.executeMouseMoveEvent(x,y)

def findExtraOverlayClasses(obj,clsList):
	windowClassName=obj.windowClassName
	if windowClassName.endswith("Cand"):
		clsList.append(ATOK26Cand)
	elif windowClassName.endswith("UIComment"):
		clsList.append(ATOK26UIComment)
