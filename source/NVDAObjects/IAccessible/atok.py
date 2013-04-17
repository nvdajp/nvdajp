# NVDAObjects/IAccessible/atok.py

from logHandler import log
import tones
from . import IAccessible
import controlTypes

class ATOK26Cand(IAccessible):
	name=_("Candidate")
	role=controlTypes.ROLE_LIST

	def event_show(self):
		#tones.beep(880,20)
		log.debug("candidate show")

class ATOK26UIComment(IAccessible):
	name=_("ATOK comment")
	role=controlTypes.ROLE_WINDOW

	def event_show(self):
		#tones.beep(880,20)
		log.debug("ui comment show")

def findExtraOverlayClasses(obj,clsList):
	windowClassName=obj.windowClassName
	if windowClassName.endswith("Cand"):
		clsList.append(ATOK26Cand)
	elif windowClassName.endswith("UIComment"):
		clsList.append(ATOK26UIComment)
